import streamlit as st
import qrcode
from PIL import Image
import io
import base64

st.set_page_config(page_title="QR Code Encoder/Decoder", page_icon="📱")

st.title("QR Code Encoder / Decoder")

mode = st.radio("Select mode", ["Encode", "Decode"])

if mode == "Encode":
    data = st.text_area("Enter text to encode")
    if st.button("Generate QR Code"):
        if data:
            # Generate QR code
            qr = qrcode.make(data)
            # Convert QR code to a BytesIO object
            buf = io.BytesIO()
            qr.save(buf)
            buf.seek(0)  # Move to the beginning of the BytesIO buffer
            # Display the QR code image
            st.image(buf, caption="Generated QR Code", use_column_width=True)
            # Create a download link for the QR code
            b64 = base64.b64encode(buf.getvalue()).decode()
            href = f'<a href="data:file/png;base64,{b64}" download="qrcode.png">Download QR Code</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Please enter text to encode.")
else:
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded QR Code", use_column_width=True)
        try:
            import pyzbar.pyzbar as pyzbar
            decoded = pyzbar.decode(img)
            if decoded:
                for d in decoded:
                    st.write("Decoded data:", d.data.decode())
            else:
                st.warning("Could not decode QR code.")
        except ImportError:
            st.error("pyzbar is required to decode QR codes. Please install it.")
