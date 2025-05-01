# Post-Quantum Cryptography Flask App

This is a Flask web application demonstrating Post-Quantum Cryptography (PQC) using the Kyber512 algorithm. It provides a user interface for generating keypairs, encrypting messages, and decrypting ciphertexts.

## Features
- **Key Generation**: Generate Kyber512 public/private keypairs.
- **Encryption**: Encrypt messages using the public key.
- **Decryption**: Decrypt ciphertexts using the private key.
- **Secure Headers**: Uses Flask-Talisman for secure HTTP headers.
- **Frontend**: Bootstrap-based UI with AJAX for smooth interactions.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-repo>/pqc-flask-app.git
   cd pqc-flask-app