# RSA Encryption and Signing

This repository contains a Python implementation of the **RSA** asymmetric key encryption algorithm. The project demonstrates RSA encryption and decryption, as well as message signing and verification.

## Files
- `RSA_Main.py`: Python script implementing the **RSA** encryption algorithm with methods for encryption, decryption, and digital signatures.

## Overview

### RSA Algorithm
- **Key Type**: Asymmetric (Public and Private Key)
- **Key Generation**:
  - Two large prime numbers are selected to generate a modulus \( n = p \times q \).
  - Public exponent \( e \) is chosen such that \( \gcd(\phi(n), e) = 1 \), where \( \phi(n) \) is Euler's totient function.
  - Private exponent \( d \) is the multiplicative inverse of \( e \mod \phi(n) \).
- **Encryption**: 
  - Uses the receiver's public key \( (e, n) \) to encrypt the message: \( \text{Cipher} = \text{Message}^e \mod n \).
- **Decryption**: 
  - Uses the private key \( (d, n) \) to decrypt the message: \( \text{Message} = \text{Cipher}^d \mod n \).

### Digital Signatures
- **Signing**: The sender hashes the message and encrypts it using their private key.
- **Verification**: The recipient can verify the signature by decrypting it with the sender’s public key and comparing it to a hash of the original message.


## Testing
The implementation includes test vector validation for both encryption and signing.

### Example Usage (Encryption)
```python
from RSA_Main import RSA_Main

# Encrypting a message using RSA
message = "This is a test message"
M = RSA_Main.IntMes(message)
p, q, N, phi = RSA_Main.GenParams(M)
e = RSA_Main.setE(phi)
d = RSA_Main.Mod_Egcd(e, phi)
if d is not None:
    C = RSA_Main.encrypt(M, e, N)
    decrypted_message = RSA_Main.decrypt(p, q, C, d)
    if decrypted_message == message:
        print("RSA Encryption successful. Original message:", message)
    else:
        print("RSA Encryption failed.")
