import asyncio
from .. import settings
from typing import Callable


STREAM_ROUTES = [
    "/stream",
    "/stream/"
]

async def stream_route_handler(scope:dict, receive:Callable, send:Callable):
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            (b"Content-Type", b"multipart/x-mixed-replace; boundary=--servemBoundary")
        ],
    })
    try:
        while True:
            if settings.GST_SHARED_FILE.exists():
                with open(settings.GST_SHARED_FILE, 'rb') as frame:
                    res = frame.read()
                    await send({
                        "type": "http.response.body",
                        "more_body": True,
                        "body": b"--servemBoundary\n" +
                            b"Content-Type: image/jpeg\n" +
                            f"Content-Length: {len(res)}\n\n".encode("utf-8") +
                            res +
                            b"\n\n"
                    })
            await asyncio.sleep(1/settings.GST_FRAME_RATE)
    except Exception as exp:
        ...
