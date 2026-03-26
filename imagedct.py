import cv2
import numpy as np
from scipy.fftpack import dct
import matplotlib.pyplot as plt

# -----------------------------
# Helper function: Apply DCT-II
# -----------------------------
def dct2(block):
    """
    Apply 2D Type-II DCT to a given 2D array.
    """
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# -----------------------------
# Load image
# -----------------------------
image_path = "your_image.jpg"  # Replace with your image path
img_bgr = cv2.imread(image_path)

if img_bgr is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

# Convert to RGB for display
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# -----------------------------
# Convert to grayscale
# -----------------------------
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# -----------------------------
# Apply DCT-II to grayscale
# -----------------------------
dct_gray = dct2(np.float32(img_gray))

# -----------------------------
# Apply DCT-II to each color channel
# -----------------------------
channels = cv2.split(img_rgb)
dct_channels = [dct2(np.float32(ch)) for ch in channels]

# -----------------------------
# Visualization
# -----------------------------
plt.figure(figsize=(12, 8))

# Original images
plt.subplot(2, 3, 1)
plt.imshow(img_rgb)
plt.title("Original Color")
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(img_gray, cmap='gray')
plt.title("Grayscale")
plt.axis("off")

# DCT magnitude (log scale for visibility)
plt.subplot(2, 3, 4)
plt.imshow(np.log1p(np.abs(dct_gray)), cmap='gray')
plt.title("DCT-II (Grayscale)")
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(np.log1p(np.abs(dct_channels[0])), cmap='Reds')
plt.title("DCT-II (Red Channel)")
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(np.log1p(np.abs(dct_channels[1])), cmap='Greens')
plt.title("DCT-II (Green Channel)")
plt.axis("off")

plt.tight_layout()
plt.show()

# -----------------------------
# Numerical comparison
# -----------------------------
energy_gray = np.sum(dct_gray**2)
energy_color = sum(np.sum(ch**2) for ch in dct_channels)

print(f"Energy (Grayscale DCT): {energy_gray:.2f}")
print(f"Energy (Color DCT sum of channels): {energy_color:.2f}")