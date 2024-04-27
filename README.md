# IF-UTS-Pemograman-Jaringan

Nama: Anggita Rachmadinda Putri
Kelas: IF 02 - 01
NIM: 1203220086
Mata Kuliah: Pemograman Jaringan

# SOAL
Buatlah sebuah permainan yang menggunakan soket dan protokol UDP. Permainannya cukup sederhana, dengan 1 server dapat melayani banyak klien (one-to-many). Setiap 10 detik, server akan mengirimkan kata warna acak dalam bahasa Inggris kepada semua klien yang terhubung. Setiap klien harus menerima kata yang berbeda (unik). Selanjutnya, klien memiliki waktu 5 detik untuk merespons dengan kata warna dalam bahasa Indonesia. Setelah itu, server akan memberikan nilai feedback 0 jika jawabannya salah dan 100 jika benar.

# Syarat UTS :
- Kerjakan dengan menggunakan bahasa pemrograman python
- Menggunakan protokol UDP
- Code untuk server dan client dikumpulkan di github repository masing masing
- Pada readme.md silahkan beri penjelaskan how code works.
- Pada readme.md silahkan beri screenshoot cara penggunaaan serta contoh ketika program berjalan
- Test case : 1 server 10 client.
- Pastikan memahami soal.
- Silahkan kumpulkan link github repository di assignment ini.
- JANGAN TELAT !

## Source Code
1. Server.py
    import socket
    import random
    import time
    
    colors_en = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'brown']

    color_translations = {
        'red': 'merah',
        'blue': 'biru',
        'green': 'hijau',
        'yellow': 'kuning',
        'orange': 'orange',
        'purple': 'ungu',
        'brown': 'coklat'
    }
    
    def send_color(sock, clients):
        for client_addr, _ in clients.items():
            color_index = random.randint(0, len(colors_en) - 1)
            color_en = colors_en[color_index]
            message = color_en.encode()
            sock.sendto(message, client_addr)
            print("Sent color:", color_en, "to", client_addr)
            clients[client_addr] = color_index  # Simpan indeks warna yang dikirim ke klien

    def check_answer(sock, client_addr, answer, clients):
        color_en = colors_en[clients[client_addr]]
        color_id = color_translations[color_en]
        if answer.lower() == color_id:
            feedback = b'100'  # Jika jawaban benar, berikan nilai 100
        else:
            feedback = b'0'  # Jika jawaban salah, berikan nilai 0
        sock.sendto(feedback, client_addr)
    
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
