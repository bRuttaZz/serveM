from pathlib import Path

__dirname__ = Path(__file__).parent

PUBLIC_DIR_PATH = Path.joinpath(__dirname__, "public")
STATIC_FILE_CHUNK_SIZE = 1024
PORT = 8088

GST_FRAME_RATE = 10

GST_SHARED_FILE = Path("/tmp/servem_frame.jpg")


'''Available cursor modes :
    - ``1``: Hidden. The cursor is not part of the screen cast stream.
    - ``2``: Embedded: The cursor is embedded as part of the stream buffers.
    - ``4``: Metadata: The cursor is not part of the screen cast stream, but sent as PipeWire stream metadata.
'''
SC_CURSOR_MODE=2
