import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST = '127.0.0.1'
PORT = 6000

clients = []

KEY = b'1234567890123456'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server started...")


def decrypt_message(ciphertext):
    iv = ciphertext[:16]
    ct = ciphertext[16:]

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    return pt.decode()


def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                clients.remove(client)


def handle_client(client):
    while True:
        try:
            encrypted_message = client.recv(1024)

            if not encrypted_message:
                break

            decrypted_message = decrypt_message(encrypted_message)

            print("Message:", decrypted_message)

            with open("chat_logs.txt", "a") as file:
                file.write(decrypted_message + "\n")

            broadcast(encrypted_message, client)

        except:
            break

    clients.remove(client)
    client.close()


while True:
    client, address = server.accept()

    print(f"Connected with {str(address)}")

    clients.append(client)

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()