import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import qrcode
from PIL import Image
from io import BytesIO

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="เครื่องมือคำนวณ BMI",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS สำหรับตกแต่งหน้าเว็บ
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px #aaa;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-top: 2rem;
        border-bottom: 2px solid #1E88E5;
        padding-bottom: 0.5rem;
    }
    .result-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: #E3F2FD;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #0D47A1;
    }
    .instruction-box {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #9E9E9E;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ส่วนหัวของแอป
st.markdown('<h1 class="main-header">🧮 เครื่องมือคำนวณดัชนีมวลกาย (BMI)</h1>', unsafe_allow_html=True)

# เมนู sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=BMI", width=150)
    st.title("เกี่ยวกับ BMI")
    st.markdown("""
    **BMI (Body Mass Index)** คือดัชนีที่ใช้วัดสัดส่วนรูปร่างของร่างกาย 
    คำนวณจากน้ำหนักและส่วนสูง ใช้ประเมินภาวะน้ำหนักเกินและอ้วนในผู้ใหญ่
    
    **เกณฑ์การประเมิน:**
    - น้อยกว่า 18.5 = น้ำหนักน้อย / ผอม
    - 18.5 - 24.9 = น้ำหนักปกติ
    - 25.0 - 29.9 = น้ำหนักเกิน
    - 30.0 ขึ้นไป = อ้วน / อ้วนมาก
    """)
    
    # เพิ่มข้อมูลผู้พัฒนา
    with st.expander("เกี่ยวกับผู้พัฒนา"):
        st.write("พัฒนาโดย: [ชื่อของคุณ]")
        st.write("เวอร์ชัน: 1.0.0")
        st.write("ติดต่อ: your.email@example.com")

# ส่วนหลักของแอป
st.markdown('<div class="instruction-box">กรุณากรอกน้ำหนักและส่วนสูงของคุณเพื่อคำนวณค่า BMI</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    น้ำหนัก = st.number_input("น้ำหนัก (กิโลกรัม)", min_value=0.0, max_value=500.0, value=60.0, step=0.1)
with col2:
    ส่วนสูง = st.number_input("ส่วนสูง (เซนติเมตร)", min_value=0.0, max_value=250.0, value=170.0, step=0.1)

# ฟังก์ชันคำนวณ BMI
def คำนวณ_bmi(น้ำหนัก, ส่วนสูง_ซม):
    ส่วนสูง_เมตร = ส่วนสูง_ซม / 100
    return น้ำหนัก / (ส่วนสูง_เมตร ** 2)

# ฟังก์ชันแปลผล BMI
def แปลผล_bmi(bmi):
    if bmi < 18.5:
        return "น้ำหนักน้อย / ผอม", "blue", "คุณควรเพิ่มน้ำหนักโดยรับประทานอาหารที่มีประโยชน์เพิ่มขึ้น"
    elif bmi < 25:
        return "น้ำหนักปกติ", "green", "คุณมีน้ำหนักที่เหมาะสม ควรรักษาสุขภาพให้แข็งแรงต่อไป"
    elif bmi < 30:
        return "น้ำหนักเกิน", "orange", "คุณควรควบคุมอาหารและออกกำลังกายอย่างสม่ำเสมอ"
    else:
        return "อ้วน / อ้วนมาก", "red", "คุณควรปรึกษาแพทย์เพื่อวางแผนลดน้ำหนักอย่างเหมาะสม"

# ฟังก์ชันสร้าง QR Code
def สร้าง_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # แปลงรูปเป็น bytes เพื่อแสดงใน Streamlit
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

if st.button("คำนวณ BMI"):
    # ตรวจสอบข้อมูลนำเข้า
    if น้ำหนัก <= 0 or ส่วนสูง <= 0:
        st.error("กรุณากรอกน้ำหนักและส่วนสูงที่มากกว่า 0")
    else:
        # คำนวณ BMI
        bmi = คำนวณ_bmi(น้ำหนัก, ส่วนสูง)
        ผลประเมิน, สี, คำแนะนำ = แปลผล_bmi(bmi)
        
        # แสดงผลลัพธ์
        st.markdown(f'<div class="result-box"><h3>ผลลัพธ์</h3>BMI ของคุณคือ <span style="font-size:1.5rem; font-weight:bold; color:{สี}">{bmi:.2f}</span><br>การประเมิน: <span style="font-size:1.2rem; font-weight:bold; color:{สี}">{ผลประเมิน}</span><br><br>{คำแนะนำ}</div>', unsafe_allow_html=True)
        
        # สร้างแผนภูมิ BMI
        fig, ax = plt.subplots(figsize=(10, 2))
        plt.xlim(10, 40)
        plt.ylim(0, 1)
        
        # สร้างช่วง BMI
        ax.axvspan(10, 18.5, alpha=0.2, color='blue')
        ax.axvspan(18.5, 25, alpha=0.2, color='green')
        ax.axvspan(25, 30, alpha=0.2, color='orange')
        ax.axvspan(30, 40, alpha=0.2, color='red')
        
        # เพิ่มตำแหน่งปัจจุบัน
        plt.plot(bmi, 0.5, 'ro', markersize=12)
        
        # เพิ่มป้ายกำกับ
        plt.text(14.25, 0.5, 'น้ำหนักน้อย', ha='center')
        plt.text(21.75, 0.5, 'ปกติ', ha='center')
        plt.text(27.5, 0.5, 'น้ำหนักเกิน', ha='center')
        plt.text(35, 0.5, 'อ้วน', ha='center')
        
        plt.title('แผนภูมิดัชนีมวลกาย (BMI)')
        plt.tick_params(axis='y', which='both', left=False, labelleft=False)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # คำนวณน้ำหนักที่เหมาะสม
        ส่วนสูง_เมตร = ส่วนสูง / 100
        น้ำหนักต่ำสุด = 18.5 * (ส่วนสูง_เมตร ** 2)
        น้ำหนักสูงสุด = 24.9 * (ส่วนสูง_เมตร ** 2)
        
        st.markdown(f'<div class="instruction-box"><h4>น้ำหนักที่เหมาะสมสำหรับส่วนสูง {ส่วนสูง} ซม.</h4>น้ำหนักที่เหมาะสมควรอยู่ระหว่าง {น้ำหนักต่ำสุด:.1f} - {น้ำหนักสูงสุด:.1f} กิโลกรัม</div>', unsafe_allow_html=True)
        
        # สร้าง QR Code สำหรับแชร์
        st.markdown('<h3 class="sub-header">แชร์แอปพลิเคชันนี้</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            # จำลองการสร้าง URL สำหรับแชร์
            # ในการใช้งานจริง นี่ควรเป็น URL ของแอปที่เผยแพร่แล้ว
            demo_url = "https://yourusername-bmi-calculator-streamlit-app.streamlit.app"
            st.markdown(f"สแกน QR Code เพื่อเข้าถึงแอปพลิเคชัน\n\nURL: `{demo_url}`")
        
        with col2:
            # สร้าง QR Code สำหรับแชร์
            qr_image = สร้าง_qr_code(demo_url)
            st.image(qr_image, width=200)

# ส่วนท้ายของแอป
