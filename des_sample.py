import pyDes

data = b"Please encrypt my data"

with open("des_key.txt","r") as f:
    des_key = f.read()

k = pyDes.des(des_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
d = k.encrypt(data)
#string_cipher = d
#print("String Cipher:" + string_cipher) 
print("Encrypted: %r" % d)
print(f"Encrypted: {d}")
print("Decrypted: %r" % k.decrypt(d).decode("utf-8"))
assert(k.decrypt(d) == data)
print("Key: %r" % k.getKey().decode("utf-8"))

# Decode the byte object produce to string -> from b'Please encrypt my data' to 'Please encrypt my data' 
#print(k.decrypt(d).decode("utf-8"))
#print(k.getKey().decode("utf-8"))