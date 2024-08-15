# as you got it already simply to send web files
import os
import io
from pathlib import Path
from typing import Callable
from ..settings import PUBLIC_DIR_PATH, STATIC_FILE_CHUNK_SIZE

EXTENSIONS = {
    "html": "text/html",
    "text": "text/plain",
    "css": "text/css",
    "js": "text/javascript",
    "xml": "text/xml",
    "csv": "text/csv",

    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "json": "appliction/json"
}

# a lazy file server
async def static_route_handler(scope:dict, receive:Callable, send:Callable):
    path = scope['path'].strip('/') or 'index.html'

    rel_path = Path.joinpath(PUBLIC_DIR_PATH, path)
    if not rel_path.exists():
        await send({
            "type": "http.response.start",
            "status": 404,
            "headers": [
                (b"Content-Type", b"text/plain"),
            ],
        })
        await send({
            "type": "http.response.body",
            "body": "Not Found".encode("utf-8"),
        })
        return

    type_ = str(path).split(".")[-1].lower()
    resp_mime = EXTENSIONS.get(type_, 'application/octet-stream')

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            (b"Content-Type", resp_mime.encode('utf-8'))
        ],
    })
    with open(rel_path, 'rb') as file:
        while True:
            chunk = file.read(STATIC_FILE_CHUNK_SIZE)
            if not chunk:
                await send({
                    "type": "http.response.body",
                    "body": b'',
                    "more_body": False
                })
                break
            await send({
                "type": "http.response.body",
                "body": chunk,
                "more_body": True
            })
        return
