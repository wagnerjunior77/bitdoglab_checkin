import network
import config
import time

def start_access_point():
    ssid = 'BitDogLab'
    password = '123456789'

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    timeout = 10  # Tenta conectar por 10 segundos
    while not ap.active() and timeout > 0:
        print(f"Aguardando ativação do AP... ({timeout}s restantes)")
        time.sleep(1)
        timeout -= 1

    if ap.active():
        print(f"✅ AP iniciado! IP: {ap.ifconfig()[0]}")
        return ap
    else:
        print("❌ Erro ao ativar o AP. Tentando novamente em 5s...")
        time.sleep(5)
        return start_access_point()  # Tenta novamente
