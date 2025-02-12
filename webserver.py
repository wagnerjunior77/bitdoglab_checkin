import socket
import hardware

# 📄 Página HTML enviada pelo servidor
def html_page():
    return """<!DOCTYPE html>
    <html><head><meta charset="UTF-8"><title>BitDogLab</title></head>
    <body>
        <h2>Página de Controle</h2>
        <form action="/" method="GET">
            <button name="msg" value="VERMELHO">Vermelho</button>
            <button name="msg" value="VERDE">Verde</button>
            <button name="msg" value="AZUL">Azul</button>
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
        if "msg=" in request:
            msg = request.split("msg=")[1].split(" ")[0]
            msg = msg.upper().strip()
            handle_message(msg)

        # Envia a resposta HTTP com a página
        response = html_page()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())
        conn.send(response.encode())
        conn.close()

    except OSError as e:
        print(f"⚠️ Erro na conexão: {e}")

# 🎨 Função para mudar a cor do LED RGB conforme o comando recebido
def handle_message(msg):
    if msg == "VERMELHO":
        hardware.set_rgb_color(65535, 0, 0)   # Vermelho
    elif msg == "VERDE":
        hardware.set_rgb_color(0, 65535, 0)   # Verde
    elif msg == "AZUL":
        hardware.set_rgb_color(0, 0, 65535)   # Azul
    else:
        print(f"⚠️ Comando desconhecido: {msg}")
