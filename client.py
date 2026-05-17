import socket
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

HOST = '127.0.0.1'
PORT = 6000

KEY = b'1234567890123456'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_CBC)

    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))

    return cipher.iv + ct_bytes

def decrypt_message(ciphertext):
    iv = ciphertext[:16]
    ct = ciphertext[16:]

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    return pt.decode()



def receive_messages():
    while True:
        try:
            encrypted_message = client.recv(1024)

            if encrypted_message:
                decrypted_message = decrypt_message(encrypted_message)
                print("\nFriend:", decrypted_message)

        except:
            print("Disconnected from server")
            client.close()
            break


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


while True:
    message = input("You: ")

    encrypted_message = encrypt_message(message)

    client.send(encrypted_message)