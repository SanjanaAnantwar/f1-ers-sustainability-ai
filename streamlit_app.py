import streamlit as st
import requests
import matplotlib.pyplot as plt
import base64

def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

set_bg("background.jpg")
API_URL = "http://127.0.0.1:8001/predict"

st.set_page_config(page_title="F1 Green AI", page_icon="🏎️", layout="wide")

st.title("🏎️🌱 F1 Green AI – V8 vs Hybrid + ERS")
st.markdown("### AI-based efficiency comparison for sustainability")

col1, col2 = st.columns(2)

def get_prediction(engine):
    res = requests.post(API_URL, json={"engine_type": engine})
    return res.json()

if st.button("🚀 Run Comparison"):
    v8 = get_prediction("V8")
    hybrid = get_prediction("Hybrid")

    with col1:
        st.subheader("🔴 V8 Engine")
        st.metric("Fuel Used (kg)", v8["fuel_used_kg"])
        st.metric("ERS Energy (MJ)", v8["ers_energy_mj"])
        st.metric("Efficiency Score", v8["efficiency_score"])

    with col2:
        st.subheader("🟢 Hybrid + ERS")
        st.metric("Fuel Used (kg)", hybrid["fuel_used_kg"])
        st.metric("ERS Energy (MJ)", hybrid["ers_energy_mj"])
        st.metric("Efficiency Score", hybrid["efficiency_score"])

    # Bar chart
    fig, ax = plt.subplots(figsize=(3, 2))

ax.bar(
    ["V8", "Hybrid"],
    [v8["fuel_used_kg"], hybrid["fuel_used_kg"]],
    width=0.35,
    color=["#e10600", "#00ff9c"]
)

ax.set_ylabel("Fuel Used (kg)")
ax.set_title("Fuel Comparison", fontsize=9)
ax.tick_params(labelsize=8)

fig.patch.set_alpha(0)
ax.set_facecolor("none")

plt.tight_layout()
st.pyplot(fig, use_container_width=False)