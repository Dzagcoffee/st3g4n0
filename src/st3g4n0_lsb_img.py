from PIL import Image
import numpy as np
import argparse
import random


def encode(input_path, output_path, message_path):
    img = Image.open(input_path).convert('RGB')
    arr = np.array(img, dtype=np.int16)
    message = open(message_path, 'rb').read()
    bits = ''.join([format(b, '08b') for b in message])

    h, w, _ = arr.shape
    capacity = h * w * 3

    if len(bits) > capacity:
        raise ValueError(f"Сообщение слишком длинное ({len(bits)} бит), вместимость: {capacity} бит")

    flat = arr.reshape(-1)

    for i, bit in enumerate(bits):
        if (flat[i] & 1) != int(bit):
            if flat[i] == 0:
                flat[i] += 1
            elif flat[i] == 255:
                flat[i] -= 1
            else:
                flat[i] += random.choice([-1, 1])

    for j in range(8):
        if (flat[len(bits) + j] & 1) != 0:
            flat[len(bits) + j] ^= 1

    arr = np.clip(flat, 0, 255).astype(np.uint8).reshape(h, w, 3)

    Image.fromarray(arr).save(output_path)

    print(f"Сообщение ({len(message)} байт) встроено в {output_path}")


def decode(input_path, output_path):
    img = Image.open(input_path).convert('RGB')
    arr = np.array(img).reshape(-1)

    bits = []

    for i in range(len(arr)):
        bits.append(str(arr[i] & 1))

        if len(bits) >= 8 and bits[-8:] == ['0'] * 8:
            bits = bits[:-8]
            break

    bytes_out = bytes(int(''.join(bits[i:i+8]), 2) for i in range(0, len(bits), 8))
    
    open(output_path, 'wb').write(bytes_out)

    print(f"Извлечено {len(bytes_out)} байт -> {output_path}")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    enc = subparsers.add_parser('encode')
    enc.add_argument('-i', '--input', required=True)
    enc.add_argument('-o', '--output', required=True)
    enc.add_argument('-m', '--message', required=True)

    dec = subparsers.add_parser('decode')
    dec.add_argument('-i', '--input', required=True)
    dec.add_argument('-o', '--output', required=True)

    args = parser.parse_args()

    if args.cmd == 'encode':
        encode(args.input, args.output, args.message)
    elif args.cmd == 'decode':
        decode(args.input, args.output)


if __name__ == '__main__':
    main()

