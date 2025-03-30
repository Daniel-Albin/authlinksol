The `backend/` folder contains the Python Flask server that handles:
- Decryption and verification of NFC tag data
- Validation of UID against the Solana blockchain

To run:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python verify.py
