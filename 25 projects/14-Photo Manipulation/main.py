import streamlit as st
import numpy as np
from PIL import Image as PILImage
import io

# Image processing functions adapted for PIL
def brighten(image_array, factor):
    # Factor > 1 brightens, < 1 darkens
    new_array = image_array * factor
    return np.clip(new_array, 0, 255).astype(np.uint8)

def adjust_contrast(image_array, factor, mid=128):
    # Adjust contrast by scaling difference from midpoint
    new_array = (image_array - mid) * factor + mid
    return np.clip(new_array, 0, 255).astype(np.uint8)

def blur(image_array, kernel_size):
    # Apply blur using a square kernel of given size (must be odd)
    x_pixels, y_pixels, num_channels = image_array.shape
    new_array = np.zeros_like(image_array)
    neighbor_range = kernel_size // 2
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                count = 0
                for x_i in range(max(0, x-neighbor_range), min(x_pixels, x+neighbor_range+1)):
                    for y_i in range(max(0, y-neighbor_range), min(y_pixels, y+neighbor_range+1)):
                        total += image_array[x_i, y_i, c]
                        count += 1
                new_array[x, y, c] = total / count
    return new_array.astype(np.uint8)

def apply_kernel(image_array, kernel):
    # Apply a convolution kernel (e.g., Sobel)
    x_pixels, y_pixels, num_channels = image_array.shape
    new_array = np.zeros_like(image_array)
    neighbor_range = kernel.shape[0] // 2
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x-neighbor_range), min(x_pixels, x+neighbor_range+1)):
                    for y_i in range(max(0, y-neighbor_range), min(y_pixels, y+neighbor_range+1)):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        if 0 <= x_k < kernel.shape[0] and 0 <= y_k < kernel.shape[1]:
                            kernel_val = kernel[x_k, y_k]
                            total += image_array[x_i, y_i, c] * kernel_val
                new_array[x, y, c] = total
    return np.clip(new_array, 0, 255).astype(np.uint8)

def combine_images(image1_array, image2_array):
    # Combine two images using square root of sum of squares
    new_array = np.sqrt(image1_array**2 + image2_array**2)
    return np.clip(new_array, 0, 255).astype(np.uint8)

# Streamlit UI
st.title("🖼️ Photo Manipulation App")
st.subheader("Upload an image and apply filters!")

# Image uploader
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # Load image
    image = PILImage.open(uploaded_file).convert("RGB")
    image_array = np.array(image).astype(np.float32)

    # Display original image
    st.write("**Original Image**")
    st.image(image, use_container_width=True)

    # Filter controls
    st.write("**Apply Filters**")
    with st.form("filter_form"):
        brightness = st.slider("Brightness (0.5 = darken, 1 = no change, 2 = brighten)", 0.5, 2.0, 1.0, 0.1)
        contrast = st.slider("Contrast (0.5 = decrease, 1 = no change, 2 = increase)", 0.5, 2.0, 1.0, 0.1)
        blur_size = st.selectbox("Blur Kernel Size (odd numbers)", [3, 5, 7, 9], index=0)
        apply_sobel = st.checkbox("Apply Sobel Edge Detection")
        submitted = st.form_submit_button("Apply Filters")

    if submitted:
        # Apply filters
        processed_array = image_array.copy()

        # Brightness
        if brightness != 1.0:
            processed_array = brighten(processed_array, brightness)

        # Contrast
        if contrast != 1.0:
            processed_array = adjust_contrast(processed_array, contrast, 128)

        # Blur
        if blur_size > 1:
            processed_array = blur(processed_array, blur_size)

        # Sobel edge detection
        if apply_sobel:
            sobel_x_kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
            sobel_y_kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
            sobel_x = apply_kernel(processed_array, sobel_x_kernel)
            sobel_y = apply_kernel(processed_array, sobel_y_kernel)
            processed_array = combine_images(sobel_x, sobel_y)

        # Convert back to PIL Image
        processed_image = PILImage.fromarray(processed_array)

        # Display processed image
        st.write("**Processed Image**")
        st.image(processed_image, use_container_width=True)

        # Download option
        buf = io.BytesIO()
        processed_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Processed Image",
            data=byte_im,
            file_name="processed_image.png",
            mime="image/png"
        )

# Instructions
with st.expander("📜 How to Use"):
    st.markdown("""
    ### How to Use
    - Upload an image (PNG, JPG, or JPEG).
    - Adjust the filters:
      - **Brightness**: Slide to darken (<1) or brighten (>1).
      - **Contrast**: Slide to decrease (<1) or increase (>1).
      - **Blur**: Select a kernel size (larger = more blur, must be odd).
      - **Sobel Edge Detection**: Check to apply edge detection.
    - Click **Apply Filters** to see the result.
    - Download the processed image using the button.

    ### About the Filters
    - **Brightness**: Multiplies pixel values by a factor.
    - **Contrast**: Scales pixel values around a midpoint (128).
    - **Blur**: Averages pixels within a square kernel.
    - **Sobel Edge Detection**: Uses Sobel kernels to detect edges, combining horizontal and vertical results.
    - **Built with Pillow for image processing and Streamlit for the UI.**
    """)