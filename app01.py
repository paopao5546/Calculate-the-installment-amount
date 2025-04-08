# app.py
import streamlit as st
import qrcode
from io import BytesIO
import base64
import socket
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ตั้งค่าหน้าเพจ
st.set_page_config(
    page_title="เครื่องคำนวณ BMI",
    page_icon="🏋️",
    layout="centered"
)

# ฟังก์ชันสำหรับคำนวณ BMI
def calculate_bmi(weight, height):
    """คำนวณค่า BMI จากน้ำหนักและส่วนสูง"""
    # แปลงส่วนสูงจากเซนติเมตรเป็นเมตร
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

# ฟังก์ชันสำหรับหาหมวดหมู่ BMI
def get_bmi_category(bmi):
    """ส่งคืนหมวดหมู่ของ BMI และคำแนะนำ"""
    if bmi < 18.5:
        return "น้ำหนักน้อย / ผอม", "คุณควรทานอาหารให้เพียงพอและออกกำลังกายเพื่อเพิ่มมวลกล้ามเนื้อ", "#3498db"
    elif bmi < 23:
        return "น้ำหนักปกติ / สุขภาพดี", "คุณมีน้ำหนักที่เหมาะสม พยายามรักษาสุขภาพต่อไป", "#2ecc71"
    elif bmi < 25:
        return "น้ำหนักเกิน", "คุณควรควบคุมอาหารและออกกำลังกายสม่ำเสมอ", "#f39c12"
    elif bmi < 30:
        return "อ้วน / โรคอ้วนระดับ 1", "คุณควรปรับเปลี่ยนพฤติกรรมการกินและเพิ่มการออกกำลังกาย", "#e74c3c"
    else:
        return "อ้วนมาก / โรคอ้วนระดับ 2", "คุณควรพบแพทย์เพื่อรับคำแนะนำในการลดน้ำหนักอย่างปลอดภัย", "#c0392b"

# ฟังก์ชันสำหรับรับ IP Address ของเครื่อง
def get_local_ip():
    """รับ IP Address ของเครื่อง"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# ฟังก์ชันสำหรับสร้าง QR Code
def generate_qr_code(data):
    """สร้าง QR Code จากข้อมูล"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# ฟังก์ชันสำหรับสร้างแผนภูมิ BMI
def create_bmi_chart():
    categories = ['น้ำหนักน้อย', 'ปกติ', 'น้ำหนักเกิน', 'อ้วน', 'อ้วนมาก']
    ranges = ['< 18.5', '18.5-22.9', '23-24.9', '25-29.9', '≥ 30']
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#c0392b']
    
    fig, ax = plt.subplots(figsize=(10, 2))
    width = 0.2
    x = np.arange(len(categories))
    
    ax.bar(x, [1, 1, 1, 1, 1], width, color=colors)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{cat}\n{rng}" for cat, rng in zip(categories, ranges)])
    ax.set_yticks([])
    ax.set_title('เกณฑ์ BMI สำหรับคนเอเชีย')
    
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    return fig

# ส่วนหัวของเว็บไซต์
st.title("🏋️ เครื่องคำนวณดัชนีมวลกาย (BMI)")
st.markdown("**ประเมินสัดส่วนร่างกายของคุณอย่างง่ายดาย**")
st.write("---")

# สร้างเลย์เอาต์คอลัมน์
col1, col2 = st.columns([2, 1])

# คอลัมน์ซ้ายสำหรับฟอร์ม
with col1:
    st.subheader("กรอกข้อมูลของคุณ")
    
    with st.form("bmi_calculator_form"):
        weight = st.number_input("น้ำหนัก (กิโลกรัม)", min_value=1.0, max_value=300.0, step=0.1)
        height = st.number_input("ส่วนสูง (เซนติเมตร)", min_value=1.0, max_value=300.0, step=0.1)
        
        submitted = st.form_submit_button("คำนวณ BMI")

# คอลัมน์ขวาสำหรับ QR Code
with col2:
    st.subheader("แชร์แอพนี้")
    local_ip = get_local_ip()
    port = 8501  # Streamlit default port
    website_url = f"http://{local_ip}:{port}"
    
    qr_code = generate_qr_code(website_url)
    st.markdown(f'<img src="data:image/png;base64,{qr_code}" alt="QR Code" style="width:100%;max-width:200px;">', unsafe_allow_html=True)
    st.markdown(f"**URL:** [{website_url}]({website_url})")

# แสดงผลลัพธ์ BMI ถ้ามีการส่งฟอร์ม
if submitted:
    bmi = calculate_bmi(weight, height)
    category, advice, color = get_bmi_category(bmi)
    
    st.write("---")
    st.subheader("ผลการคำนวณ")
    
    metric_cols = st.columns(2)
    with metric_cols[0]:
        st.metric("BMI ของคุณ", f"{bmi}")
    with metric_cols[1]:
        st.metric("สถานะ", category)
    
    st.markdown(f'<div style="background-color:{color}20;padding:15px;border-radius:5px;border-left:5px solid {color}"><strong>คำแนะนำ:</strong> {advice}</div>', unsafe_allow_html=True)

# แสดงแผนภูมิ BMI
st.write("---")
st.subheader("เกณฑ์ BMI สำหรับคนเอเชีย")
st.pyplot(create_bmi_chart())

# แสดงข้อมูลเพิ่มเติม
with st.expander("ข้อมูลเพิ่มเติมเกี่ยวกับ BMI"):
    st.markdown("""
    **ดัชนีมวลกาย** (Body Mass Index - BMI) เป็นค่าที่คำนวณจากน้ำหนักและส่วนสูง ใช้บ่งชี้ว่า
    คุณมีน้ำหนักที่เหมาะสมกับส่วนสูงหรือไม่
    
    **สูตรคำนวณ BMI:**
    ```
    BMI = น้ำหนัก (กิโลกรัม) / (ส่วนสูง (เมตร))²
    ```
    
    **หมายเหตุ:** เกณฑ์ BMI ที่ใช้เป็นเกณฑ์สำหรับคนเอเชีย ซึ่งแตกต่างจากเกณฑ์สากล
    """)

# ส่วนท้ายของเว็บไซต์
st.write("---")
st.caption("แอปคำนวณ BMI พัฒนาด้วย Python และ Streamlit © 2025")


def save_qr_code(url, filename="bmi_app_qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR Code saved to {filename}")

# ใส่ IP Address ของคุณที่นี่
local_ip = "192.168.1.37"  # เปลี่ยนเป็น IP จริงของคุณ
port = 8501
url = f"http://{local_ip}:{port}"
save_qr_code(url)
