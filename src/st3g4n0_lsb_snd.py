import argparse
import numpy as np
import wave
import random


def encode(input_wav, output_wav, message_path):
    with wave.open(input_wav, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(params.nframes)

    samples = np.frombuffer(frames, dtype=np.int16)
    message = open(message_path, 'rb').read()

    bits = ''.join(format(b, '08b') for b in message)
    h = len(samples)
    capacity = h
    if len(bits) > capacity - 8:
        raise ValueError(f"Сообщение слишком длинное ({len(bits)} бит), вместимость: {capacity - 8} бит")

    samples = samples.astype(np.int32)

    for i, bit in enumerate(bits):
        if (samples[i] & 1) != int(bit):
            if samples[i] == 32767:
                samples[i] -= 1
            elif samples[i] == -32768:
                samples[i] += 1
            else:
                samples[i] += random.choice([-1, 1])

    for j in range(8):
        if (samples[len(bits) + j] & 1) != 0:
            samples[len(bits) + j] ^= 1

    samples = np.clip(samples, -32768, 32767).astype(np.int16)

    with wave.open(output_wav, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(samples.tobytes())

    print(f"Сообщение ({len(message)} байт) встроено в {output_wav}")


def decode(stego_wav, output_path):
    with wave.open(stego_wav, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(params.nframes)

    samples = np.frombuffer(frames, dtype=np.int16)
    bits = []

    for i in range(len(samples)):
        bits.append(str(samples[i] & 1))
        if len(bits) >= 8 and bits[-8:] == ['0'] * 8:
            bits = bits[:-8]
            break

    message_bytes = bytes(int(''.join(bits[i:i+8]), 2) for i in range(0, len(bits), 8))
    open(output_path, 'wb').write(message_bytes)
    print(f"Извлечено {len(message_bytes)} байт -> {output_path}")


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

