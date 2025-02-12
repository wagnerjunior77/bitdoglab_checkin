# hardware.py
import config
from machine import Pin, PWM, ADC
import time

# Variáveis globais (PWM etc.)
led_r = None
led_g = None
led_b = None
buzzer_a_pwm = None
buzzer_b_pwm = None

# Joystick ADC
joystick_x_adc = None
joystick_y_adc = None
mic_adc        = None

def init_hardware():
    global led_r, led_g, led_b
    global buzzer_a_pwm, buzzer_b_pwm
    global joystick_x_adc, joystick_y_adc, mic_adc

    # =============================
    # 1) Configurar LEDs (PWM)
    # =============================
    led_r = PWM(Pin(config.LED_R_PIN))
    led_g = PWM(Pin(config.LED_G_PIN))
    led_b = PWM(Pin(config.LED_B_PIN))

    for led in (led_r, led_g, led_b):
        led.freq(1000)
        led.duty_u16(0)  
        # Em cátodo comum, duty=0 => 0% de "tensão", LED apagado.
        # Se quiser iniciar tudo desligado, use 0. 
        # Se preferir iniciar aceso, ponha 65535.

    # =============================
    # 2) Buzzers (também PWM) - se forem passivos
    # =============================
    buzzer_a_pwm = PWM(Pin(config.BUZZER_A_PIN))
    buzzer_a_pwm.duty_u16(0)  # começa desligado
    buzzer_a_pwm.freq(2000)

    buzzer_b_pwm = PWM(Pin(config.BUZZER_B_PIN))
    buzzer_b_pwm.duty_u16(0)
    buzzer_b_pwm.freq(2000)

    # =============================
    # 3) Botões (pull_up)
    # =============================
    Pin(config.BTN_A_PIN, Pin.IN, Pin.PULL_UP)
    Pin(config.BTN_B_PIN, Pin.IN, Pin.PULL_UP)
    Pin(config.JOYSTICK_BTN_PIN, Pin.IN, Pin.PULL_UP)

    # =============================
    # 4) Joystick e Microfone (ADC)
    # =============================
    joystick_x_adc = ADC(Pin(config.JOYSTICK_X_PIN))
    joystick_y_adc = ADC(Pin(config.JOYSTICK_Y_PIN))
    mic_adc        = ADC(Pin(config.MIC_PIN))

    # Se precisar, pode printar algo
    print("Hardware inicializado!")

def set_rgb_color(r, g, b):
    """
    Para cátodo comum, 0 => LED apagado e 65535 => LED aceso 100%.
    Então, se quiser vermelho máximo: set_rgb_color(65535, 0, 0).
    """
    led_r.duty_u16(r)
    led_g.duty_u16(g)
    led_b.duty_u16(b)


def beep_a(freq=1000, duty=32768, duration_ms=200):
    pass

def beep_b(freq=500, duty=32768, duration_ms=200):
    pass

def read_joystick():
    """
    Retorna tupla (x_val, y_val) de 0..65535
    """
    x_val = joystick_x_adc.read_u16()
    y_val = joystick_y_adc.read_u16()
    return (x_val, y_val)

def read_mic():
    return mic_adc.read_u16()

def is_btn_a_pressed():
    return Pin(config.BTN_A_PIN).value() == 0

def is_btn_b_pressed():
    return Pin(config.BTN_B_PIN).value() == 0

def is_joystick_btn_pressed():
    return Pin(config.JOYSTICK_BTN_PIN).value() == 0
