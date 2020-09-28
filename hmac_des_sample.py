import pyDes
import hmac
import hashlib

#data = b"Please encrypt my data"
data = "Please encrypt my data"
data = data.encode()
with open("des_key.txt","r") as f:
    des_key = f.read()

key = pyDes.des(des_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

# Open the text file containing the shared HMAC key and store it as a string variable
with open("hmac_key.txt", "r") as f:
        hmac_key = f.read()
hmac_key_byte = hmac_key.encode("utf-8")
connection = True

#byte_literal_message = message
h = hmac.new(hmac_key_byte, data, hashlib.md5,)
digest = h.hexdigest().encode("utf-8")

concatenate_message = data + digest

encrypted_message = key.encrypt(concatenate_message)
#string_cipher = d
#print("String Cipher:" + string_cipher) 
decrypted_message = key.decrypt(encrypted_message).decode("utf-8")

print("Encrypted: %r" % encrypted_message)
#print(f"Encrypted: {d}")
print(f"HMAC key is: {hmac_key}")
print(f"HMAC Digest is: {digest}")
print("Digest Size: " + str(h.digest_size) + " bytes")
print("Block Size: " + str(h.block_size) + " bytes")
print(f"HMAC concatenation with message: {concatenate_message}")
print("Decrypted: %r" % decrypted_message)
#assert(k.decrypt(d) == data)
print("Key: %r" % key.getKey().decode("utf-8"))


count = 0
reverse_hmac = ''
reverse_message = ''
hmac_string = ''
forward_message = ''
for i in reversed(decrypted_message):
    count += 1
    if count < 33:
        reverse_hmac = reverse_hmac + i
    if count == 32:
        for j in reversed(reverse_hmac):
            hmac_string += j
    if count > 32:
        reverse_message = reverse_message + i
    if count == len(decrypted_message):
        for k in reversed(reverse_message):
            forward_message += k

#reverse_hmac = reverse_hmac + i
#for j in reversed(reverse_hmac):
#            hmac_string = hmac_string + reverse_hmac
print(count)
#for i in reversed(reverse_hmac):
#    hmac_string = hmac_string + i
print(hmac_string)
print(forward_message)
print(reverse_hmac)
print(reverse_message)
# Decode the byte object produce to string -> from b'Please encrypt my data' to 'Please encrypt my data' 
#print(k.decrypt(d).decode("utf-8"))
#print(k.getKey().decode("utf-8"))