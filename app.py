from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_talisman import Talisman
from crypto.pqc_crypto import generate_keypair, encrypt_message, decrypt_message
from dotenv import load_dotenv
from forms import EncryptForm, DecryptForm
from uuid import uuid4
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = str(uuid4())

# Configure Talisman with security headers
talisman = Talisman(
    app,
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            'https://cdn.jsdelivr.net',
            'https://code.jquery.com',
            'https://cdnjs.cloudflare.com'
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com'
        ],
        'img-src': [
            "'self'",
            'data:',
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com'
        ],
        'font-src': [
            "'self'",
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com'
        ],
        'connect-src': "'self'",
        'frame-ancestors': "'none'",
        'base-uri': "'self'",
        'form-action': "'self'"
    },
    content_security_policy_nonce_in=['script-src'],
    referrer_policy='strict-origin-when-cross-origin',
    permissions_policy={
        'geolocation': '()',
        'camera': '()',
        'microphone': '()',
        'payment': '()'
    },
    force_file_save=True,
    x_content_type_options=True,
    x_xss_protection=True
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/keygen", methods=["GET", "POST"])
def keygen():
    if request.method == "POST":
        key, _ = generate_keypair()
        session['pqc_key'] = key.decode()  # Store in Flask session
        flash("Key generated successfully!", "success")
        return redirect(url_for('keygen'))
    
    public_key = session.get('pqc_key')
    return render_template("keygen.html", public_key=public_key)

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    form = EncryptForm()
    ciphertext = None
    
    if form.validate_on_submit():
        if 'pqc_key' not in session:
            flash("Please generate a key first using the Key Generation page.", "danger")
            return redirect(url_for('encrypt'))
        
        message = form.message.data.encode()
        ciphertext = encrypt_message(message, session['pqc_key'].encode()).decode()
    
    return render_template("encrypt.html", 
                         form=form,
                         ciphertext=ciphertext,
                         has_key='pqc_key' in session)

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    form = DecryptForm()
    plaintext = None
    
    if form.validate_on_submit():
        if 'pqc_key' not in session:
            flash("Please generate a key first using the Key Generation page.", "danger")
            return redirect(url_for('decrypt'))
        
        try:
            ciphertext = form.ciphertext.data.encode()
            plaintext = decrypt_message(ciphertext, session['pqc_key'].encode()).decode()
        except Exception:
            flash("Decryption failed. Please check your input.", "danger")
    
    return render_template("decrypt.html",
                        form=form,
                        plaintext=plaintext,
                        has_key='pqc_key' in session)

if __name__ == "__main__":
    app.run(debug=True)