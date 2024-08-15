# access stream from portal

import settings
import dbus
from typing import Callable
from gi.repository import Gst
from dbus.mainloop.glib import DBusGMainLoop

class DesktopPortal:
    def __init__(self) -> None:
        DBusGMainLoop(set_as_default=True)

        self.bus = dbus.SessionBus()
        self.bus_name = 'org.freedesktop.portal.Desktop'
        self.bus_object_path = '/org/freedesktop/portal/desktop'
        self.request_iface = 'org.freedesktop.portal.Request'
        self.screen_cast_iface = 'org.freedesktop.portal.ScreenCast'

        self.pipeline = None
        self.session = None

        self.request_token_counter = 0
        self.session_token_counter = 0
        self.sender_name = self.bus.get_unique_name()[1:].replace('.', '_')

        self.portal = self.bus.get_object(self.bus_name, self.bus_object_path)
        self.callback_on_start = lambda *x: True

    def start_screencast_request(self, callback_on_start:Callable):
        """Entry point"""
        self.callback_on_start = callback_on_start
        (session_path, session_token) = self.new_session_path()
        self.screen_cast_call(self.portal.CreateSession, self.on_create_session_response,
                options={ 'session_handle_token': session_token })

    def new_request_path(self):
        self.request_token_counter += 1
        token = 'u%d'%self.request_token_counter
        path = '/org/freedesktop/portal/desktop/request/%s/%s'%(self.sender_name, token)
        return (path, token)

    def new_session_path(self):
        self.session_token_counter += 1
        token = 'u%d'%self.session_token_counter
        path = '/org/freedesktop/portal/desktop/session/%s/%s'%(self.sender_name, token)
        return (path, token)

    def screen_cast_call(self, method:Callable, callback, *args, options={}):
        (request_path, request_token) = self.new_request_path()
        self.bus.add_signal_receiver(
            callback,
            'Response',
            self.request_iface,
            self.bus_name,
            request_path
        )
        options['handle_token'] = request_token
        method(*(args + (options, )),
            dbus_interface=self.screen_cast_iface)

    def play_pipewire_stream(self, node_id):
        empty_dict = dbus.Dictionary(signature="sv")
        fd_object = self.portal.OpenPipeWireRemote(self.session, empty_dict,
                                            dbus_interface=self.screen_cast_iface)
        fd = fd_object.take()
        self.callback_on_start(fd, node_id)

    def on_start_response(self, response, results):
        if response != 0:
            raise Exception("Failed to start: %s"%response)

        print(f"[{self.__class__.__name__}] streams:")
        for (node_id, stream_properties) in results['streams']:
            print("\tpipewire stream: {}".format(node_id))
            self.play_pipewire_stream(node_id)

    def on_select_sources_response(self, response, results):
        if response != 0:
            raise Exception(f"Failed to select sources: {response}")

        print(f"[{self.__class__.__name__}] sources selected")
        global session
        self.screen_cast_call(self.portal.Start, self.on_start_response, self.session, '')

    def on_create_session_response(self, response, results):
        if response != 0:
            raise Exception("Failed to create session: %d"%response)

        self.session = results['session_handle']
        print(f"[{self.__class__.__name__}] portal session created : {self.session}")

        self.screen_cast_call(self.portal.SelectSources, self.on_select_sources_response,
            self.session, options={
                'multiple': False, 'types': dbus.UInt32(1|2), 'cursor_mode': dbus.UInt32(settings.SC_CURSOR_MODE)
            })
