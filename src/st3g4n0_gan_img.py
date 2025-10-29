from steganogan import SteganoGAN
steganogan = SteganoGAN.load(architecture='dense')

with open("input_data/secret.txt") as f:
    steganogan.encode(
        'input_data/img.png',
        'output_data/stego_gan.png',
        f.read()
    )

print(steganogan.decode('output_data/stego_gan.png'))
