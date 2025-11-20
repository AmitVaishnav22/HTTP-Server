# HTTPS Python Server — README

This project demonstrates how to build a minimal asynchronous HTTPS server from scratch using Python's asyncio, sockets, and ssl modules. It is intended for learning and lightweight local use only.

## Features
- Asynchronous, non-blocking server using asyncio
- Serves static files (GET)
- Simple MIME type handling via mimetypes
- TLS/HTTPS support via Python's ssl module (self-signed cert for local testing)

## steps to build own http server from sratch
### 1. Create a TCP socket
  * Use socket.socket(AF_INET, SOCK_STREAM)
  * Bind to (host, port)
  * Start listening with listen()
### 2. Accept incoming client connections
  * Call accept() in a loop
  * This gives you:
    * client_socket
    * client_address
### 3. Receive raw HTTP data
  * Use client_socket.recv(1024)
  * This contains the HTTP request like: GET /index.html HTTP/1.1
  Host: localhost
### 4. Parse the HTTP request
  * Extract:
    * method → GET
    * uri → /index.html
    * version → HTTP/1.1
    * You only need to read the first line (request line).
### 5. Dispatch the request to handlers
  * Call correct handler based on method:
    * handle_GET()
    * handle_POST()
  * If unknown → return 501 Not Implemented.
### 6. Check if the requested file exists
  * Convert URL to filename
    * Example: /index.html → index.html
    * If file NOT found → return 404 Not Found
### 7. Read the file contents
  * Open file in binary mode
  * Read entire content
### 8. Build the HTTP response
  * Response :
    * Status Line,
    * Response Headers
    * (blank line)
    * Response Body
  * Example:
    * HTTP/1.1 200 OK
    * Content-Type: text/html
    * <html>...</html>
### 9. Send response to the client
  * Use client_socket.sendall(response_bytes)
### 10. Close the connection
  * For each request
  * Or keep alive (advanced)

## Requirements
- Python 3.8+
- OpenSSL (for creating a self-signed certificate) or Windows PowerShell capability to create certs
- No third-party Python packages required

## Project layout
```powershell
├── main.py          # example HTTPS server script
├── arch.png             # serving media
├── index.html         # example static file
└── README.md
```

## Example server (main.py)
Save this minimal script as `server.py` in the project root. It uses asyncio and ssl to accept HTTPS connections and serve files.

## Run the server
1. Ensure `cert.pem` and `key.pem` are in the project root (or pass paths via --cert/--key).
2. Run (Windows PowerShell / cmd):
```powershell
python server.py 
3. Open a browser to: https://localhost:8443
   - Browser will show a security warning for self-signed cert; accept to proceed for testing.

## Testing with curl
```powershell
curl -k https://localhost:8443/       # -k skips certificate verification
curl -k https://localhost:8443/index.html
```

## Notes & Limitations
- This server is educational and lacks production features:
  - No POST/PUT body parsing
  - No connection keep-alive handling
  - No HTTP/2
  - Minimal header parsing and validation
- For production use, use a proven web server (nginx, Caddy) or frameworks (uvicorn, aiohttp) and proper certificates from a CA.

## Troubleshooting
- "address already in use": pick another port or stop the process using the port.
- OpenSSL not found on Windows: install Git for Windows (includes OpenSSL), or create cert via PowerShell/private CA.

## Next steps / enhancements
- Add proper request parsing and routing
- Add persistent connection handling and request pipelining
- Add logging and configurable static root
- Use Let's Encrypt or system CA for valid certificates