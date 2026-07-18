import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF

# Cấu hình giao diện
st.set_page_config(page_title="Ultimate Credit Engine", layout="wide")

# --- HÀM BỔ TRỢ ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BAO CAO THAM DINH TIN DUNG", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- UI CHÍNH ---
st.title("🚀 Ultimate Credit Engine Pro")

tabs = st.tabs(["📊 Thẩm định nhanh", "📈 Phân tích kịch bản", "🗂️ Quản lý hồ sơ"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Nhập liệu")
        so_tien = st.number_input("Số tiền vay (Triệu)", 10, 10000, 500)
        lai_suat = st.slider("Lãi suất (%/năm)", 1.0, 30.0, 9.5)
        ky_han = st.number_input("Kỳ hạn (Tháng)", 6, 360, 60)
    with col2:
        thu_nhap = st.number_input("Thu nhập (Triệu)", 5, 500, 30)
        phi_sinh_hoat = st.number_input("Chi phí sinh hoạt (Triệu)", 0, 100, 10)
        tsdb = st.number_input("Giá trị TSĐB (Triệu)", 0, 20000, 1000)

    # Tính toán
    tra_gop = (so_tien * (lai_suat/100/12)) / (1 - (1 + lai_suat/100/12)**-ky_han)
    kha_nang_tra = thu_nhap - phi_sinh_hoat
    dti = (tra_gop / (thu_nhap + 1)) * 100
    
    st.metric("Số tiền trả/tháng", f"{tra_gop:,.0f} triệu")
    
    if tra_gop > kha_nang_tra:
        st.error("CẢNH BÁO: Khoản vay vượt quá khả năng chi trả hàng tháng!")
    else:
        st.success("Tốt: Khoản vay nằm trong ngưỡng chi trả.")

with tabs[1]:
    st.subheader("Phân tích nhạy cảm (Sensitivity Analysis)")
    st.write("Ảnh hưởng của lãi suất đến số tiền phải trả:")
    
    scenarios = []
    for r in np.arange(lai_suat-2, lai_suat+3, 1):
        pmt = (so_tien * (r/100/12)) / (1 - (1 + r/100/12)**-ky_han)
        scenarios.append({'Lãi suất': f"{r:.1f}%", 'Số tiền trả': pmt})
    
    df_scen = pd.DataFrame(scenarios)
    st.line_chart(df_scen.set_index('Lãi suất'))

with tabs[2]:
    st.subheader("Xuất báo cáo")
    report_data = {"Số tiền vay": so_tien, "Lãi suất": lai_suat, "DTI": round(dti, 2)}
    if st.download_button("Tải xuống Báo cáo thẩm định (PDF)", data=generate_pdf(report_data), file_name="report.pdf"):
        st.balloons()
