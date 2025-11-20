import asyncio
import os
import mimetypes
import threading
import socket

class TCPServer:
    host='127.0.0.1'
    port=8080
    def start_server(self):
        """Starts the TCP server."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            cann,addr=server_socket.accept()
            print(f"Connected by ${cann} ${addr}")
            client_thread = threading.Thread(
                target=self.handle_client, args=(cann,)
            )
            client_thread.daemon = True  # want to keep it until the system is running
            client_thread.start()
    def handle_client(self,conn):
        print("Client connected",conn)
        try:
            data = conn.recv(1024)
            print("Received data:", data)
            if not data:
                conn.close()
                return
            response = self.handle_request(data)
            conn.sendall(response)
        except Exception as e:  
            print("Error handling client:", e)
        finally:
            conn.close()

        # print("Starting server...")
        # print(self.host,self.port,self.handle_client)
        # server= await asyncio.start_server(self.handle_client, self.host, self.port)
        # print(f"Server listening on {self.host}:{self.port}")
        # async with server:
        #     await server.serve_forever()

    async def handle_clientt(self, reader, writer):
        print("Client connected",reader,writer)
        try:
            data = await reader.read(1024)
            print("Received data:", data)
            if not data:
                writer.close()
                await writer.wait_closed()
                return
            response = self.handle_request(data)
            writer.write(response)
            await writer.drain()
        except Exception as e:  
            print("Error handling client:", e)
        finally:
            writer.close()
            await writer.wait_closed()
        

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
    asyncio.run(server.start_server())