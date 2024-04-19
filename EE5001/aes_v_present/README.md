# AES-128 vs PRESENT-80 Encryption Algorithms

This repository contains Python implementations of two symmetric key encryption algorithms: **AES-128** and **PRESENT-80**. These implementations were developed for an assignment in the IoT Security Module EE5001 at Dublin City University (DCU), mainly to demonstrate how the two algorithms compare in terms of code size, execution speed, and security strength.

## Files
- `AES_128.py`: Python script implementing the **AES-128** encryption algorithm.
- `Present_80.py`: Python script implementing the **PRESENT-80** encryption algorithm.

## Overview

### AES-128 Algorithm
- **Key size**: 128-bit
- **Block size**: 128-bit
- **Rounds**: 10
- **Security**: Strong resistance to cryptanalysis, especially brute-force attacks.
- **Applications**: Data encryption for hard drives, secure protocols (TLS, SSL, VPN), and secure storage.

The AES-128 implementation includes key expansion (11 round keys), byte substitution using an S-box, shifting rows, mixing columns with Galois field multiplication, and XORing the state with the round key.

### PRESENT-80 Algorithm
- **Key size**: 80-bit
- **Block size**: 64-bit
- **Rounds**: 32
- **Security**: Suitable for lightweight encryption, but not as strong as AES-128.
- **Applications**: Designed for low-power devices such as IoT sensors and edge computing.

The PRESENT-80 implementation uses 32 round keys and a post-whitening key, with each round applying a substitution step using a nibble-based S-box and a bit permutation layer.

## Comparison Summary
| Feature           | AES-128                          | PRESENT-80                       |
|-------------------|----------------------------------|----------------------------------|
| **Block Size**     | 128-bit                          | 64-bit                           |
| **Key Size**       | 128-bit                          | 80-bit                           |
| **Rounds**         | 10                               | 32                               |
| **Code Size**      | Larger, more complex             | Smaller, lightweight             |
| **Execution Speed**| Slower, more resource-intensive  | Faster, designed for low-power   |
| **Security**       | Stronger (128-bit strength)      | Adequate for lightweight uses    |

## Testing
Both implementations include test vector validation:
- **AES-128**: Provides test cases for validating encryption with predefined plaintext, key, and expected cipher values.
- **PRESENT-80**: Similar validation with lightweight block encryption and key expansion.

### Example Usage (AES-128)
```python
from AES_128 import AES128_Enc

# Encrypting a block using AES-128
master_key = '2b7e151628aed2a6abf7158809cf4f3c'
plaintext = '6bc1bee22e409f96e93d7e117393172a'
ciphertext = AES128_Enc.Encrypt(plaintext, master_key)
print(ciphertext)

Test_Vectors={'1' :{'TextBlock':plaintext ,'Key':master_key, 'Cipher': ciphertext},
             }
AES128_Enc.Vector_Testing(Test_Vectors)
```


### Example Usage (PRESENT-80)

```python
from Present_80 import Pres80

# Encrypting a block using PRESENT-80
key = '40000000000000000000'
plaintext = '0000000000000000'
ciphertext = Pres80.Encrypt(plaintext, key)
print(ciphertext)
Test_Vectors={'1' :{'TextBlock':plaintext ,'Key':master_key, 'Cipher': ciphertext},
             }
Pres80.Vector_Testing(Test_Vectors)
```