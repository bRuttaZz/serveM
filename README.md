




Okay im running out of time _> starting with a quart server (for extensibility, may be customize its handlers for doing some custom functionaily)
anyway i may want send some random web content files as well.. so I want a framework

change of thoughts -> goind with a simple asgi server


```txt
HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace; boundary=--myboundary

--myboundary
Content-Type: image/jpeg
Content-Length: [length]

[JPEG data]

--myboundary
Content-Type: image/jpeg
Content-Length: [length]

[JPEG data]

--myboundary--

```
