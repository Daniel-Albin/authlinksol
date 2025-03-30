from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from Crypto.Util.Padding import pad
import binascii

# 🔐 Same AES key used in verify.py
SDM_AES_KEY = bytes.fromhex("000102030405060708090A0B0C0D0E0F")

# 📦 Fake UID (7 bytes) + counter (3 bytes)
uid = bytes.fromhex("04AABBCCDDEE01")   # 7-byte UID
counter = (42).to_bytes(3, 'big')        # Scan counter = 42
payload = uid + counter                  # Total: 10 bytes

# Pad and encrypt using AES-CBC with IV=0
iv = bytes(16)
cipher = AES.new(SDM_AES_KEY, AES.MODE_CBC, iv)
enc = cipher.encrypt(pad(payload, 16))
enc_hex = binascii.hexlify(enc).decode()

# Calculate MAC
cmac = CMAC.new(SDM_AES_KEY, ciphermod=AES)
cmac.update(enc)
mac_hex = cmac.hexdigest()[:16]  # Truncated to simulate NTAG behavior

print("enc=", enc_hex)
print("mac=", mac_hex)

