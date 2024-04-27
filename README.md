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
   Masukkan library yang dibutuhkan untuk membuat program ini
    ```sh
    import socket
    import random
    import time
    ```

    Warna - warna yang digunakan dalam program ini
    
    ```sh
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
    ```
    | Bahasa Inggris | Bahasa Indonesia |
    | ------ | ------ |
    | red | merah |
    | blue | biru |
    | green | hijau |
    | yellow | kuning |
    | orange | orange |
    | purple | ungu |
    | brown | coklat |
   
Dalam fungsi send_color, server melakukan iterasi melalui setiap klien dalam clients. Setiap kali mengunjungi klien, server memilih secara acak sebuah indeks warna baru dari daftar warna dalam bahasa Inggris. Kemudian, mengambil kata warna yang sesuai dengan indeks yang dipilih tersebut. Pesan yang berisi kata warna tersebut dikirim ke klien menggunakan soket. Setelah itu, server memperbarui nilai yang terkait dengan klien dalam clients dengan indeks warna yang baru dikirim. Ini memungkinkan server untuk melacak warna mana yang telah dikirim ke setiap klien.
   
    ```sh
    def send_color(sock, clients):
        for client_addr, _ in clients.items():
            color_index = random.randint(0, len(colors_en) - 1)
            color_en = colors_en[color_index]
            message = color_en.encode()
            sock.sendto(message, client_addr)
            print("Sent color:", color_en, "to", client_addr)
            clients[client_addr] = color_index  # Simpan indeks warna yang dikirim ke klien
       ```
       
Fungsi check_answer bertanggung jawab untuk memeriksa jawaban yang diberikan oleh klien terhadap warna yang dikirimkan oleh server. Pertama, indeks warna yang dikirimkan ke klien diambil dari clients yang merupakan dictionary yang menyimpan alamat klien beserta indeks warna yang telah dikirimkan. Indeks ini digunakan untuk mengambil kata warna dalam bahasa Inggris (color_en). Selanjutnya, kata warna tersebut diterjemahkan ke dalam bahasa Indonesia menggunakan color_translations, menghasilkan color_id. Fungsi kemudian membandingkan jawaban klien dengan terjemahan warna tersebut. Jika jawaban klien sesuai dengan terjemahan, nilai feedback diatur menjadi b'100', yang menandakan jawaban benar, jika tidak, nilai feedback diatur menjadi b'0', menandakan jawaban salah. Feedback kemudian dikirim kembali ke klien melalui soket sock dengan menggunakan alamat klien client_addr.

    ```sh
    def check_answer(sock, client_addr, answer, clients):
        color_en = colors_en[clients[client_addr]]
        color_id = color_translations[color_en]
        if answer.lower() == color_id:
            feedback = b'100'  # Jika jawaban benar, berikan nilai 100
        else:
            feedback = b'0'  # Jika jawaban salah, berikan nilai 0
        sock.sendto(feedback, client_addr)
       ```

Fungsi main() bertanggung jawab atas logika utama dari server. Pertama, server memulai dengan mengikat socket UDP ke alamat tertentu dan kemudian memulai loop tak terbatas. Setiap 10 detik, server mengirimkan kata warna acak ke semua klien yang terhubung menggunakan fungsi send_color(). Selanjutnya, server menunggu jawaban dari klien. Jika dalam waktu 5 detik tidak ada jawaban, server akan melanjutkan ke langkah berikutnya. Jika ada jawaban dari klien, server akan memeriksanya dengan menggunakan fungsi check_answer() dan memberikan feedback. Proses ini terus berulang sampai server ditutup.

    ```sh
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
        ```
Penjelasan:
Code tersebut merupakan implementasi server sederhana dalam protokol UDP yang mengirimkan kata warna acak dalam bahasa Inggris ke klien setiap 10 detik. Server menerima jawaban dari klien, memeriksa jawaban tersebut, dan memberikan feedback berupa nilai 100 jika jawaban benar dan nilai 0 jika jawaban salah. Proses pengiriman kata warna dan penerimaan jawaban dari klien dilakukan secara bersamaan dalam loop tak terbatas, di mana server menunggu selama 5 detik untuk menerima jawaban dari klien sebelum melanjutkan ke iterasi berikutnya. Setelah selesai, socket server ditutup.

2. Client.py
   ```sh
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
   ```
   
