import socket
import os
import mimetypes

class TCPServer:
    host='127.0.0.1'
    port=8080
    def start_server(self):
        # Create a TCP socket
        # AF_INET for IPv4, SOCK_STREAM for TCP 
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Bind the socket to the address and port
        s.bind((self.host,self.port))
        # Listen for incoming connections
        s.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            cann,addr=s.accept()
            print(f"Connected by ${cann} ${addr}")

            data=cann.recv(1024)
            if not data:
                break
            response=self.handle_request(data)
            print("Received:", response)
            cann.sendall(response)  # Echo back the received data
            cann.close()

class HTTPServer(TCPServer):
    rheaders = {
        'Server': 'HttpServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented'
    }

    def handle_request(self, data):
        """Handles the incoming request.
           Compiles and returns the response
        """

        request = HTTPRequest(data)
        print("request:", request)
        print(request.__dict__)
        print(end="\n")
        print(f"Handling {request.method} request for {request.uri} {request}")
        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        return handler(request)

    def handle_404(self, request):
        """Handles not found errors."""
        response_line = self.response_line(status_code=404)

        response_headers = self.response_headers()

        blank_line = b"\r\n"

        response_body = b"""<html>
            <body>
            <h1>404 Not Found</h1>
            <body>
            </html>
        """
        return b"".join([response_line, response_headers, blank_line, response_body])

    def HTTP_501_handler(self, request):
        """Handles unimplemented methods."""
        response_line = self.response_line(status_code=501)

        response_headers = self.response_headers()

        blank_line = b"\r\n"

        response_body = b"""<html>
            <body>
            <h1>501 Not Implemented</h1>
            <body>
            </html>
        """
        return b"".join([response_line, response_headers, blank_line, response_body])
        
    def handle_GET(self, request):
        """Handles GET requests."""
        filename = request.uri.strip('/')
        print("Filename:", filename)

        if os.path.isfile(filename):
            response_line = self.response_line(status_code=200)
            content_type = mimetypes.guess_type(filename)[0] or 'text/html'

            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)
            with open(filename, 'rb') as f:
                response_body = f.read()
            blank_line = b"\r\n"
            return b"".join([response_line, response_headers, blank_line, response_body])
        else:
            return self.handle_404(request)
    


        # response_line = self.response_line(status_code=200)

        # response_headers = self.response_headers()

        # blank_line = b"\r\n"

        # response_body = b"""<html>
        #     <body>
        #     <h1>Request received!</h1>
        #     <body>
        #     </html>
        # """
        # return b"".join([response_line, blank_line, response_body])
    
    def response_line(self, status_code):
        """Generates the response line."""
        reason_phrase = self.status_codes.get(status_code, 'Unknown Status')
        return f"HTTP/1.1 {status_code} {reason_phrase}\r\n".encode()
    
    def response_headers(self,extra_headers=None):
        """Generates the response headers."""
        if extra_headers:
            self.rheaders.update(extra_headers)
        headers = ""
        for header, value in self.rheaders.items():
            headers += f"{header}: {value}\r\n"
        return headers.encode()

class HTTPRequest:
    def __init__(self,data):
        self.method=None
        self.uri=None
        self.version="HTTP/1.1"
        self.parse(data)

    def parse(self,data):
        text = data.decode("utf-8", errors="ignore")
        request_line = text.split("\r\n")[0]
        words = request_line.split(" ")
        self.method = words[0]
        if len(words) > 1:
            self.uri = words[1]
        if len(words) > 2:
            self.version = words[2]

if __name__ == "__main__":
    server=HTTPServer()
    server.start_server()