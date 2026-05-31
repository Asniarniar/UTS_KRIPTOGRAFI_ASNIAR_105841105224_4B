import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

def generate_key(password: str) -> bytes:
    """Mengubah password teks menjadi key 256-bit menggunakan SHA-256"""
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def encrypt_file(input_filename: str, output_filename: str, password: str):
    """Fungsi untuk mengunci/mengenkripsi file DOCX"""
    try:
        key = generate_key(password)
        
        with open(input_filename, 'rb') as f:
            file_data = f.read()
        
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
        
        with open(output_filename, 'wb') as f:
            f.write(iv)
            f.write(encrypted_data)
            
        print(f"\n[SUKSES] File '{input_filename}' berhasil dienkripsi!")
        print(f"[INFO] Hasil enkripsi disimpan sebagai: '{output_filename}'")
    except FileNotFoundError:
        print(f"\n[ERROR] File '{input_filename}' tidak ditemukan. Pastikan nama filenya benar!")
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")

def decrypt_file(input_filename: str, output_filename: str, password: str):
    """Fungsi untuk membuka/mendekripsi file .enc kembali ke DOCX"""
    try:
        key = generate_key(password)
        
        with open(input_filename, 'rb') as f:
            iv = f.read(16)
            encrypted_data = f.read()
            
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        with open(output_filename, 'wb') as f:
            f.write(decrypted_data)
            
        print(f"\n[SUKSES] File '{input_filename}' berhasil didekripsi!")
        print(f"[INFO] File asli dipulihkan sebagai: '{output_filename}'")
    except FileNotFoundError:
        print(f"\n[ERROR] File '{input_filename}' tidak ditemukan!")
    except (ValueError, KeyError):
        print("\n[GAGAL DEKRIPSI] Password salah atau file telah rusak/dimodifikasi!")
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")

# Antarmuka Pengguna Utama (Menu Utama)
def main_menu():
    while True:
        print("\n" + "="*40)
        print("     APLIKASI ENKRIPSI FILE AES (DOCX)    ")
        print("="*40)
        print("1. Enkripsi File (.docx -> .enc)")
        print("2. Dekripsi File (.enc -> .docx)")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            input_file = input("Masukkan nama file DOCX asli (contoh: tugas.docx): ")
            output_file = input("Masukkan nama file hasil enkripsi (contoh: tugas.enc): ")
            password = input("Masukkan password pengunci: ")
            encrypt_file(input_file, output_file, password)
            
        elif pilihan == '2':
            input_file = input("Masukkan nama file terenkripsi (contoh: tugas.enc): ")
            output_file = input("Masukkan nama file hasil pemulihan (contoh: hasil_pulih.docx): ")
            password = input("Masukkan password pembuka: ")
            decrypt_file(input_file, output_file, password)
            
        elif pilihan == '3':
            print("\nTerima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("\nPilihan tidak valid. Silakan pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main_menu()