from .. import settings
from gi.repository import Gst

class StreamMan:
    def __init__(self, pipewire_fd, pipewire_node_id) -> None:
        Gst.init(None)
        self.pipeline = Gst.parse_launch(
            (
                'pipewiresrc fd={file} path={node_id} ! '
                'videorate ! video/x-raw,framerate={frate}/1 ! videoconvert ! '
                'jpegenc ! multifilesink location={out_file} max-files=1'
            ).format(
                file=pipewire_fd, node_id=pipewire_node_id,
                out_file=str(settings.GST_SHARED_FILE),
                frate=settings.GST_FRAME_RATE,
            )
        )
        self.pipeline.get_bus().connect('message', self._on_msg)

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)

    def _on_msg(self, message):
        type = message.type
        if type == Gst.MessageType.EOS or type == Gst.MessageType.ERROR:
            raise Exception(f"Gstreamer error : {message}")
