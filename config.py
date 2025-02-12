# config.py

# =========================================================
# PINOS DA BITDOGLAB (Exemplo adaptado do seu mapeamento)
# =========================================================

# LEDs
LED_R_PIN = 13
LED_G_PIN = 11
LED_B_PIN = 12

# Buzzers
BUZZER_A_PIN = 21
BUZZER_B_PIN = 10

# Botões
BTN_A_PIN = 5
BTN_B_PIN = 6
JOYSTICK_BTN_PIN = 22

# Joystick analógico (ADC)
# Observação: em MicroPython, precisamos chamar ADC(Pin(x)) 
# no pino físico GP26..28, mas não existe "adc_select_input()" 
# como no C. Vamos mapear o pino físico aqui:
JOYSTICK_X_PIN = 26  # canal ADC0
JOYSTICK_Y_PIN = 27  # canal ADC1
MIC_PIN         = 28  # canal ADC2 (exemplo)

# I2C (se quisermos usar)
I2C_SDA_PIN = 14
I2C_SCL_PIN = 15

I2C_FREQ = 400000  # 400kHz

# Se for usar Wi-Fi AP (Access Point):
AP_SSID     = 'MicroPython-AP'
AP_PASSWORD = '123456789'


