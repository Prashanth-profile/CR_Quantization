import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

# SVD Compression Function
def svd_compression(frame, k):
    U, S, Vt = np.linalg.svd(frame, full_matrices=False)
    U_k = U[:, :k]
    S_k = np.diag(S[:k])
    Vt_k = Vt[:k, :]
    compressed_frame = np.dot(U_k, np.dot(S_k, Vt_k))
    compressed_size = (U_k.size + S_k.size + Vt_k.size)  # Total elements stored
    opt_size= (U_k.size + len(S[:k]) + Vt_k.size)
    return compressed_frame, compressed_size, opt_size

# JPEG Compression Function
def jpeg_compression(frame, quality):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded_img = cv2.imencode('.jpg', frame, encode_param)
    decoded_frame = cv2.imdecode(encoded_img, cv2.IMREAD_GRAYSCALE)
    compressed_size = len(encoded_img)  # Total bytes of compressed JPEG
    return decoded_frame, compressed_size

# Load video and process
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# SVD and JPEG parameters
svd_k_values = [6, 11, 22, 50]  # Singular values retained
jpeg_quality_values = [1, 7, 20, 73]  # JPEG quality levels

# Metrics storage
svd_results = []
jpeg_results = []
svd_opt_results=[]

# Process one frame for simplicity
for frame_idx in range(min(frame_count, 1)):  # Limit to 10 frames for demonstration
    ret, frame = cap.read()
#ret, frame = cap.read()
    if ret:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Original frame size in bytes
        original_size = gray_frame.size

        # SVD Compression
        for k in svd_k_values:
            svd_frame, svd_size, svd_opt_size = svd_compression(gray_frame, k)
            svd_psnr = psnr(gray_frame, svd_frame, data_range=gray_frame.max() - gray_frame.min())
            svd_ssim = ssim(gray_frame, svd_frame, data_range=gray_frame.max() - gray_frame.min())
            svd_comp_rate=svd_size/original_size
            svd_opt_comp_rate = svd_opt_size / original_size
            svd_results.append(("SVD", k, svd_size, svd_psnr, svd_ssim, svd_comp_rate))
            svd_opt_results.append(("R-SVD", k, svd_opt_size, svd_psnr, svd_ssim, svd_opt_comp_rate))
            cv2.imwrite(f"output/svd/frame_{frame_idx}_k{k}.png", svd_frame)

        # JPEG Compression
        for quality in jpeg_quality_values:
            jpeg_frame, jpeg_size = jpeg_compression(gray_frame, quality)
            jpeg_psnr = psnr(gray_frame, jpeg_frame, data_range=gray_frame.max() - gray_frame.min())
            jpeg_ssim = ssim(gray_frame, jpeg_frame, data_range=gray_frame.max() - gray_frame.min())
            jpeg_comp_rate=jpeg_size/original_size
            jpeg_results.append(("JPEG", quality, jpeg_size, jpeg_psnr, jpeg_ssim, jpeg_comp_rate))
            cv2.imwrite(f"output/jpeg/frame_{frame_idx}_q{quality}.jpg", jpeg_frame)

cap.release()

# Convert results to arrays
svd_method, svd_par, svd_sizes, svd_psnrs, svd_ssims, svd_rate = zip(*svd_results)
svd_method, svd_par, svd_opt_size, svd_psnrs, svd_ssims, svd_opt_comp_rate = zip(*svd_opt_results)
jpeg_method, jpeg_par, jpeg_sizes, jpeg_psnrs, jpeg_ssims, jpeg_rate = zip(*jpeg_results)

# Print results
print("Method | Parameter | Compressed Size (bytes) | PSNR | SSIM | Compression Rate")
for method, param, size, psnr_value, ssim_value, rate in svd_results:
    print(f"{method:6} | {param:9} | {size:22} | {psnr_value:.2f} | {ssim_value:.4f} | {rate:.3f}")

for method, param, size, psnr_value, ssim_value, rate in svd_opt_results:
    print(f"{method:6} | {param:9} | {size:22} | {psnr_value:.2f} | {ssim_value:.4f} | {rate:.3f}")

for method, param, size, psnr_value, ssim_value, rate in jpeg_results:
    print(f"{method:6} | {param:9} | {size:22} | {psnr_value:.2f} | {ssim_value:.4f} | {rate:.3f}")

# Plot SSIM
#plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(svd_rate, svd_psnrs, label="SVD", marker='o')
plt.plot(svd_opt_comp_rate, svd_psnrs, label="R-SVD", marker='o')
plt.plot(jpeg_rate, jpeg_psnrs, label="JPEG", marker='o')
#plt.title("SSIM vs Compressed Bytes")
plt.xlabel("Compressed Rate")
plt.ylabel("Compression PSNR")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(svd_sizes, svd_rate, label="SVD", marker='o')
plt.plot(svd_opt_size, svd_opt_comp_rate, label="R-SVD", marker='o')
plt.plot(jpeg_sizes, jpeg_rate, label="JPEG", marker='o')
#plt.title("SSIM vs Compressed Bytes")
plt.xlabel("Compressed Bytes")
plt.ylabel("Compression Rate")
plt.legend()

# Plot PSNR
plt.legend()

plt.tight_layout()
plt.show()
