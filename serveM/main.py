import argparse
from . import settings
from . import __version__

class ServeM:
    loop = None
    stream_man = None

    def __init__(self) -> None:
        self.comp_check()
        from gi.repository import GLib
        from .screencast.portal import DesktopPortal
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
        from .screencast.stream_man import StreamMan
        from .server.server import start_server_in_gio_loop
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
        try:
            self.portal.start_screencast_request(self.on_stream_handler)
            self.loop.run()
            # TODO: has to improve the exception handling for callback defenitions
        except Exception as exp:
            print("\n[SERVM] {}".format(exp))
        except BaseException:
            print("\n[SERVM] ceasing..")
        finally:
            self.on_termination()

def parse_args():
    parser = argparse.ArgumentParser(
        prog="serveM",
        description="[%(prog)s {version}] "
        "A simple screen sharing server for modern GNU/LINUX desktops!".format(version=__version__),
        allow_abbrev=True,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    parser.add_argument(
        "-f",
        "--framerate",
        required=False,
        default=None,
        type=int,
        help="Specify Framerate. Defaults to 10fps",
    )
    parser.add_argument(
        "-p",
        "--port",
        required=False,
        type=int,
        default=None,
        help="Specify custom server port. Defaults to 8000",
    )
    parser.add_argument(
        "--cursor",
        required=False,
        action="store_true",
        default=False,
        help="If provided the cursor position will be captured as well",
    )
    args = parser.parse_args()

    return args, parser

def main():
    args, parser = parse_args()
    if args.framerate: settings.GST_FRAME_RATE = args.framerate
    if args.port : settings.PORT =  args.port
    if args.cursor: settings.SC_CURSOR_MODE = 2

    ServeM().run()
