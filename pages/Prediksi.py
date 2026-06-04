import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import base64

# =========================
# IMPORT PREPROCESS
# =========================
from tensorflow.keras.applications.resnet50 import preprocess_input

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Prediksi Penyakit",
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

        /* TEXT */

        h1, h2, h3, h4, h5, h6, p, label {{
            color:white;
        }}

        /* BUTTON */

        div.stButton > button {{

            width:100%;

            border-radius:15px;

            font-size:18px;

            font-weight:bold;

            background-color:#4CAF50;

            color:white;

            border:none;

            transition:0.3s;
        }}

        div.stButton > button:hover {{

            background-color:#45a049;

            transform:scale(1.03);
        }}

        /* FILE UPLOADER */

        section[data-testid="stFileUploader"] {{

            background-color:rgba(255,255,255,0.15);

            padding:15px;

            border-radius:15px;
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
# CHECK SESSION
# =========================
if "tanaman" not in st.session_state:

    st.warning(
        "Silakan pilih tanaman terlebih dahulu"
    )

    st.stop()

# =========================
# GET SESSION
# =========================
tanaman = st.session_state["tanaman"]

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model(tanaman):

    # =========================
    # CABAI
    # =========================
    if tanaman == "cabai":

        model_path = os.path.join(
            BASE_DIR,
            "models",
            "project_cabai.h5"
        )

    # =========================
    # TOMAT
    # =========================
    elif tanaman == "tomat":

        model_path = os.path.join(
            BASE_DIR,
            "models",
            "project_tomat.h5"
        )

    # =========================
    # KENTANG
    # =========================
    elif tanaman == "kentang":

        model_path = os.path.join(
            BASE_DIR,
            "models",
            "project_kentang.h5"
        )

    # =========================
    # LOAD MODEL
    # =========================
    model = tf.keras.models.load_model(

        model_path,

        compile=False,

        custom_objects={
            "preprocess_input": preprocess_input
        }
    )

    return model

# =========================
# LOAD MODEL
# =========================
model = load_model(tanaman)

# =========================
# CLASS NAMES
# =========================
class_names = {

    "tomat": [
        "Bacterial_spot",
        "Early_blight",
        "Late_blight",
        "Target_Spot",
        "Tomato_Yellow_Leaf_Curl_Virus"
    ],

    "cabai": [
        "Whitefly",
        "Yellowish",
        "Leaf_Curl_Virus",
        "Leaf_Spot"
    ],

    "kentang": [
        "Early Blight",
        "Late Blight"
    ]
}

# =========================
# TITLE
# =========================
st.markdown(
    f"""
    <h1 style='text-align:center; color:white;'>
    Deteksi Penyakit Daun {tanaman.capitalize()}
    </h1>
    """,

    unsafe_allow_html=True
)

st.write("")

# =========================
# FILE UPLOADER
# =========================
uploaded_file = st.file_uploader(
    "Upload Gambar Daun CABAI/TOMAT/KENTANG yang ingin dicek jenis penyakitnya ",
    type=["jpg", "jpeg", "png"]
)

# =========================/
# PREDIKSI
# =========================
if uploaded_file is not None:

    # =========================
    # OPEN IMAGE
    # =========================
    image = Image.open(
        uploaded_file
    ).convert("RGB")

    # =========================
    # SHOW IMAGE
    # =========================
    st.image(
        image,
        caption="Gambar Upload",
        width=350
    )

    # =========================
    # RESIZE IMAGE
    # =========================
    img = image.resize((224, 224))

    # =========================
    # IMAGE TO ARRAY
    # =========================
    img_array = np.array(img)

    # =========================
    # EXPAND DIMENSION
    # =========================
    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # =========================
    # PREDICT
    # =========================
    prediction = model.predict(
        img_array
    )

    # =========================
    # GET CLASS
    # =========================
    predicted_class = np.argmax(
        prediction
    )

    # =========================
    # CONFIDENCE
    # =========================
    confidence = np.max(
        prediction
    ) * 100

    # =========================
    # RESULT
    # =========================
    hasil = class_names[tanaman][predicted_class]

    # =========================
    # SHOW RESULT
    # =========================
    st.markdown(
    f"""
    <div style="
        background-color: #d4edda;
        border-left: 6px solid #28a745;
        padding: 15px 20px;
        border-radius: 8px;
        color: #155724;
        font-size: 30px;
        font-weight: bold;
    ">
        Hasil Prediksi Daun yang Dicek Terjangkit Penyakit:{hasil}
    </div>
    """,
    unsafe_allow_html=True
)    
    # =========================
    # CONFIDENCE
    # =========================
    st.markdown(
    f"""
    <div style="
        background-color: #d4edda;
        border-left: 6px solid #28a745;
        padding: 15px 20px;
        border-radius: 8px;
        color: #155724;
        font-size: 30px;
        font-weight: bold;
    ">
        Dengan Tingkat Keyakinan : {confidence:.2f}%
    </div>
    """,
    unsafe_allow_html=True
) 
    

    st.write("")

    # =========================
    # PROBABILITAS
    # =========================
    st.subheader(
        "dengan Probabilitas Terjangankit Jenis Penyakit Lainnya:"
    )

    for i, kelas in enumerate(
        class_names[tanaman]
    ):

        prob = prediction[0][i] * 100

        st.write(
            f"{kelas} : {prob:.2f}%"
        )

        st.progress(
            float(prob / 100)
        )

# =========================
# BACK BUTTON
# =========================
st.write("")
st.write("")

if st.button("⬅️ Kembali"):

    st.switch_page("app.py")