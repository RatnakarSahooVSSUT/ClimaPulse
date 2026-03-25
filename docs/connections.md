# 🔌 ClimaPulse Hardware Connections  
### 📡 Complete Wiring & Pin Configuration Guide (Raspberry Pi 4)

---

## 📌 Overview  

This document provides the **complete hardware connection details** for the **ClimaPulse Air Quality Monitoring System**, including all sensors, communication interfaces, and GPIO mappings.

The system integrates **multiple sensors, ADC, display, and control interfaces** using **I2C, UART, and GPIO protocols**, forming a robust embedded IoT architecture.

---

## 🧠 System Controller  

- **Raspberry Pi 4 Model B**

---

## 🔗 Communication Architecture  

| Interface | Components | GPIO Pins |
|----------|-----------|----------|
| I2C | BME280, ADS1115, OLED | GPIO2 (SDA), GPIO3 (SCL) |
| UART | PMS5003 | GPIO14 (TX), GPIO15 (RX) |
| UART (USB) | MH-Z19E CO2 Sensor | USB (ttyUSB0) |
| GPIO | Buttons, LEDs | Multiple pins |

---

## 🌫️ Particulate Matter Sensor (PMS5003)  

**Protocol:** UART  

| PMS5003 Pin | Raspberry Pi |
|------------|-------------|
| VCC | 5V |
| GND | GND |
| TX | GPIO15 (RX) |
| RX | GPIO14 (TX) |

---

## 🌬️ CO2 Sensor (MH-Z19E)  

**Protocol:** UART via USB  

| Sensor Pin | Raspberry Pi |
|-----------|-------------|
| VCC | 5V |
| GND | GND |
| TX/RX | USB to UART Adapter (ttyUSB0) |

---

## 🌡️ Environmental Sensor (BME280)  

**Protocol:** I2C  

| BME280 Pin | Raspberry Pi |
|-----------|-------------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO2 |
| SCL | GPIO3 |

---

## 📟 OLED Display (SSD1306)  

**Protocol:** I2C  

| OLED Pin | Raspberry Pi |
|---------|-------------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO2 |
| SCL | GPIO3 |

---

## ⚡ Analog-to-Digital Converter (ADS1115)  

**Protocol:** I2C  

| ADS1115 Pin | Raspberry Pi |
|------------|-------------|
| VDD | 3.3V |
| GND | GND |
| SDA | GPIO2 |
| SCL | GPIO3 |

---

## 🧪 Gas Sensors Interface  

**Connected via ADS1115 (Analog Inputs)**  

| Sensor | ADS1115 Channel |
|-------|----------------|
| MiCS-2714 (NO2) | A0 |
| MQ-7 (CO) | A1 |
| MQ-4 (CH4) | A2 |

### ⚠️ Signal Conditioning Required  
- Use **LM358 / NE5532 Op-Amps**  
- Implement **voltage divider circuits**  
- Ensure output is within **0–3.3V range**  

---

## 🔘 User Input (Buttons)  

| Function | GPIO Pin |
|--------|---------|
| Screen Control 1 | GPIO17 |
| Screen Control 2 | GPIO27 |
| Screen Control 3 | GPIO22 |
| Main System Button | GPIO23 |
| WiFi / IP Button | GPIO25 |

---

## 💡 Status Indicators  

| Component | GPIO Pin |
|----------|---------|
| Status LED | GPIO24 |
| System LED | GPIO26 |

---

## ⚡ Power Distribution  

| Component | Voltage |
|----------|--------|
| Raspberry Pi | 5V |
| PMS5003 | 5V |
| MH-Z19E | 5V |
| Gas Sensors | 5V |
| BME280 | 3.3V |
| OLED Display | 3.3V |
| ADS1115 | 3.3V |

---

## ⚠️ Design Considerations  

- 🚫 Do NOT connect 5V outputs directly to Raspberry Pi GPIO (3.3V logic only)  
- 🔌 Maintain **common ground across all components**  
- ⚡ Use **stable regulated power supply**  
- 🔍 Ensure proper **sensor calibration before deployment**  
- 📡 Keep wiring short to reduce noise  

---

## 🛠️ Setup Instructions  

### Enable Required Interfaces  
```
sudo raspi-config
```

- Enable **I2C**
- Enable **Serial (UART)**
- Disable serial console if required  

---

## ✅ System Validation Checklist  

- [ ] All sensors powered correctly  
- [ ] I2C devices detected (`i2cdetect -y 1`)  
- [ ] UART communication verified  
- [ ] OLED display functioning  
- [ ] ADC readings stable  
- [ ] Dashboard receiving data  

---

## 📈 System Insight  

This hardware architecture demonstrates:  
- Multi-protocol embedded system design  
- Real-time environmental sensing  
- Analog + digital signal integration  
- Scalable IoT deployment framework  

---

⭐ *This connection guide is derived directly from the working implementation of ClimaPulse and is optimized for reproducibility and deployment.*  
