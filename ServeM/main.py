import os
import settings

class ServeM:
    loop = None
    stream_man = None

    def __init__(self) -> None:
        self.comp_check()
        from gi.repository import GLib
        from screencast.portal import DesktopPortal
        self.loop = GLib.MainLoop()
        self.portal = DesktopPortal()


    def comp_check(self):
        import gi
        try:
            gi.require_version('Gst', '1.0')
        except Exception as exp:
            raise Exception((
                "Seemslike you missing some libraries to start with. "
                "Consider installing 'gstreamer1.0' and libraries"
            ))

    def on_stream_handler(self, pipewire_fd, pipewire_noed_id):
        from screencast.stream_man import StreamMan
        from server.server import start_server_in_gio_loop
        self.stream_man = StreamMan(pipewire_fd, pipewire_noed_id)
        self.stream_man.start()
        # and finally starting the server
        start_server_in_gio_loop()

    def on_termination(self):
        if self.stream_man: self.stream_man.stop()
        if self.loop : self.loop.quit()
        settings.GST_SHARED_FILE.unlink(missing_ok=True)

    def run(self):
        """And the entry point"""
        self.portal.start_screencast_request(self.on_stream_handler)
        try:
            self.loop.run()
        except Exception as exp:
            print("\n[SERVM] {}".format(exp))
        except BaseException:
            print("\n[SERVM] ceasing..")
        finally:
            self.on_termination()

def main():
    ServeM().run()

if __name__=="__main__":
    ServeM().run()
