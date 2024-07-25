import sympy
from math import gcd 




def gen_key(p, q): 

    n = p * q
    
    #phi is the totient of n 
    phi = (p-1) * (q-1)

    #for generating public key 
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            e = i
            break

    #for generating private key ,d
    j = 0
    while True:
        if (j * e) % phi == 1:
            d = j
            break
        j += 1
    
    
    return ((e, n), (d, n))

def encrypt(priv_k, plaintext):
    #unpack
    key, n = priv_k
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    #Return the array of bytes
    return cipher


def decrypt(pub_k, ciphertext):
    #unpack 
    key, n = pub_k
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    msg = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(msg)

if __name__ == "__main__":
   
    p = sympy.randprime(0,100)
    q = sympy.randprime(0,100)
    while p == q:
        q=sympy.randprime(0,100)


    public, private = gen_key(p, q)

    message = input("Enter a message to encrypt:\n")
    encrypted_msg = encrypt(private, message)
    print("The encypted message is ")
    encrypted = ''.join(map(str, encrypted_msg))
    print(encrypted)
    
    
    print("The decrpted message is:")
    decrypted_message = decrypt(public, encrypted_msg)
    print(decrypted_message)




