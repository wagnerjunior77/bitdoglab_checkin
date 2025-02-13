import socket
import hardware
import time
import re

# 📝 Histórico de presença
presence_log = []
present_users = set()

# 📝 Página HTML enviada pelo servidor
def html_page():
    log_html = "".join(f"<li>{entry}</li>" for entry in presence_log[-5:])  # Mostra os últimos 5 registros
    status = f"Total de pessoas presentes: {len(present_users)}"
    
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>BitDogLab - Check-in</title>
  </head>
  <body>
    <h2>Registro de Presença</h2>
    <p>{status}</p>
    <form action="/" method="GET">
        <button name="user" value="Joao">João</button>
        <button name="user" value="Maria">Maria</button>
        <button name="user" value="Carlos">Carlos</button>
        <button name="user" value="Visitante">Visitante</button>
    </form>
    <form action="/" method="GET">
        <button name="clear" value="true">Limpar Histórico</button>
    </form>
    <h3>Histórico de Check-in</h3>
    <ul>{log_html}</ul>
  </body>
</html>"""

# 🔗 Variável global para armazenar o socket do servidor
_server_socket = None

# Função para extrair parâmetros apenas da linha do GET
def parse_query(get_line):
    params = {}
    partes = get_line.split(" ")
    if len(partes) < 2:
        return params
    caminho = partes[1]  # Exemplo: "/?user=Joao" ou "/?clear=true"
    if "?" in caminho:
        query_string = caminho.split("?", 1)[1]
        for par in query_string.split("&"):
            if "=" in par:
                key, value = par.split("=", 1)
                params[key] = value
    return params

# 🚀 Função para iniciar o servidor web
def start_server(port=80):
    global _server_socket
    _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Evita erro de porta ocupada
    _server_socket.bind(('', port))
    _server_socket.listen(5)
    print(f"🌐 Servidor web iniciado na porta {port}")

# 🛡️ Função que verifica conexões e processa requisições HTTP
def check_for_connections():
    global _server_socket
    try:
        conn, addr = _server_socket.accept()
        print(f"📩 Conexão recebida de {addr}")

        # Lê a requisição HTTP completa
        request = conn.recv(1024).decode()
        print(f"📝 Requisição recebida:\n{request}")

        # Utiliza somente a primeira linha (GET) para extrair os parâmetros
        get_line = request.split("\n")[0]
        params = parse_query(get_line)
        print("Parâmetros extraídos:", params)
        
        if params.get("clear") == "true":
            clear_log()
        elif "user" in params:
            user = params["user"].upper().strip()
            toggle_checkin(user)

        # Envia a resposta HTTP com a página
        response = html_page()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())
        conn.send(response.encode())
        conn.close()
    except OSError as e:
        print(f"⚠️ Erro na conexão: {e}")

# 💉 Função para alternar check-in/check-out do usuário
def toggle_checkin(user):
    global presence_log, present_users
    current_time = time.localtime()  # Retorna uma tupla (ano, mês, dia, hora, minuto, segundo, …)
    timestamp = "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])
    
    if user in present_users:
        present_users.remove(user)
        presence_log.append(f"{user} saiu às {timestamp}")
        print(f"📍 {user} saiu!")
    else:
        present_users.add(user)
        presence_log.append(f"{user} entrou às {timestamp}")
        print(f"📍 {user} entrou!")
    
    update_led_status()

# 📚 Função para limpar o histórico
def clear_log():
    global presence_log, present_users
    presence_log.clear()
    present_users.clear()
    print("📚 Histórico de presença limpo!")
    update_led_status()

# 💡 Atualiza o LED RGB conforme a presença de usuários
def update_led_status():
    if len(present_users) > 0:
        hardware.set_rgb_color(0, 65535, 0)  # Verde se houver pessoas presentes
    else:
        hardware.set_rgb_color(65535, 0, 0)   # Vermelho se ninguém estiver presente

