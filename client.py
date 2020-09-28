import socket
import sys
import pyDes
import hmac
import hashlib
# Create a socket for the server with the standard parameters.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get the local host name and create a port number to bind with the server socket.
host = socket.gethostname()
port = 1234
client_socket.connect((host,port))
# Giving the client its name for the chat.
name = "Client"
print(" Connected to chat server")
# Send server the client's name and get the server's name.
client_socket.send(name.encode())
s_name = client_socket.recv(1024)
s_name = s_name.decode()
print("")
print(s_name, "has joined the chat room ")

# Open the text file containing the shared DES Key and store as a string variable.
with open("des_key.txt","r") as f:
    des_key = f.read()
# Make sure that the key has 8 characters and store it to variable 'k'
des = pyDes.des(des_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

# Open the text file containing the shared HMAC key and store it as a string variable
with open("hmac_key.txt", "r") as f:
        hmac_key = f.read()
hmac_key_byte = hmac_key.encode("utf-8")
connection = True
# While connection is True.
while connection:
    # Enter a message to be encrypted and sent to server
    message = input(str("Please enter your message: "))
    
    str_message = message

    # The message is first encode as a byte object.
    message = message.encode()
    #byte_literal_message = message
    h = hmac.new(hmac_key_byte, message, hashlib.md5,)
    digest = h.hexdigest().encode("utf-8")

    concatenate_message = message + digest
    # Fucntion that encrypts message using the shared DES key.
    encrypted_message = des.encrypt(concatenate_message)

    client_socket.send(encrypted_message)

    # Python doesn't allow the encrypted message to be decoded.
    #print("***********************\n")
    print("--- Sender Side ---\n")
    print("Shared DES key is: " + des_key)
    print(f"Shared HMAC key is: {hmac_key}")
    print("Plain message is: " + str_message)
    print(f"Sender side HMAC is: {digest}")
    #print(f"HMAC concatenation with message: {concatenate_message}")
    print(f"Sent ciphertext is: {encrypted_message}")
    #print("***********************\n")
    print("\n")
    # Get the receiving encrypted message from server.
    recv_message = client_socket.recv(2048)
    # Decrypt the message from client with the shared DES key.
    decrypted_message = des.decrypt(recv_message).decode("utf-8")
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

    forward_encode_message = forward_message.encode("utf-8")
    h_calc = hmac.new(hmac_key_byte, forward_encode_message, hashlib.md5,)
    digest_calc = h_calc.hexdigest().encode("utf-8")
    hmac_string = hmac_string.encode("utf-8")
    #print("***********************")
    print("--- Receiver Side ---") 
    print(f"Received ciphertext is: {recv_message}")
    print("Received message is: " + forward_message)
    print(f"Received HMAC is: {hmac_string}")
    print(f"Calculated HMAC is: {digest_calc}")
    #print("***********************\n")
    print("\n")