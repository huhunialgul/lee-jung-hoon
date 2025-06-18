import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="의료 영상 품질 평가 툴", layout="wide")

st.title("🩻 의료 영상 품질 평가 툴")
st.markdown("업로드된 의료 영상을 기반으로 해상도, 노이즈 등 품질 요소를 평가합니다.")

uploaded_file = st.file_uploader("의료 영상 업로드 (JPG, PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("L")  # 흑백으로 변환
    img_array = np.array(image)

    st.subheader("업로드된 영상")
    st.image(image, caption="업로드된 영상", use_column_width=True)

    # 해상도 측정
    height, width = img_array.shape
    st.write(f"**해상도**: {width} x {height} px")

    # 노이즈 측정: 분산을 기반으로 간단한 측정
    noise_std = np.std(cv2.GaussianBlur(img_array, (3, 3), 0) - img_array)
    st.write(f"**노이즈 추정치 (표준편차)**: {noise_std:.2f}")

    # 선명도 측정: 라플라시안 기반
    laplacian_var = cv2.Laplacian(img_array, cv2.CV_64F).var()
    st.write(f"**선명도 (Laplacian Variance)**: {laplacian_var:.2f}")

    st.markdown("---")
    st.markdown("📌 **참고 지표:**")
    st.markdown("- 선명도가 너무 낮으면 흐릿한 영상일 수 있습니다.")
    st.markdown("- 노이즈가 높을수록 영상 품질이 저하되었을 가능성이 있습니다.")

