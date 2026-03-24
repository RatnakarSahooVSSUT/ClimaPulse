import RPi.GPIO as GPIO
import time
import os
import subprocess
import socket
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

BUTTON_PIN = 23          # main control button
WIFI_BUTTON_PIN = 25      # wifi/ip display button
LED_PIN = 24
LONG_PRESS_TIME = 3.0
SERVICE_NAME = "airquality.service"

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(WIFI_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

WIDTH = 128
HEIGHT = 64

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

button_pressed = False
press_start_time = 0
long_press_triggered = False
shutdown_triggered = False
last_countdown_value = -1

wifi_button_last = GPIO.HIGH
wifi_screen_active = False
wifi_debounce_time = 0
WIFI_DEBOUNCE = 0.25

def show_oled(line1="", line2="", line3="", line4=""):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=0)
    draw.text((0, 0), line1, font=font, fill=255)
    draw.text((0, 16), line2, font=font, fill=255)
    draw.text((0, 32), line3, font=font, fill=255)
    draw.text((0, 48), line4, font=font, fill=255)
    oled.image(image)
    oled.show()

def clear_oled():
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=0)
    oled.image(image)
    oled.show()
    oled.fill(0)
    oled.show()

def led_on():
    GPIO.output(LED_PIN, GPIO.HIGH)

def led_off():
    GPIO.output(LED_PIN, GPIO.LOW)

def is_service_running():
    result = subprocess.run(
        ["systemctl", "is-active", SERVICE_NAME],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() == "active"

def update_led_state():
    if is_service_running():
        led_on()
    else:
        led_off()

def run_systemctl(action):
    return subprocess.run(
        ["sudo", "systemctl", action, SERVICE_NAME],
        capture_output=True,
        text=True
    )

def get_wifi_name():
    result = subprocess.run(
        ["iwgetid", "-r"],
        capture_output=True,
        text=True
    )
    ssid = result.stdout.strip()
    return ssid if ssid else None

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def show_ready_screen():
    show_oled("AIR NODE", "READY", "Press button", "WiFi/IP allowed ")

def show_wifi_screen():
    ssid = get_wifi_name()
    ip = get_ip_address()

    if ssid and ip:
        show_oled("NETWORK", f"WiFi:{ssid[:12]}", f"IP:{ip}", "Press to exit")
    elif ip:
        show_oled("NETWORK", "WiFi:Connected", f"IP:{ip}", "Press to exit")
    else:
        show_oled("NETWORK", "WiFi:Not Conn.", "IP: --", "Press to exit")

def start_service():
    global wifi_screen_active
    wifi_screen_active = False

    show_oled("SYSTEM", "Starting service", "", "Please wait...")
    print("Starting service...")
    result = run_systemctl("start")
    time.sleep(1.0)

    if is_service_running():
        led_on()
        show_oled("SYSTEM", "STATUS: ON", "Service running", "")
        print("SYSTEM ON")
        time.sleep(1.2)
        return True
    else:
        led_off()
        err = result.stderr.strip() or result.stdout.strip() or "Unknown error"
        print(f"START FAILED: {err}")
        show_oled("ERROR", "Start failed", "", err[:20])
        time.sleep(2.5)
        show_ready_screen()
        return False
    
def stop_service():
    global wifi_screen_active
    wifi_screen_active = False

    show_oled("SYSTEM", "Stopping service", "", "Please wait...")
    print("Stopping service...")
    result = run_systemctl("stop")
    time.sleep(0.8)

    if not is_service_running():
        led_off()
        show_oled("SYSTEM", "STATUS: OFF", "Service stopped", "")
        print("SYSTEM OFF")
        time.sleep(1.5)
        show_ready_screen()
        return True
    else:
        led_on()
        err = result.stderr.strip() or result.stdout.strip() or "Unknown error"
        print(f"STOP FAILED: {err}")
        show_oled("ERROR", "Stop failed", "", err[:20])
        time.sleep(2.5)
        update_led_state()
        return False

def show_shutdown_hold_countdown(remaining):
    show_oled("SYSTEM", "Hold to shutdown", f"Shutdown in: {remaining}", "")

print("Button controller started")
print("Short press -> ON/OFF")
print("Hold 3 sec  -> SHUTDOWN")
print("WiFi button -> show IP when service is OFF")

update_led_state()

if is_service_running():
    show_oled("SYSTEM", "Already ON", "Service running", "")
else:
    show_ready_screen()

try:
    while True:
        if shutdown_triggered:
            time.sleep(0.1)
            continue

        service_running = is_service_running()

        # -------- WIFI BUTTON --------
        wifi_now = GPIO.input(WIFI_BUTTON_PIN)
        now_time = time.time()

        if not service_running:
            if wifi_now == GPIO.LOW and wifi_button_last == GPIO.HIGH:
                if now_time - wifi_debounce_time > WIFI_DEBOUNCE:
                    wifi_debounce_time = now_time
                    wifi_screen_active = not wifi_screen_active

                    if wifi_screen_active:
                        show_wifi_screen()
                    else:
                        show_ready_screen()

        wifi_button_last = wifi_now
        
        # -------- MAIN CONTROL BUTTON --------
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            if not button_pressed:
                button_pressed = True
                press_start_time = time.time()
                long_press_triggered = False
                last_countdown_value = 3
                wifi_screen_active = False
                show_shutdown_hold_countdown(3)

            else:
                elapsed = time.time() - press_start_time
                remaining = max(1, int(LONG_PRESS_TIME - elapsed) + 1)

                if remaining != last_countdown_value and not long_press_triggered:
                    last_countdown_value = remaining
                    if elapsed < LONG_PRESS_TIME:
                        show_shutdown_hold_countdown(remaining)

                if not long_press_triggered and elapsed >= LONG_PRESS_TIME:
                    print("SHUTDOWN TRIGGERED")
                    long_press_triggered = True
                    shutdown_triggered = True
                    wifi_screen_active = False

                    if service_running:
                        show_oled("SYSTEM", "Stopping service", "for shutdown...", "")
                        run_systemctl("stop")
                        time.sleep(0.8)

                    for sec in [3, 2, 1]:
                        show_oled("SYSTEM", "SHUTTING DOWN", f"In {sec} sec", "")
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        time.sleep(0.25)
                        GPIO.output(LED_PIN, GPIO.LOW)
                        time.sleep(0.25)
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        time.sleep(0.25)
                        GPIO.output(LED_PIN, GPIO.LOW)
                        time.sleep(0.25)

                    clear_oled()
                    time.sleep(0.2)
                    os.system("sudo shutdown -h now")

        else:
            if button_pressed:
                if not long_press_triggered:
                    if service_running:
                        stop_service()
                    else:
                        start_service()

                button_pressed = False
                press_start_time = 0
                long_press_triggered = False
                last_countdown_value = -1

                if not shutdown_triggered and not is_service_running() and not wifi_screen_active:
                    show_ready_screen()

        update_led_state()
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    clear_oled()
    led_off()
    GPIO.cleanup()
