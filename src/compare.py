import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def compare_images(cover_path, stego_path, diff_out="diff_map.png"):
    cover = np.array(Image.open(cover_path).convert("RGB"))
    stego = np.array(Image.open(stego_path).convert("RGB"))

    if cover.shape != stego.shape:
        raise ValueError("Изображения должны быть одинакового размера")

    diff = np.abs(cover.astype(np.int16) - stego.astype(np.int16))
    changed = np.any(diff > 0, axis=2)

    total_pixels = cover.shape[0] * cover.shape[1]
    changed_pixels = np.count_nonzero(changed)
    percent_pix = 100 * changed_pixels / total_pixels

    print(f"Изменено пикселей: {changed_pixels}/{total_pixels} ({percent_pix:.6f}%)")

    cover_bits = np.unpackbits(cover, axis=None)
    stego_bits = np.unpackbits(stego, axis=None)
    bit_diffs = np.count_nonzero(cover_bits != stego_bits)
    percent_bits = 100 * bit_diffs / len(cover_bits)

    print(f"Изменено бит: {bit_diffs}/{len(cover_bits)} ({percent_bits:.6f}%)")

    diff_map = np.zeros_like(cover)
    diff_map[changed] = [255, 0, 0]

    diff_intensity = diff.sum(axis=2)
    diff_norm = diff_intensity / np.max(diff_intensity + 1e-9)

    fig = plt.figure(figsize=(20, 10))
    plt.imshow(cover)

    fig = plt.figure(figsize=(20, 10))
    plt.imshow(stego)

    fig = plt.figure(figsize=(20, 10))
    plt.imshow(diff_map)

    fig = plt.figure(figsize=(20, 10))
    im = plt.imshow(diff_norm, cmap="inferno")
    fig.colorbar(im, fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.show()


compare_images("./output_data/dct_gs_img/before.png", "./output_data/dct_gs_img/after.png")