import uvicorn
from typing import Callable
from gi.repository import GObject, Gio, GLib

from .stream_route import STREAM_ROUTES, stream_route_handler
from .static_routes import static_route_handler
from .. import settings

async def server(scope:dict, receive:Callable, send:Callable):
    if scope['path'] in STREAM_ROUTES:
        await stream_route_handler(scope, receive, send)
    else:
        await static_route_handler(scope, receive, send)


class WebServer(GObject.Object):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback

    def start(self):
        task = Gio.Task.new(self, None, self.callback, None)
        task.set_return_on_cancel(False)
        task.run_in_thread(self._thread_callback)

    def _thread_callback(self, task, worker, task_data, cancellable):
        """Run the blocking operation in a worker thread."""
        print(f"[{self.__class__.__name__}] starting web server..")
        try:
            uvicorn.run(server, host="0.0.0.0", port=settings.PORT, backlog=10)
        except  Exception as exp:
            print(f"Error booting up web server : ", exp)
        task.return_error(GLib.Error())


def on_server_error(worker, result, handler_data):
    raise Exception(f"Error starting web server @ {settings.PORT}")

def start_server_in_gio_loop():
    server = WebServer(on_server_error)
    server.start()
