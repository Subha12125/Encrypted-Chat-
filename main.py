import socket
import threading
import rsa
import time
from datetime import datetime


publicKey, privateKey = rsa.newkeys(1024)
public_partner = None
now = datetime.now()

print("Welcome to the secure chat application!")
time.sleep(2)
print("You can now start chatting with your friend securely.")
time.sleep(2)
choice = input("Do you want to host(1) or connect(2)? ")
if(choice == "1"):
    time.sleep(2)
    print("You are the host.")
    time.sleep(2)
    print("Please share your IP address with your friend.")
    time.sleep(3)
    print("Connecting to your friend...")
    

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.169.86", 9999))
    server.listen()
    client , _ = server.accept()
    client.send(publicKey.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(2048))


elif(choice == "2"):

    time.sleep(2)
    print("You are the client.")
    time.sleep(2)
    print("Please ask your friend for their IP address.")
    time.sleep(3)
    print("Connecting to your friend...")
    time.sleep(2)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.169.86", 9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(2048))
    client.send(publicKey.save_pkcs1("PEM"))

else:
    exit()

def sending_message(c):
    while True:
        message = input(">> ")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print(now.strftime("%H:%M ")+ "You: " + message)


def receiving_message(c):
    while True:
        print(now.strftime("%H:%M ")+"Client: " + rsa.decrypt(c.recv(1024), privateKey).decode())


threading.Thread(target=sending_message, args=(client,)).start()
threading.Thread(target=receiving_message, args=(client,)).start()

