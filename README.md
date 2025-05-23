# 🛡️ TFLite Pi Security Cam with Discord Alerts

A lightweight security camera using TensorFlow Lite and a Raspberry Pi 5, AI Module, and camera that sends Discord alerts when a person is detected for more than 2 seconds. Designed for DIY home security and automation.

---

## 🚀 Features
- Real-time person detection with TFLite (SSD MobileNet)
- Sends image snapshots to Discord via webhook
- Buffered detection to avoid false positives
- Live annotated OpenCV feed
- Runs on Raspberry Pi 5 with Picamera2

---

## 📸 Hardware Requirements
- Raspberry Pi 4 (or 3B+) I am using 5 but for other reason
- Pi Camera Module (v2+)
- Internet access for Discord webhook

---
## Required Libraries
- tflite-runtime
- numpy
- requests
- opencv-python
- picamera2

```bash
pip install tflite-runtime numpy requests opencv-python
sudo apt install python3-picamera2
```
---

## 🧪 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/tflite-pi-security-cam.git
cd tflite-pi-security-cam
```
## 2. Install Dependencies

``` bash
sudo apt update
sudo apt install python3-picamera2 libatlas-base-dev python3-opencv
pip install -r requirements.txt
```
### 3. Add Your Discord Webhook
Create config.json:

```json
{
  "webhook_url": "https://discord.com/api/webhooks/XXXX/XXXXX"
}
```
### 4. 🧠 Run the Camera
```bash
python3 security_camera.py
```
Press q to quit.

## 🔧 Files Overview
* security_camera.py: Main detection script with buffer logic + live feed
* notify_discord.py: Uploads images to Discord using webhook
* config.json: Stores your webhook config
* test_notify.py: Sends a test image to Discord
* models/: Place your .tflite model here
  * already has an example model and labels
  
##🛡️ License
[MIT License](LICENSE)





