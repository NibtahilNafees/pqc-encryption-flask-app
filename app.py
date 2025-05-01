from flask import Flask, render_template, request, redirect, url_for, flash, session
from crypto.pqc_crypto import generate_keypair, encrypt_message, decrypt_message
from dotenv import load_dotenv
import os
from uuid import uuid4

load_dotenv()

app = Flask(__name__)
app.secret_key = str(uuid4())

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
    ciphertext = None
    if request.method == "POST":
        if 'pqc_key' not in session:
            flash("Please generate a key first using the Key Generation page.", "danger")
            return redirect(url_for('encrypt'))  # Stay on same page
        
        message = request.form["message"].encode()
        ciphertext = encrypt_message(message, session['pqc_key'].encode()).decode()
    
    # Pass whether key exists to template
    return render_template("encrypt.html", 
                         ciphertext=ciphertext,
                         has_key='pqc_key' in session)

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    plaintext = None
    if request.method == "POST":
        if 'pqc_key' not in session:
            flash("Please generate a key first using the Key Generation page.", "danger")
            return redirect(url_for('decrypt'))  # Stay on same page
        
        try:
            ciphertext = request.form["ciphertext"].encode()
            plaintext = decrypt_message(ciphertext, session['pqc_key'].encode()).decode()
        except Exception:
            flash("Decryption failed. Please check your input.", "danger")
    
    return render_template("decrypt.html",
                        plaintext=plaintext,
                        has_key='pqc_key' in session)

if __name__ == "__main__":
    app.run(debug=True)