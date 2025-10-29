#!/usr/bin/env python3

import cv2
import numpy as np
import argparse

def _dct_map(img_gray: np.ndarray) -> np.ndarray:
    f32 = img_gray.astype(np.float32)
    dct = cv2.dct(f32)
    mag = np.log1p(np.abs(dct))
    mag -= mag.min()
    if mag.max() > 0:
        mag /= mag.max()
    return (mag * 255).astype(np.uint8)

def _save_viz(before_gray: np.ndarray, after_gray: np.ndarray, out_prefix: str):
    dct_before = _dct_map(before_gray)
    dct_after  = _dct_map(after_gray)

    delta = cv2.absdiff(dct_before, dct_after)

    cv2.imwrite(f"{out_prefix}_dct_before.png", dct_before)
    cv2.imwrite(f"{out_prefix}_dct_after.png",  dct_after)
    cv2.imwrite(f"{out_prefix}_dct_delta.png",  delta)

def embed_dct(cover_path: str, secret_path: str, output_path: str, viz: bool = False):
    cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
   
    if cover is None:
        raise FileNotFoundError(f"Unable to open {cover_path}")

    msg = open(secret_path, 'rb').read()
    bits = ''.join(format(b, '08b') for b in msg) + '00000000'

    h, w = cover.shape
    H, W = (h // 8) * 8, (w // 8) * 8
    base = cover[:H, :W].astype(np.float32).copy()

    if viz:
        before_gray = base.astype(np.uint8)

    bit_idx = 0
    for i in range(0, H, 8):
        for j in range(0, W, 8):
            if bit_idx >= len(bits):
                break
            block = base[i:i+8, j:j+8]
            dct = cv2.dct(block)

            u, v = 4, 3
            coeff = dct[u, v]
            bit = int(bits[bit_idx])

            ival = int(np.round(coeff))
            if (abs(ival) % 2) != bit:
                if ival >= 0:
                    ival += 1
                else:
                    ival -= 1
            dct[u, v] = float(ival)

            base[i:i+8, j:j+8] = cv2.idct(dct)
            bit_idx += 1
        if bit_idx >= len(bits):
            break

    stego = np.clip(base, 0, 255).astype(np.uint8)
    out = cover.copy()
    out[:H, :W] = stego
    cv2.imwrite(output_path, out)
    print(f"Сообщение ({len(msg)} байт) встроено в {output_path}")

    if viz:
        _save_viz(before_gray, out[:H, :W], output_path.rsplit('.', 1)[0])

def extract_dct(stego_path: str, output_path: str):
    img = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Unable to open {stego_path}")

    h, w = img.shape
    H, W = (h // 8) * 8, (w // 8) * 8
    region = img[:H, :W].astype(np.float32)

    bits = []
    done = False
    for i in range(0, H, 8):
        for j in range(0, W, 8):
            block = region[i:i+8, j:j+8]
            dct = cv2.dct(block)
            ival = int(np.round(dct[4, 3]))
            bits.append(str(abs(ival) % 2))
            if len(bits) >= 8 and bits[-8:] == ['0'] * 8:
                bits = bits[:-8]
                done = True
                break
        if done:
            break

    data = bytes(int(''.join(bits[k:k+8]), 2) for k in range(0, len(bits), 8))
    open(output_path, 'wb').write(data)
    print(f"Извлечено {len(data)} байт → {output_path}")

def main():
    ap = argparse.ArgumentParser(description="Стеганография через DCT (8x8) с визуализацией спектра")
    sub = ap.add_subparsers(dest='cmd', required=True)

    enc = sub.add_parser('encode', help='Встроить сообщение (DCT)')
    enc.add_argument('-i', '--input', required=True, help='Путь к исходному изображению')
    enc.add_argument('-o', '--output', required=True, help='Путь к выходному изображению')
    enc.add_argument('-m', '--message', required=True, help='Файл с сообщением (текст/бинарный)')
    enc.add_argument('--viz', action='store_true', help='Сохранить DCT-карты до/после и их разницу')

    dec = sub.add_parser('decode', help='Извлечь сообщение (DCT)')
    dec.add_argument('-i', '--input', required=True, help='Путь к стего-изображению')
    dec.add_argument('-o', '--output', required=True, help='Файл для сохранения результата')

    args = ap.parse_args()

    if args.cmd == 'encode':
        embed_dct(args.input, args.message, args.output, viz=args.viz)
    else:
        extract_dct(args.input, args.output)

if __name__ == '__main__':
    main()

