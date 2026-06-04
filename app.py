import streamlit as st
import base64

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Deteksi Penyakit Tanaman",
    layout="centered"
)

# =========================
# FUNCTION BACKGROUND
# =========================
def add_bg_from_local(image_file):

    with open(image_file, "rb") as image:

        encoded_string = base64.b64encode(
            image.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{

            background:
            linear-gradient(
                rgba(0,0,0,0.45),
                rgba(0,0,0,0.45)
            ),

            url(
                "data:image/jpg;base64,{encoded_string}"
            );

            background-size: cover;

            background-position: center;

            background-repeat: no-repeat;

            background-attachment: fixed;
        }}

        /* TITLE */

        .main-title{{
            text-align:center;
            font-size:50px;
            font-weight:bold;
            color:white;
        }}

        /* SUB TITLE */

        .sub-title{{
            text-align:center;
            font-size:24px;
            color:white;
        }}

        /* PILIH TANAMAN */

        .pilih{{
            text-align:center;
            background-color:#FFD700;
            padding:12px;
            border-radius:15px;
            font-size:28px;
            font-weight:bold;
            color:black;
        }}

        /* BUTTON */

        div.stButton > button {{

            height:120px;

            width:100%;

            font-size:24px;

            font-weight:bold;

            border-radius:20px;

            border:none;

            background-color:white;

            color:black;

            transition:0.3s;
        }}

        div.stButton > button:hover {{

            background-color:#4CAF50;

            color:white;

            transform:scale(1.05);
        }}

        </style>
        """,

        unsafe_allow_html=True
    )

# =========================
# CALL BACKGROUND
# =========================
add_bg_from_local("bg.jpg")

# =========================
# HEADER
# =========================
st.markdown(
    """
    <p class="main-title">
    🌱 Deteksi Penyakit Tanaman
    </p>
    """,

    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="sub-title">
    Aplikasi Klasifikasi Penyakit Daun
    Cabai, Tomat, dan Kentang
    </p>
    """,

    unsafe_allow_html=True
)

st.write("")
st.write("")

# =========================
# PILIH TANAMAN
# =========================
st.markdown(
    """
    <p class="pilih">
    Silakan Pilih Tanaman
    </p>
    """,

    unsafe_allow_html=True
)

st.write("")
st.write("")

# =========================
# BUTTON TANAMAN
# =========================
col1, col2, col3 = st.columns(3)

# =========================
# CABAI
# =========================
with col1:

    if st.button("🌶️ CABAI"):

        st.session_state["tanaman"] = "cabai"

        st.switch_page("pages/Prediksi.py")

# =========================
# TOMAT
# =========================
with col2:

    if st.button("🍅 TOMAT"):

        st.session_state["tanaman"] = "tomat"

        st.switch_page("pages/Prediksi.py")

# =========================
# KENTANG
# =========================
with col3:

    if st.button("🥔 KENTANG"):

        st.session_state["tanaman"] = "kentang"

        st.switch_page("pages/Prediksi.py")