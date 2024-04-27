# import socket
# import sys 

# ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# host, port = '127.0.0.1', 12345
# ClientSocket.sendto(b'', (host, port))

# while True:
#     color = ClientSocket.recvfrom(1024)[0].decode('utf-8')
#     print("Server mengirimkan warna:", color)
#     answer = input("Tebak warna ini (dalam bahasa Indonesia): ")
#     ClientSocket.sendto(str.encode(answer), (host, port))
#     print("Feedback dari server:", ClientSocket.recvfrom(1024)[0].decode('utf-8'))

# ClientSocket.close()
# sys.exit(0)

import socket
import sys

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host, port = '127.0.0.1', 12345
ClientSocket.sendto(b'', (host, port))

while True:
    color = ClientSocket.recvfrom(1024)[0].decode('utf-8')
    print("Server mengirimkan warna:", color)
    answer = input("Tebak warna ini (dalam bahasa Indonesia): ")
    ClientSocket.sendto(str.encode(answer), (host, port))
    feedback = ClientSocket.recvfrom(1024)[0].decode('utf-8')
    if feedback == '100':
        print("Feedback dari server: Jawaban Anda benar! Nilai Anda 100.")
    else:
        print("Feedback dari server: Jawaban Anda salah! Nilai Anda 0.")

ClientSocket.close()
sys.exit(0)