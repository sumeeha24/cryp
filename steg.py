from PIL import Image
import numpy as np

def _message_to_bits(message: bytes) -> list:
    return [int(bit) for byte in message for bit in format(byte, '08b')]

def _bits_to_bytes(bits: list) -> bytes:
    return bytes(int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8))

def hide_data_in_image(image_path: str, data: bytes, output_path: str):
    image = Image.open(image_path)
    img_arr = np.array(image)
    flat_img = img_arr.flatten()

    bits = _message_to_bits(data)
    bits += [0]*8  # delimiter
    if len(bits) > len(flat_img):
        raise ValueError("Message too long")

    for i, bit in enumerate(bits):
        flat_img[i] = int(flat_img[i]) & ~1 | bit

    new_img = flat_img.reshape(img_arr.shape)
    Image.fromarray(new_img.astype(np.uint8)).save(output_path)

def extract_data_from_image(image_path: str) -> bytes:
    image = Image.open(image_path)
    img_arr = np.array(image)
    flat_img = img_arr.flatten()

    bits = [int(flat_img[i]) & 1 for i in range(len(flat_img))]
    byte_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == [0]*8:
            break
        byte_list.extend(byte)
    return _bits_to_bytes(byte_list)
