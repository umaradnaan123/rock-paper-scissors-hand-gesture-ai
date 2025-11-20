# Rock Paper Scissors – Hand Gesture AI (OpenCV + Mediapipe)

A fast and responsive **Hand Gesture Controlled Rock-Paper-Scissors Game** built using:

- Mediapipe (Hand Tracking)
- OpenCV (Webcam & Drawing)
- Python

This project detects the number of fingers you show (Rock, Paper, Scissors) and plays against the computer in real time.

---

## 🎮 Demo

- Show **0 fingers** → Rock ✊  
- Show **2 fingers** → Scissors ✌️  
- Show **5 fingers** → Paper 🖐️  

The computer will immediately choose a random gesture and display the winner.

---

## 🚀 Features

✔ Real-time hand tracking  
✔ Fast detection using **model_complexity=0**  
✔ Smooth 30 FPS  
✔ Cooldown system to avoid multiple triggers  
✔ Accurate finger counting  
✔ Stable thumb detection  

---

## 📦 Installation

### 1️⃣ Create a virtual environment (recommended)

```bash
python -m venv rps_env
rps_env\Scripts\activate
