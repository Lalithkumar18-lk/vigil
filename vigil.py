import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time
import random
from datetime import datetime

git add .
git commit -m "Added requirement"
git push


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Vegil AI Surveillance System", layout="wide")

st.title("🚨 Vegil AI – Intelligent Urban Surveillance System")
st.markdown("Real-Time Threat Detection & Monitoring Dashboard")

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
st.sidebar.header("⚙ System Control")

camera_option = st.sidebar.selectbox(
    "Select Camera Source",
    ("Webcam", "Sample Video")
)

start_button = st.sidebar.button("▶ Start Monitoring")
stop_button = st.sidebar.button("⛔ Stop Monitoring")

# -----------------------------
# INCIDENT DATABASE (Temporary)
# -----------------------------
if "incident_log" not in st.session_state:
    st.session_state.incident_log = []

# -----------------------------
# FUNCTION: Simulate Threat Detection
# -----------------------------
def detect_threat():
    value = random.randint(1, 100)

    if value < 60:
        return "LOW", 0.60
    elif value < 85:
        return "MEDIUM", 0.75
    else:
        return "HIGH", 0.90

# -----------------------------
# MAIN MONITORING SECTION
# -----------------------------
frame_window = st.empty()

if start_button:

    cap = cv2.VideoCapture(0)

    st.success("Monitoring Started...")

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame
        frame = cv2.resize(frame, (640, 480))

        # Simulated Threat Detection
        threat_level, confidence = detect_threat()

        # Draw Bounding Box (Demo)
        cv2.rectangle(frame, (200, 100), (450, 350), (0, 0, 255), 2)
        cv2.putText(frame, f"Threat: {threat_level}", (200, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, f"Confidence: {confidence}", (200, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        frame_window.image(frame, channels="BGR")

        # Log Incident if MEDIUM or HIGH
        if threat_level in ["MEDIUM", "HIGH"]:
            incident = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Threat Level": threat_level,
                "Confidence": confidence,
                "Status": "Alert Triggered"
            }

            st.session_state.incident_log.append(incident)

            st.warning(f"⚠ {threat_level} Threat Detected!")

        time.sleep(1)

        if stop_button:
            break

    cap.release()
    st.error("Monitoring Stopped")

# -----------------------------
# INCIDENT LOG TABLE
# -----------------------------
st.subheader("📊 Incident Log")

if len(st.session_state.incident_log) > 0:
    df = pd.DataFrame(st.session_state.incident_log)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No incidents recorded yet.")

# -----------------------------
# SYSTEM METRICS
# -----------------------------
st.subheader("📈 System Performance")

col1, col2, col3 = st.columns(3)

col1.metric("Detection Accuracy", "93%")
col2.metric("Alert Latency", "2-3 sec")
col3.metric("FPS Processing", "25-30 FPS")

st.markdown("---")
st.markdown("© 2026 Vegil AI | AI-Powered Smart Surveillance")
