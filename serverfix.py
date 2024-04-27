# import socket
# import random
# import time

# # Daftar kata warna dalam bahasa Inggris
# colors_en = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'brown']

# # Daftar terjemahan kata warna dalam bahasa Indonesia
# color_translations = {
#     'red': 'merah',
#     'blue': 'biru',
#     'green': 'hijau',
#     'yellow': 'kuning',
#     'orange': 'orange',
#     'purple': 'ungu',
#     'brown' : 'coklat'
# }

# # Fungsi untuk mengirim kata warna acak ke semua klien
# def send_color(sock, clients):
#     color = random.choice(colors_en)
#     message = color.encode()
#     for client_addr in clients:
#         sock.sendto(message, client_addr)
#     print("Sent color:", color)

# # Fungsi untuk memeriksa jawaban klien dan memberikan nilai feedback
# def check_answer(sock, client_addr, answer, colors_en, clients):
#     color_en = colors_en[clients[client_addr]]
#     color_id = color_translations[color_en]
#     if answer.lower() == color_id:
#         feedback = b'100'  # Jika jawaban benar, berikan nilai 100
#         feedback_msg = b'Jawaban Anda benar! nilai anda 100'
#     else:
#         feedback = b'0'  # Jika jawaban salah, berikan nilai 0
#         feedback_msg = b'Jawaban Anda salah! nilai anda 0'
#     sock.sendto(feedback_msg, client_addr)
#     return feedback

# # Fungsi utama
# def main():
#     server_address = ('localhost', 12345)

#     # Buat socket UDP
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     server_socket.bind(server_address)

#     clients = {}  # Dictionary untuk menyimpan alamat klien dan indeks warna yang telah dikirim

#     print("Server is running...")

#     while True:
#         # Terima jawaban dari klien dan berikan feedback
#         server_socket.settimeout(5)  # Set timeout 5 detik
#         try:
#             while True:
#                 data, client_address = server_socket.recvfrom(1024)
#                 answer = data.decode()
#                 if client_address not in clients:
#                     clients[client_address] = random.randint(0, len(colors_en) - 1)
#                 feedback = check_answer(server_socket, client_address, answer, colors_en, clients)
#                 print_feedback(client_address, answer, feedback)
#         except socket.timeout:
#             pass

#         # Kirim kata warna acak ke semua klien setiap 10 detik
#         send_color(server_socket, clients)
#         time.sleep(10)

#     server_socket.close()

# def print_feedback(client_addr, client_answer, feedback):
#     if feedback == b'100':
#         print("Client at {} answered correctly with '{}'.".format(client_addr, client_answer))
#     else:
#         print("Client at {} answered incorrectly with '{}'.".format(client_addr, client_answer))

# if __name__ == "__main__":
#     main()

import socket
import random
import time

# Daftar kata warna dalam bahasa Inggris
colors_en = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'brown']

# Daftar terjemahan kata warna dalam bahasa Indonesia
color_translations = {
    'red': 'merah',
    'blue': 'biru',
    'green': 'hijau',
    'yellow': 'kuning',
    'orange': 'orange',
    'purple': 'ungu',
    'brown': 'coklat'
}

# Fungsi untuk mengirim kata warna acak ke semua klien
def send_color(sock, clients):
    for client_addr, _ in clients.items():
        color_index = random.randint(0, len(colors_en) - 1)
        color_en = colors_en[color_index]
        message = color_en.encode()
        sock.sendto(message, client_addr)
        print("Sent color:", color_en, "to", client_addr)
        clients[client_addr] = color_index  # Simpan indeks warna yang dikirim ke klien

# Fungsi untuk memeriksa jawaban klien dan memberikan nilai feedback
def check_answer(sock, client_addr, answer, clients):
    color_en = colors_en[clients[client_addr]]
    color_id = color_translations[color_en]
    if answer.lower() == color_id:
        feedback = b'100'  # Jika jawaban benar, berikan nilai 100
    else:
        feedback = b'0'  # Jika jawaban salah, berikan nilai 0
    sock.sendto(feedback, client_addr)

# Fungsi utama
def main():
    server_address = ('localhost', 12345)

    # Buat socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)

    clients = {}  # Dictionary untuk menyimpan alamat klien dan indeks warna yang telah dikirim

    print("Server is running...")

    while True:
        # Kirim kata warna acak ke semua klien setiap 10 detik
        send_color(server_socket, clients)
        time.sleep(10)

        # Terima jawaban dari klien dan berikan feedback
        server_socket.settimeout(5)  # Set timeout 5 detik
        try:
            while True:
                data, client_address = server_socket.recvfrom(1024)
                answer = data.decode()
                if client_address not in clients:
                    clients[client_address] = random.randint(0, len(colors_en) - 1)
                check_answer(server_socket, client_address, answer, clients)
        except socket.timeout:
            pass

    server_socket.close()

if __name__ == "__main__":
    main()