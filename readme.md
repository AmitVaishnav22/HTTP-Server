# HTTPS Python Server — README

This project demonstrates how to build a minimal asynchronous HTTPS server from scratch using Python's asyncio, sockets, and ssl modules. It is intended for learning and lightweight local use only.

## Features
- Asynchronous, non-blocking server using asyncio
- Serves static files (GET)
- Simple MIME type handling via mimetypes
- TLS/HTTPS support via Python's ssl module (self-signed cert for local testing)

## Requirements
- Python 3.8+
- OpenSSL (for creating a self-signed certificate) or Windows PowerShell capability to create certs
- No third-party Python packages required

## Project layout
.
├── main.py          # example HTTPS server script
├── arch.png             # serving media
├── index.html         # example static file
└── README.md

## Generate a self-signed certificate (OpenSSL)
Open a terminal (Git Bash or Windows with OpenSSL installed) and run:
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```
This produces `cert.pem` and `key.pem`. Move them to the project root or `certs/` folder.

(If you prefer PowerShell and Windows cert store or .pfx, you can generate alternatives — the server example below uses PEM files.)

## Example server (main.py)
Save this minimal script as `server.py` in the project root. It uses asyncio and ssl to accept HTTPS connections and serve files.

## Run the server
1. Ensure `cert.pem` and `key.pem` are in the project root (or pass paths via --cert/--key).
2. Run (Windows PowerShell / cmd):
```powershell
python server.py --port 8443 --cert cert.pem --key key.pem
```
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
  - Uses self-signed certificates for local testing only
- For production use, use a proven web server (nginx, Caddy) or frameworks (uvicorn, aiohttp) and proper certificates from a CA.

## Troubleshooting
- "address already in use": pick another port or stop the process using the port.
- OpenSSL not found on Windows: install Git for Windows (includes OpenSSL), or install OpenSSL separately, or create cert via PowerShell/private CA.

## Next steps / enhancements
- Add proper request parsing and routing
- Add persistent connection handling and request pipelining
- Add logging and configurable static root
- Use Let's Encrypt or system CA for valid certificates