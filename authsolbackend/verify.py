from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from Crypto.Util.Padding import unpad
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import base64
import binascii

app = Flask(__name__)

# 🔐 Your 16-byte SDM AES key (hex format, change to your real key)
SDM_AES_KEY = bytes.fromhex("000102030405060708090A0B0C0D0E0F")

# 🔗 Solana config
SOLANA_PROGRAM_ID = Pubkey.from_string("DUYDjC7h8GUFiBUeY25CRjQfokdeRdUCyC5AbPhZiBTi")
SOLANA_RPC_URL = "https://api.devnet.solana.com"
solana_client = Client(SOLANA_RPC_URL)

@app.route("/verify")
def verify():
    enc = request.args.get("enc")
    mac = request.args.get("mac")

    if not enc or not mac:
        return jsonify({"error": "Missing ENC or MAC"}), 400

    try:
        # 🔓 Step 1: Decrypt ENC
        enc_bytes = binascii.unhexlify(enc)
        iv = bytes(16)  # Default IV = 16 zero bytes for NTAG 424
        cipher = AES.new(SDM_AES_KEY, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(enc_bytes), 16)

        uid = decrypted[:7]
        counter = int.from_bytes(decrypted[7:10], "big")

        print(f"🔓 UID: {uid.hex()}")
        print(f"🔢 Scan Counter: {counter}")

        # ✅ Step 2: Recalculate MAC
        cmac = CMAC.new(SDM_AES_KEY, ciphermod=AES)
        cmac.update(enc_bytes)
        calculated_mac = cmac.hexdigest()[:len(mac)]  # Truncate if needed

        if mac.lower() != calculated_mac.lower():
            return jsonify({"authentic": False, "reason": "MAC validation failed"}), 401

        # 🔗 Step 3: Derive PDA and check Solana
        seed = [b"product", uid]
        product_pda, _ = Pubkey.find_program_address(seed, SOLANA_PROGRAM_ID)

        response = solana_client.get_account_info(product_pda)
        exists = response.value is not None

        return jsonify({
            "authentic": exists,
            "uid": uid.hex(),
            "counter": counter,
            "product_address": str(product_pda)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

