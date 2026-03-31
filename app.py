import streamlit as st
from PIL import Image, ImageFilter
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

st.title("✨ AI Image Dashboard")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🧰 Tools")

uploaded_file = st.sidebar.file_uploader(
    "📤 Upload Image",
    type=["png", "jpg", "jpeg"]
)

tool = st.sidebar.radio(
    "Select Tool",
    ["🎨 Background Change", "✨ Enhance Image"]
)

# =========================
# MAIN AREA
# =========================
col1, col2 = st.columns(2)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    image.thumbnail((600, 600))

    with col1:
        st.subheader("📸 Original Image")
        st.image(image, use_column_width=True)

    # =========================
    # 🎨 BACKGROUND TOOL
    # =========================
    if tool == "🎨 Background Change":
        st.sidebar.subheader("🎨 Background Settings")

        color = st.sidebar.color_picker("Pick Color", "#00ffaa")

        if st.sidebar.button("🚀 Apply Background"):
            with st.spinner("Removing background..."):
                from rembg import remove

                cutout = remove(image).convert("RGBA")

                bg = Image.new("RGBA", cutout.size, color)
                result = Image.alpha_composite(bg, cutout)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button(
                "📥 Download",
                buf.getvalue(),
                "background.png"
            )

    # =========================
    # ✨ ENHANCE TOOL
    # =========================
    elif tool == "✨ Enhance Image":
        st.sidebar.subheader("✨ Enhance Settings")

        strength = st.sidebar.slider("Sharpness", 1, 5, 2)

        if st.sidebar.button("🚀 Enhance"):
            with st.spinner("Enhancing image..."):
                result = image

                for _ in range(strength):
                    result = result.filter(ImageFilter.SHARPEN)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button(
                "📥 Download",
                buf.getvalue(),
                "enhanced.png"
            )

else:
    st.info("👈 Upload an image from the sidebar to begin")