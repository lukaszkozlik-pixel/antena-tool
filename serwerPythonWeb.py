import http.server
import ssl
import os

port = 8443
bind_address = "0.0.0.0"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print("Log: " + format % args)

httpd = http.server.HTTPServer((bind_address, port), MyHandler)

# Używamy PROTOCOL_TLS, który automatycznie wybierze najlepszą wspólną wersję
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

# Wyłączamy niektóre restrykcje, które mogą blokować handshake w Crostini
context.options |= ssl.OP_NO_SSLv2
context.options |= ssl.OP_NO_SSLv3

try:
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f"Serwer działa na https://0.0.0.0:{port}")
    httpd.serve_forever()
except Exception as e:
    print(f"Błąd krytyczny: {e}")