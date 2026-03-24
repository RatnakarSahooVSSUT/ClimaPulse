import serial
import time
import math
import statistics
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_bme280 import basic as adafruit_bme280
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ssd1306
from datetime import datetime

# ================= FIREBASE =================
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/home/yesist12/env_ai_system/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

UPLOAD_INTERVAL = 15
last_upload_time = 0

# ================= LED =================
status_led = digitalio.DigitalInOut(board.D26)
status_led.direction = digitalio.Direction.OUTPUT

# ================= CONFIG =================
VCC = 5.0
RL = 10000.0
MEDIAN_WINDOW = 5
ALPHA = 0.2

NO2_M, NO2_B = -0.55, 0.05
CO_M, CO_B = -0.77, 0.34
CH4_A = 2.0
CH4_B = -3.7

WARMUP_TIME = 180
CAL_TIME = 60

# ================= SERIAL =================
pms = serial.Serial('/dev/serial0',9600,timeout=0.1)
co2_ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)

# ================= I2C =================
i2c = busio.I2C(board.SCL,board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,address=0x76)

ads = ADS1115(i2c)
ads.gain = 1

no2_chan = AnalogIn(ads,0)
co_chan = AnalogIn(ads,1)
ch4_chan = AnalogIn(ads,2)

# ================= OLED =================
WIDTH = 128
HEIGHT = 64
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH,HEIGHT,i2c)

image = Image.new("1",(WIDTH,HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# ================= BUTTONS =================
btn1 = digitalio.DigitalInOut(board.D17)
btn2 = digitalio.DigitalInOut(board.D27)
btn3 = digitalio.DigitalInOut(board.D22)

for b in [btn1,btn2,btn3]:
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP

current_screen = 1

last_btn1=True
last_btn2=True
last_btn3=True

last_press_time=0
DEBOUNCE=0.25

# ================= STORAGE =================
pm25_hist=[]
pm10_hist=[]
co2_hist=[]

pm25_ema=None
pm10_ema=None

co_ppm=0
no2_ppm=0
ch4_ppm=0

temp=0
hum=0
pres=0

co2=0
aqi=0

# ================= FILTERS =================

def median_filter(hist,val):
    hist.append(val)
    if len(hist)>MEDIAN_WINDOW:
        hist.pop(0)
    return statistics.median(hist)

def spike_filter(new,old,threshold=150):
    if old is None:
        return new
    if abs(new-old)>threshold:
        return old
    return new

def co2_filter(val):
    co2_hist.append(val)
    if len(co2_hist)>5:
        co2_hist.pop(0)
    return sum(co2_hist)/len(co2_hist)

def env_compensation(ppm,temp,hum):
    temp_factor=1+0.01*(temp-20)
    hum_factor=1+0.005*(hum-65)
    return ppm/(temp_factor*hum_factor)

# ================= GAS FUNCTIONS =================

def get_rs(voltage):
    if voltage<=0.01:
        voltage=0.01
    return RL*(VCC-voltage)/voltage

def compute_ppm(ratio,M,B):
    if ratio<=0:
        return 0
    return 10**((math.log10(ratio)-B)/M)

# ================= AQI =================

def aqi_pm25(c):
    table=[(0,30,0,50),(31,60,51,100),(61,90,101,200),
           (91,120,201,300),(121,250,301,400),(251,500,401,500)]
    for Cl,Ch,Il,Ih in table:
        if Cl<=c<=Ch:
            return int(((Ih-Il)/(Ch-Cl))*(c-Cl)+Il)
    return 500

def aqi_pm10(c):
    table=[(0,50,0,50),(51,100,51,100),(101,250,101,200),
           (251,350,201,300),(351,430,301,400),(431,600,401,500)]
    for Cl,Ch,Il,Ih in table:
        if Cl<=c<=Ch:
            return int(((Ih-Il)/(Ch-Cl))*(c-Cl)+Il)
    return 500

# ================= CO2 =================

def read_co2():
    co2_ser.reset_input_buffer()
    cmd=bytearray([0xFF,0x01,0x86,0,0,0,0,0,0x79])
    co2_ser.write(cmd)
    time.sleep(0.2)
    res=co2_ser.read(9)
    if len(res)==9 and res[0]==0xFF and res[1]==0x86:
        return res[2]*256+res[3]
    return None

# ================= WARMUP =================

for remaining in range(WARMUP_TIME,0,-1):

    status_led.value = not status_led.value

    draw.rectangle((0,0,WIDTH,HEIGHT),fill=0)

    draw.text((15,0),"SYSTEM START",font=font,fill=255)
    draw.text((10,18),"Sensors heating",font=font,fill=255)

    minutes=remaining//60
    seconds=remaining%60

    draw.text((40,36),f"{minutes:02}:{seconds:02}",font=font,fill=255)
    draw.text((20,52),"Please wait",font=font,fill=255)

    oled.image(image)
    oled.show()

    time.sleep(1)

status_led.value=True

# ================= CALIBRATION =================

def calibrate(channel,name):

    samples=[]
    start=time.time()

    while time.time()-start<CAL_TIME:

        draw.rectangle((0,0,WIDTH,HEIGHT),fill=0)

        draw.text((0,0),"CALIBRATING",font=font,fill=255)
        draw.text((0,16),f"{name} sensor",font=font,fill=255)

        remaining=int(CAL_TIME-(time.time()-start))

        draw.text((0,34),f"Time:{remaining}s",font=font,fill=255)

        oled.image(image)
        oled.show()

        samples.append(get_rs(channel.voltage))
        time.sleep(1)

    return sum(samples)/len(samples)

NO2_R0=calibrate(no2_chan,"NO2")
CO_R0=calibrate(co_chan,"CO")
CH4_R0=calibrate(ch4_chan,"CH4")

# ================= SENSOR TIMERS =================

last_pm_time=0
last_gas_time=0
last_env_time=0
last_co2_time=0

PM_INTERVAL=1
GAS_INTERVAL=2
ENV_INTERVAL=5
CO2_INTERVAL=3

# ================= MAIN LOOP =================

while True:

    now=time.monotonic()

    status_led.value=True

    # -------- BUTTON HANDLING --------

    if btn1.value == False and last_btn1:
        if now-last_press_time>DEBOUNCE:
            current_screen=1
            last_press_time=now

    if btn2.value == False and last_btn2:
        if now-last_press_time>DEBOUNCE:
            current_screen=2
            last_press_time=now

    if btn3.value == False and last_btn3:
        if now-last_press_time>DEBOUNCE:
            current_screen=3
            last_press_time=now

    last_btn1=btn1.value
    last_btn2=btn2.value
    last_btn3=btn3.value

    # -------- PM SENSOR --------

    if now-last_pm_time>PM_INTERVAL:

        last_pm_time=now

        try:

            b=pms.read(1)

            if b==b'\x42' and pms.read(1)==b'\x4d':

                frame=pms.read(30)

                if len(frame)==30:

                    data=b'\x42\x4d'+frame

                    raw_pm25=data[12]*256+data[13]
                    raw_pm10=data[14]*256+data[15]

                    m25=median_filter(pm25_hist,raw_pm25)
                    m10=median_filter(pm10_hist,raw_pm10)

                    m25=spike_filter(m25,pm25_ema)
                    m10=spike_filter(m10,pm10_ema)

                    if pm25_ema is None:
                        pm25_ema=m25
                        pm10_ema=m10
                    else:
                        pm25_ema=(1-ALPHA)*pm25_ema+ALPHA*m25
                        pm10_ema=(1-ALPHA)*pm10_ema+ALPHA*m10

                    aqi=max(aqi_pm25(pm25_ema),aqi_pm10(pm10_ema))

        except:
            pass

    # -------- GAS SENSOR --------

    if now-last_gas_time>GAS_INTERVAL:

        last_gas_time=now

        try:

            no2_rs=get_rs(no2_chan.voltage)
            co_rs=get_rs(co_chan.voltage)
            ch4_rs=get_rs(ch4_chan.voltage)

            no2_ppm=compute_ppm(no2_rs/NO2_R0,NO2_M,NO2_B)
            co_ppm=compute_ppm(co_rs/CO_R0,CO_M,CO_B)

            ch4_ratio=ch4_rs/CH4_R0
            ch4_ppm=CH4_A*pow(ch4_ratio,CH4_B)

            co_ppm=env_compensation(co_ppm,temp,hum)
            no2_ppm=env_compensation(no2_ppm,temp,hum)
            ch4_ppm=env_compensation(ch4_ppm,temp,hum)

        except:
            pass

    # -------- ENVIRONMENT --------

    if now-last_env_time>ENV_INTERVAL:

        last_env_time=now

        try:
            temp=bme280.temperature
            hum=bme280.humidity
            pres=bme280.pressure
        except:
            pass

    # -------- CO2 --------

    if now-last_co2_time>CO2_INTERVAL:

        last_co2_time=now

        val=read_co2()

        if val:
            co2=co2_filter(val)

    # -------- FIREBASE --------
    if now-last_upload_time>UPLOAD_INTERVAL:

        last_upload_time=now

        firebase_data={
            "pm25":float(pm25_ema) if pm25_ema else 0.0,
            "pm10":float(pm10_ema) if pm10_ema else 0.0,
            "co2":float(co2),
            "co":float(co_ppm),
            "ch4":float(ch4_ppm),
            "no2":float(no2_ppm),
            "temperature":float(temp),
            "humidity":float(hum),
            "pressure":float(pres),
            "aqi":float(aqi),
            "timestamp":datetime.utcnow()
        }

        try:
            db.collection("sensor_data").add(firebase_data)
        except:
            pass

    # -------- OLED --------

    draw.rectangle((0,0,WIDTH,HEIGHT),fill=0)

    if current_screen==1:

        draw.text((0,0),"AIR QUALITY",font=font,fill=255)
        draw.text((0,14),f"PM2.5:{round(pm25_ema,2) if pm25_ema else 0}",font=font,fill=255)
        draw.text((0,26),f"PM10:{round(pm10_ema,2) if pm10_ema else 0}",font=font,fill=255)
        draw.text((0,38),f"AQI:{aqi}",font=font,fill=255)

    elif current_screen==2:

        draw.text((0,0),"GAS LEVELS",font=font,fill=255)
        draw.text((0,14),f"CO2:{round(co2)} ppm",font=font,fill=255)
        draw.text((0,26),f"CO:{round(co_ppm,2)} ppm",font=font,fill=255)
        draw.text((0,38),f"CH4:{round(ch4_ppm,2)} ppm",font=font,fill=255)
        draw.text((0,50),f"NO2:{round(no2_ppm,3)} ppm",font=font,fill=255)

    elif current_screen==3:

        draw.text((0,0),"ENVIRONMENT",font=font,fill=255)
        draw.text((0,14),f"Temp:{round(temp,2)} oC",font=font,fill=255)
        draw.text((0,26),f"Hum:{round(hum,2)} %",font=font,fill=255)
        draw.text((0,38),f"Pres:{round(pres,2)} hPa",font=font,fill=255)

    oled.image(image)
    oled.show()

    time.sleep(0.01)