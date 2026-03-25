# 🌍 ClimaPulse: Smart Outdoor Air Quality Monitoring System  
### 🚀 Real-Time Environmental Surveillance using IoT & Multi-Sensor Embedded System  

![IoT](https://img.shields.io/badge/Domain-IoT-blue)
![Embedded](https://img.shields.io/badge/Embedded-Raspberry%20Pi-green)
![Sensors](https://img.shields.io/badge/Sensors-Multi--Sensor%20Array-orange)
![AQI](https://img.shields.io/badge/Monitoring-AQI%20%7C%20Gases-purple)
![Dashboard](https://img.shields.io/badge/Dashboard-Web%20Based-yellow)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Focus](https://img.shields.io/badge/Focus-Smart%20City%20%7C%20Environment-red)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

---

## 📌 Overview  

**ClimaPulse** is a **compact, intelligent IoT-based outdoor air quality monitoring system** designed for **real-time environmental surveillance and pollution analysis**. It enables continuous monitoring of **critical atmospheric parameters and harmful pollutants**, combining **embedded systems, multi-sensor integration, and cloud connectivity**.

Built on a **Raspberry Pi 4 platform**, the system provides **both local visualization and remote dashboard monitoring**, making it suitable for **smart cities, industrial zones, and research applications**.

---

## 🎯 Key Highlights  

- 🌫️ Real-time **Air Quality Index (AQI) monitoring**  
- 🌬️ Multi-parameter sensing (PM, gases, temperature, humidity, pressure)  
- 📊 Live **web dashboard visualization**  
- 📟 Local **OLED display for field monitoring**  
- 📡 IoT-enabled remote data access  
- 🔘 User interaction via buttons & indicators  
- 🔧 Modular, portable, and scalable design  
- 🌍 Supports **smart-city and environmental analytics use-cases**  

---

## 🧠 System Architecture  

```
Sensors → Signal Acquisition → Raspberry Pi → Data Processing → OLED Display
                                             ↓
                                      IoT Dashboard (Web)
```

---

## ⚙️ Parameters Monitored  

| Category | Parameters |
|--------|-----------|
| Particulate Matter | PM2.5, PM10 |
| Gases | CO2, CO (equivalent), NO2 (equivalent), CH4 (equivalent) |
| Environment | Temperature, Humidity, Pressure |
| Index | AQI (Air Quality Index) |

---

## 🛠️ Hardware Components  

- Raspberry Pi 4 Model B  
- PMS5003 (PM2.5 / PM10 Sensor)  
- MH-Z19E (CO2 Sensor)  
- MQ-4 (Methane Sensor)  
- MQ-7 (Carbon Monoxide Sensor)  
- MiCS-2714 (NO2 Sensor)  
- BME280 (Temp, Humidity, Pressure)  
- OLED Display Module  
- Push Buttons & Status Indicators  
- Power Supply  

---

## 💻 Software & Technologies  

- **Programming:** Python  
- **Communication Protocols:** UART, I2C, GPIO  
- **Data Processing:** Real-time sensor fusion  
- **Frontend:** Web Dashboard (IoT Interface)  
- **Cloud Integration:** Remote monitoring & storage  

---

## 🔌 Working Principle  

- Multiple sensors continuously capture **pollution and environmental data**  
- Raspberry Pi performs **real-time data acquisition and processing**  
- AQI is computed based on collected parameters  
- Data is displayed locally via **OLED screen**  
- Simultaneously transmitted to **web dashboard for remote monitoring**  
- Enables **trend analysis and environmental comparison across locations**  

---

## 📊 System Features  

| Feature | Description |
|--------|------------|
| Real-Time Monitoring | Continuous environmental data capture |
| Multi-Sensor Fusion | Combined analysis of gases + particles |
| Local Display | Instant on-device feedback |
| Remote Dashboard | Web-based visualization |
| Portability | Easy deployment across locations |
| Scalability | Extendable for larger networks |

---

## 🌍 Applications  

- Smart city environmental monitoring  
- Industrial pollution tracking  
- Traffic junction air quality analysis  
- Campus & institutional monitoring  
- Roadside pollution assessment  
- Public health & environmental research  

---

## 🚧 Engineering Challenges  

- ⚠️ Sensor calibration and accuracy alignment  
- ⚠️ Handling noisy gas sensor outputs  
- ⚠️ Real-time multi-sensor data synchronization  
- ⚠️ Reliable IoT data transmission  

---

## ✅ Solutions Implemented  

- ✔️ Sensor fusion for improved accuracy  
- ✔️ Calibration strategies for gas sensors  
- ✔️ Efficient data acquisition pipeline  
- ✔️ Stable web-based visualization system  

---

## 📸 Results  

✔️ Accurate real-time air quality monitoring  
✔️ Functional IoT dashboard for remote access  
✔️ Stable multi-sensor integration  
✔️ Portable and field-deployable prototype  

---

## 📚 Learning Outcomes  

- IoT system design and deployment  
- Multi-sensor interfacing and calibration  
- Environmental data analysis  
- Embedded Linux (Raspberry Pi)  
- Real-time data visualization  
- System-level hardware-software integration  

---

## 🔮 Future Scope  

- 🤖 AI/ML-based pollution prediction  
- 📱 Mobile app integration  
- 📡 Distributed sensor network deployment  
- ☁️ Advanced cloud analytics  
- 📊 Historical trend forecasting  

---

## 🌱 SDG Alignment  

Aligned with United Nations Sustainable Development Goals:  
- **SDG 3:** Good Health & Well-being  
- **SDG 9:** Industry, Innovation & Infrastructure  
- **SDG 11:** Sustainable Cities & Communities  
- **SDG 13:** Climate Action  

---

## 👨‍💻 Team  

- **Ratnakar Sahoo**  
- Priyadarshani Mahapatra  
- Sohan Kumar Nayak  

Department of Electronics & Telecommunication Engineering  
Veer Surendra Sai University of Technology (VSSUT), Burla  

---

## 🎓 Mentors  

- Prof. Harish Kumar Sahoo  
- Dr. Aditya Kumar Hota  

---

## ⭐ Portfolio Description (For Resume / LinkedIn)  

**ClimaPulse: IoT-Based Outdoor Air Quality Monitoring System**  
Developed a real-time environmental monitoring system using Raspberry Pi and multi-sensor integration to measure AQI, particulate matter, and gas concentrations. Implemented sensor fusion, embedded data processing, and a web-based dashboard for remote visualization. Designed a scalable and portable solution for smart-city and pollution monitoring applications, demonstrating strong expertise in IoT, embedded systems, and environmental sensing.

---

## 📜 License  

This project is intended for **academic and research purposes**.  
Use and modify with proper attribution.  

---

## 🤝 Contributions  

Contributions and improvements are welcome!  
Feel free to fork and submit a pull request.  

---

⭐ *If you find this project impactful, consider starring the repository!*  
