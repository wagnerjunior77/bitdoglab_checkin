import socket
import hardware

# 📄 Página HTML enviada pelo servidor
def html_page():
    return """<!DOCTYPE html>
    <html><head><meta charset="UTF-8"><title>BitDogLab - Check-in</title></head>
    <body>
        <h2>Registro de Presença</h2>
        <p>Selecione seu nome para fazer check-in/check-out:</p>
        <form action="/" method="GET">
            <button name="user" value="Joao">João</button>
            <button name="user" value="Maria">Maria</button>
            <button name="user" value="Carlos">Carlos</button>
            <button name="user" value="Visitante">Visitante</button>
        </form>
    </body>
    </html>"""

# 🔗 Variável global para armazenar o socket do servidor
_server_socket = None

# 🚀 Função para iniciar o servidor web
def start_server(port=80):
    global _server_socket
    _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Evita erro de porta ocupada
    _server_socket.bind(('', port))
    _server_socket.listen(5)
    print(f"🌐 Servidor web iniciado na porta {port}")

# 📡 Função que verifica conexões e processa requisições HTTP
def check_for_connections():
    global _server_socket
    try:
        conn, addr = _server_socket.accept()
        print(f"📩 Conexão recebida de {addr}")

        # Lê a requisição HTTP
        request = conn.recv(1024).decode()
        print(f"📜 Requisição recebida:\n{request}")

        # Processa os comandos dos botões enviados na URL
        if "user=" in request:
            user = request.split("user=")[1].split(" ")[0].split("&")[0]
            user = user.upper().strip()
            handle_checkin(user)

        # Envia a resposta HTTP com a página
        response = html_page()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())
        conn.send(response.encode())
        conn.close()
    except OSError as e:
        print(f"⚠️ Erro na conexão: {e}")

# 🖍 Função para processar check-in/check-out do usuário
def handle_checkin(user):
    print(f"📍 {user} fez check-in/check-out!")
    hardware.set_rgb_color(0, 65535, 0)  # Verde como confirmação

