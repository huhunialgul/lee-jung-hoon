import streamlit as st

# --------------------------
# 기본 설정
# --------------------------
st.set_page_config(page_title="BMI & 건강 지표 계산기", layout="centered")

st.title("🩺 BMI & 건강 지표 계산기")
st.write("당신의 키, 몸무게, 성별, 나이 등을 입력하면 건강 지표와 맞춤형 팁을 제공합니다.")

# --------------------------
# 사용자 입력
# --------------------------
gender = st.radio("성별", ["남성", "여성"])
age = st.number_input("나이", min_value=10, max_value=120, value=25)
height = st.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=170.0)
weight = st.number_input("몸무게 (kg)", min_value=30.0, max_value=200.0, value=70.0)

activity_level = st.selectbox("활동 수준", [
    "매우 적음 (거의 운동 안 함)",
    "가벼운 활동 (주 1~2회)",
    "보통 활동 (주 3~5회)",
    "활발한 활동 (거의 매일)",
    "매우 활발 (하루 2회 운동 이상)"
])

# --------------------------
# 계산 함수
# --------------------------

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "저체중", "영양 보충과 적절한 식사 중요"
    elif 18.5 <= bmi < 23:
        return "정상", "현재 체중을 유지하세요"
    elif 23 <= bmi < 25:
        return "과체중", "가벼운 운동과 식단 조절이 권장됩니다"
    elif 25 <= bmi < 30:
        return "비만 (1단계)", "체중 감량을 위한 적극적인 관리가 필요합니다"
    else:
        return "고도비만", "의료 전문가 상담 권장"

def calculate_bmr(gender, weight, height, age):
    if gender == "남성":
        return round(66 + (13.7 * weight) + (5 * height) - (6.8 * age), 1)
    else:
        return round(655 + (9.6 * weight) + (1.8 * height) - (4.7 * age), 1)

def get_activity_multiplier(level):
    return {
        "매우 적음 (거의 운동 안 함)": 1.2,
        "가벼운 활동 (주 1~2회)": 1.375,
        "보통 활동 (주 3~5회)": 1.55,
        "활발한 활동 (거의 매일)": 1.725,
        "매우 활발 (하루 2회 운동 이상)": 1.9
    }.get(level, 1.2)

# --------------------------
# 결과 출력
# --------------------------

if st.button("건강 지표 계산하기"):
    bmi = calculate_bmi(weight, height)
    bmi_status, bmi_tip = interpret_bmi(bmi)
    bmr = calculate_bmr(gender, weight, height, age)
    multiplier = get_activity_multiplier(activity_level)
    daily_calories = round(bmr * multiplier, 1)

    st.subheader("📊 결과 요약")
    st.write(f"**BMI**: {bmi} ({bmi_status})")
    st.write(f"**기초대사량 (BMR)**: {bmr} kcal/day")
    st.write(f"**권장 일일 섭취 칼로리**: {daily_calories} kcal/day")

    st.subheader("💡 건강 팁")
    st.info(bmi_tip)

    st.subheader("🏃 운동 루틴 추천")
    if bmi < 18.5:
        st.write("- 요가, 가벼운 근력 운동")
        st.write("- 고칼로리 영양 섭취와 병행")
    elif bmi < 23:
        st.write("- 유산소 + 근력운동 균형")
        st.write("- 주 3~4회, 30분 이상 운동")
    elif bmi < 25:
        st.write("- 빠르게 걷기, 자전거, 가벼운 조깅")
        st.write("- 식단 조절도 병행하세요")
    else:
        st.write("- 유산소 운동 중심: 걷기, 수영, 자전거")
        st.write("- 운동 강도는 점진적으로 증가시키세요")
        st.write("- 식사량 조절 및 영양소 균형 중요")
