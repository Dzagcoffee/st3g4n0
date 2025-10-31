import cv2
import numpy as np
import argparse
import struct


UV = (4, 3)
MIN_AMP = 3.0
BLOCK_SIZE = 8
VIZ = True


def bytes_to_bits(b: bytes) -> str:
    return ''.join(f'{x:08b}' for x in b)

def bits_to_bytes(bits: str) -> bytes:
    L = (len(bits) // 8) * 8
    
    return bytes(int(bits[i:i+8], 2) for i in range(0, L, 8))

def dct_map(img: np.ndarray) -> np.ndarray:
    d = cv2.dct(img.astype(np.float32))
    m = np.log1p(np.abs(d))
    m = (m / (m.max() + 1e-8) * 255).astype(np.uint8)
    
    return m

def save_viz(before: np.ndarray, after: np.ndarray, prefix: str):
    before_map = dct_map(before)
    after_map = dct_map(after)
    diff = cv2.absdiff(before_map, after_map)
    
    cv2.imwrite(prefix + "_dct_before.png", before_map)
    cv2.imwrite(prefix + "_dct_after.png", after_map)
    cv2.imwrite(prefix + "_dct_diff.png", diff)
    
    print("Сохранены DCT-карты:", prefix + "_dct_before.png", prefix + "_dct_after.png", prefix + "_dct_diff.png")

def embed_sign(c: float, bit: int, min_amp: float) -> float:
    a = abs(c)

    if a < min_amp:
        a = min_amp
    
    return a if bit == 0 else -a

def extract_sign(c: float) -> int:
    return 0 if c >= 0 else 1


def encode(input_path: str, output_path: str, message_path: str):
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        raise FileNotFoundError(f"Не удалось открыть {input_path}")

    try:
        with open(message_path, 'r', encoding='windows-1251') as f:
            msg = f.read().encode('windows-1251')
    except Exception:
        with open(message_path, 'rb') as f:
            msg = f.read()

    header = struct.pack('<I', len(msg))
    data = header + msg
    bits = bytes_to_bits(data)

    h, w = img.shape
    H, W = (h // BLOCK_SIZE) * BLOCK_SIZE, (w // BLOCK_SIZE) * BLOCK_SIZE
    cover = img[:H, :W].astype(np.float32)
    stego = cover.copy()

    if VIZ:
        before = cover.copy()

    bit_idx = 0
    total_bits = len(bits)

    for i in range(0, H, BLOCK_SIZE):
        for j in range(0, W, BLOCK_SIZE):
            if bit_idx >= total_bits:
                break
    
            block = cover[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE]
            dct = cv2.dct(block)
            u, v = UV
            b = int(bits[bit_idx])
            dct[u, v] = embed_sign(dct[u, v], b, MIN_AMP)
            stego[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE] = cv2.idct(dct)
            bit_idx += 1
    
        if bit_idx >= total_bits:
            break

    out_img = np.clip(stego, 0, 255).astype(np.uint8)
    cv2.imwrite(output_path, out_img)
    
    print(f"Встроено {len(msg)} байт -> {output_path}")

    if VIZ:
        save_viz(before, stego, output_path.rsplit('.', 1)[0])


def decode(input_path: str, output_path: str):
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Не удалось открыть {input_path}")

    h, w = img.shape
    H, W = (h // BLOCK_SIZE) * BLOCK_SIZE, (w // BLOCK_SIZE) * BLOCK_SIZE
    region = img[:H, :W].astype(np.float32)

    bits = []
    for i in range(0, H, BLOCK_SIZE):
        for j in range(0, W, BLOCK_SIZE):
            block = region[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE]
            dct = cv2.dct(block)
            bits.append(str(extract_sign(dct[UV[0], UV[1]])))

    data = bits_to_bytes(''.join(bits))
    msg_len = struct.unpack('<I', data[:4])[0]
    msg_data = data[4:4+msg_len]

    with open(output_path, 'wb') as f:
        f.write(msg_data)

    print(f"Извлечено {len(msg_data)} байт → {output_path}")

    try:
        print("Сообщение (Windows-1251):", msg_data.decode('windows-1251'))
    except UnicodeDecodeError:
        print("Сообщение содержит бинарные данные или другую кодировку и не может быть отображено. Сообщение сохранено в файл.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    enc = sub.add_parser('encode')
    enc.add_argument('-i', '--input', required=True)
    enc.add_argument('-o', '--output', required=True)
    enc.add_argument('-m', '--message', required=True)

    dec = sub.add_parser('decode')
    dec.add_argument('-i', '--input', required=True)
    dec.add_argument('-o', '--output', required=True)

    args = ap.parse_args()
    if args.cmd == 'encode':
        encode(args.input, args.output, args.message)
    else:
        decode(args.input, args.output)


if __name__ == '__main__':
    main()

