import random,math,hashlib


class RSA_Main:
    def IntMes(M, Mode=None):
        # Check if Message is a string
        if isinstance(M, str):
            # Encode the string to byte string in UTF-8 format 
            M = M.encode('utf-8')

            # Hash message in case of signature signing operation
            if Mode == "Hash":
                # Hash the bytes using SHA-256
                M = hashlib.sha256(M).digest()

            # Convert the bytes to an integer (big-endian)
            M = int.from_bytes(M, 'big')

        return M
    
    def CheckPrim(n):
        "'Miller-Rabin probabilistic Algorithm to check primality of randomly generated input '"

        # Compute how many rounds needed of dividing d by 2 until d is odd
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Repeat the test for primality 10  times for accuracy
        for _ in range(10):
            # Choose a random integer a smaller than n-2
            a = random.randint(2, n - 2)

            x = pow(a, d, n)

            # If x equals 1 or n-1, continue to the next iteration
            if x == 1 or x == n - 1:
                continue

            # Repeat squaring x r-1 times
            while r > 1:
                x = pow(x, 2, n)
                # If x is congruent to n-1, break
                if x == n - 1:
                    break
                r-=1
            #If x !=1 or n-1 exit function
            else:
                return False

        return True
    
    def genPrime(prime=1, range_l=5, range_h=100000):

        # Generate a random number within the specified range
        n = random.randint(range_l, range_h)
        
        # return false if even
        if n % 2 == 0:
            return  RSA_Main.genPrime(prime, range_l, range_h)

        # Repeat until a prime number is found
        while True:
            # In case this is the second prime number (q) regenerate if it equals to (p)
            if n == prime:
                return RSA_Main.genPrime(prime, range_l, range_h)

            # Check if the current number is prime using the Miller-Rabin Method
            if RSA_Main.CheckPrim(n):
                # If prime, return the number
                return n

            # If n not a prime, generate a new random number within the specified range
            n = random.randint(range_l, range_h)

    def GenParams(M):
        # If M is a large enough value reduce it for the lower range of generated prime numbers
        if M > 1000:
            M = M // 100

        # Generate a random prime number p and q within a range of 100000 values around M (M/100 to 1000*M) so no matter what size is M, N is large enough
        p = RSA_Main.genPrime(range_l=M, range_h=1000 * M)
        q = RSA_Main.genPrime(p, range_l=M, range_h=1000 * M)

        # Calculate N modulus
        N = p * q

        # Calculate totient function for the values of p, q
        phi = (p - 1) * (q - 1)

        return p, q, N, phi

    def setE(phi):

        # If e is between phi/2 and phi-1 then phi/e<2
        low = (phi // 2) + 1
        up= phi - 1

        ''' Generate public exponent e as a prime number, which together with phi/e<2  makes gcd(e,phi)=1 
        because if e is a prime number it does not have any common factors with phi except itself,
        and if phi/e<2 and e<phi it means phi is not a multiple of e '''
        e = RSA_Main.genPrime(range_l=low, range_h=up)

        return e


    def Mod_Egcd(inv, mod):
    
        # Store the initial modulus for later use
        init_mod = mod
        
        #  extended Euclidean algorithm variables
        x, y, u, v = 0, 1, 1, 0
        
        # modify mod until 0
        while mod != 0:
            q, t = divmod(inv, mod)
            inv, mod = mod, t
            x, u = u - q * x, x
            y, v = v - q * y, y
        
        # Check if the inverse exists (gcd is 1)
        if inv == 1:
            # Return the modular multiplicative inverse
            return u % init_mod  
        else:
            # Return None if the inverse does not exist
            return None  



    def GenKeys(M,phi,N):

        #Key pair generation 
        e=RSA_Main.setE(phi)
        d=RSA_Main.setD(e,phi)

        #Public key, Private key
        return (e,N) , (d,N)
    
    def encrypt(M, Exp,N):

        #Raise Message to exponent (could be e or d) and mod to N
        return pow(M,Exp,N)


    def CRT_Opt(p, q,C,d):

        #Calculate CRT unique parameters for each of p and q
        dp = d % (p - 1)
        dq = d % (q - 1)

        # Divide raising power of Cipher text to d into exponentation to dp, dq and mod to p, q respectively instead of N
        m1=pow(C, dp, p)
        m2=pow(C, dq, q)

        #Multiplicative Inverse for q mod p
        qinv = RSA_Main.Mod_Egcd(q, p)
        h=qinv*(m1-m2) %p

        #Assemble decrypted message
        message = m2+(h*q)
        return message

    def decrypt(p, q,C,Exp,Mode="Encryption"):
        #Use Chinese Remainder theorem to speed up decryption process
        Original=RSA_Main.CRT_Opt(p, q,C,Exp)
        #number of bytes in the original message= number of bits+guard bits/ 8 bits per byte
        len = (Original.bit_length() + 7) // 8

        # In case this is a regular encryption/decryption of a message, perform additional processing
        if(Mode!="Hash"):
            Original = Original.to_bytes(len, 'big')
            Original=Original.decode('utf-8')
        return Original
    


#Encryption Test
Message="This is a test message"
M=RSA_Main.IntMes(Message)
p,q,N,phi=RSA_Main.GenParams(M)
e=RSA_Main.setE(phi)
d=RSA_Main.Mod_Egcd(e,phi)
if d is not None:
    C=RSA_Main.encrypt(M,e,N)
    MM=RSA_Main.decrypt(p,q,C,d)
    if MM == Message:
        print("RSA Encryption successful. Original message: ", Message)
    else:
        print("RSA Encryption failed. Original message: ", Message)


#Signature Test
Message="This is a message signing test"
M=RSA_Main.IntMes(Message,"Hash")
p,q,N,phi=RSA_Main.GenParams(M)
e=RSA_Main.setE(phi)
d=RSA_Main.Mod_Egcd(e,phi)
if d is not None:
    C=RSA_Main.encrypt(M,d,N)
    MM=RSA_Main.decrypt(p,q,C,e,"Hash")
    if MM == M:
        print("RSA Signature successful. Original Hash Code: ", M)
    else:
        print("RSA Signature Original Hash Code: ", M)