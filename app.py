from flask import Flask, render_template, request, jsonify
from crypto.pqc_crypto import generate_keypair, encrypt_message, decrypt_message

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_keys', methods=['GET'])
def generate_keys():
    """Handle the key generation request."""
    public_key, private_key = generate_keypair()
    # Convert keys to a readable format (e.g., hex or base64) for display
    return jsonify({
        'public_key': public_key.hex(),
        'private_key': private_key.hex()
    })

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Handle the encryption request."""
    data = request.get_json()
    message = bytes(data['message'], 'utf-8')
    public_key = bytes.fromhex(data['public_key'])
    
    ciphertext = encrypt_message(message, public_key)
    return jsonify({'ciphertext': ciphertext.hex()})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Handle the decryption request."""
    data = request.get_json()
    ciphertext = bytes.fromhex(data['ciphertext'])
    private_key = bytes.fromhex(data['private_key'])
    
    plaintext = decrypt_message(ciphertext, private_key)
    return jsonify({'plaintext': plaintext.decode('utf-8')})

if __name__ == '__main__':
    app.run(debug=True)
