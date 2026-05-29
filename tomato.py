import streamlit as st
import pandas as pd
import joblib
import os

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="스마트팜 착과율 예측",
    page_icon="🌱",
    layout="centered"
)

# -----------------------------
# CSS 디자인
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f4fff4;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #2e7d32;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-bottom: 30px;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #43a047, #66bb6a);
    color: white;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
    height: 55px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #2e7d32, #43a047);
    transform: scale(1.02);
}

.result-box {
    background-color: #e8f5e9;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-top: 25px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

.result-text {
    font-size: 30px;
    font-weight: bold;
    color: #1b5e20;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 모델 불러오기 (안전하게 로드: 우선 'rfmodel.pkl', 없으면 'tomato.pkl' 사용)
# -----------------------------
model_candidates = ["rfmodel.pkl", "tomato.pkl"]
rf_model = None
loaded_model_name = None
for m in model_candidates:
    if os.path.exists(m):
        rf_model = joblib.load(m)
        loaded_model_name = m
        break

if rf_model is None:
    st.error("모델 파일이 없습니다. 'rfmodel.pkl' 또는 'tomato.pkl'을 프로젝트 루트에 업로드하세요.")
    st.stop()

# 모델 로드된 파일명 (디버그용)
st.write(f"Loaded model: {loaded_model_name}")

# -----------------------------
# 제목
# -----------------------------
st.markdown('<div class="title">🌱 스마트팜 착과율 예측 시스템</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">환경 데이터를 기반으로 예상 착과율을 예측합니다.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# 입력 영역 카드
# -----------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📌 환경 데이터 입력")

    col1, col2 = st.columns(2)

    with col1:
        temp = st.number_input(
            "🌡 내부온도 (℃)",
            min_value=-20.0,
            max_value=60.0,
            value=25.0,
            step=0.1
        )

        humidity = st.number_input(
            "💧 내부습도 (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=0.1
        )

    with col2:
        soil_temp = st.number_input(
            "🌱 지온 (℃)",
            min_value=-10.0,
            max_value=50.0,
            value=20.0,
            step=0.1
        )

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 예측 버튼
# -----------------------------
if st.button("📊 착과율 예측하기"):

    # DataFrame 생성
    input_data = pd.DataFrame(
        [[temp, humidity, soil_temp]],
        columns=['내부온도', '내부습도', '지온']
    )

    # 예측
    predicted = rf_model.predict(input_data)

    # 결과 출력
    st.markdown(f"""
    <div class="result-box">
        <div style="font-size:22px;">예상 착과율</div>
        <div class="result-text">{predicted[0]:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    # 상태 메시지
    if predicted[0] >= 80:
        st.success("🔥 매우 좋은 환경입니다!")
    elif predicted[0] >= 60:
        st.info("👍 양호한 환경 상태입니다.")
    else:
        st.warning("⚠ 환경 조건 개선이 필요합니다.")