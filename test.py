# main.py
import config
import hardware
import wifi_utils
import webserver
import time

def main():
    # 1) Inicializar hardware
    hardware.init_hardware()

    # 2) Iniciar Wi-Fi no modo AP (se quiser)
    ap = wifi_utils.start_access_point()  
    # ou, se quiser STA:
    # wlan = wifi_utils.connect_station()

    # 3) Subir servidor web
    webserver.start_server(port=80)

    # 4) Loop principal
    while True:
        # Verificar conexões HTTP
        webserver.check_for_connections()

        # Se quiser ler joystick, botões etc. no loop, pode fazer aqui:
        # x, y = hardware.read_joystick()
        # if hardware.is_btn_a_pressed():
        #     hardware.beep_a()

        time.sleep(0.1)

if __name__ == "__main__":
    main()

