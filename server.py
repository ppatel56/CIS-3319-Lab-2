import socket
import sys
import pyDes
import hmac
import hashlib

# Create a socket for the server with the standard parameters.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get the local host name and create a port number to bind with the server socket.
host = socket.gethostname()
port = 1234
server_socket.bind((host,port))
# Giving the server its name for the chat.
name = "Server"
print("")
print("Server is waiting for incoming connections.....\n")
# Server is listening for a socket, in this case only one socket. 
server_socket.listen(1)
# Accept the connection to client and get it's name.
client_connection, addr = server_socket.accept()
print("Recieved connection\n")
s_name = client_connection.recv(1024)
s_name = s_name.decode()
print(s_name, "has joined the chat room")
# Send client the server's name.
client_connection.send(name.encode())

# Open the text file containing the shared DES Key and store as a string variable.
with open("des_key.txt","r") as f:
        des_key = f.read()
# Make sure that the key has 8 characters and store it to variable 'k'
key_des = pyDes.des(des_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

# Open the text file containing the shared HMAC key and store it as a string variable
with open("hmac_key.txt", "r") as f:
        hmac_key = f.read()
hmac_key_byte = hmac_key.encode("utf-8")

connection = True
# While connection is True.
while connection:

        # Get the receiving encrypted message from client.
        recv_message = client_connection.recv(2048)
        # Decrypt the message from client with the shared DES key.
        decrypted_message = key_des.decrypt(recv_message).decode("utf-8")
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
        # Since received message from client is encrypted as a byte object,
        # Python doesn't allow it to be decoded.
        #print("***********************\n") 
        print("--- Receiver Side ---") 
        print(f"Received ciphertext is: {recv_message}")
        print("Received message is: " + forward_message)
        print(f"Received HMAC is: {hmac_string}")
        print(f"Calculated HMAC is: {digest_calc}")
        print("\n")
        #print("***********************\n")

        message = input(str("Please enter your message: "))
        
        str_message = message
        message = message.encode("utf-8")
        
        h = hmac.new(hmac_key_byte, message, hashlib.md5,)
        digest = h.hexdigest().encode("utf-8")

        concatenate_message = message + digest

        #concatenate_message = concatenate_message.encode("utf-8")
        # Fucntion that encrypts message using the shared DES key.
        encrypted_message = key_des.encrypt(concatenate_message)

        client_connection.send(encrypted_message)
        
        #print("***********************\nKey is: " + des_key)
        print("--- Sender Side ---\n")
        print("Shared DES key is: " + des_key)
        print(f"Shared HMAC key is: {hmac_key}")
        #print("Plain message is: " + str_message)
        print(f"Sender side HMAC is: {digest}")
        #print(f"HMAC concatenation with message: {concatenate_message}")
        print(f"Sent ciphertext is: {encrypted_message}")
        #print("***********************\n")
        print("\n")
        #print("***********************\n")
