import sqlite3  # Mengimpor modul SQLite3 untuk mengelola database
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Mengimpor elemen-elemen GUI dari Tkinter

# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuat koneksi ke database SQLite bernama 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()  # Membuat cursor untuk menjalankan perintah SQL
    # Membuat tabel 'nilai_siswa' jika belum ada, dengan kolom sesuai spesifikasi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    # Kolom ID dengan auto increment, Nama siswa sebagai teks, Nilai biologi, fisika, dan inggris sebagai integer, Prediksi fakultas sebagai teks
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk mengambil data dari database
def fetch_data():
    # Membuka koneksi ke database
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()  # Membuat cursor
    # Mengambil semua data dari tabel 'nilai_siswa'
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()  # Menyimpan hasil pengambilan data ke dalam 'rows'
    conn.close()  # Menutup koneksi ke database
    return rows  # Mengembalikan data yang diambil

# Fungsi untuk menyimpan data ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    # Menyisipkan data ke tabel 'nilai_siswa'
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    # Memperbarui data berdasarkan ID
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    # Menghapus data berdasarkan ID
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    # Membandingkan nilai untuk menentukan fakultas yang sesuai
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menambahkan data baru ke database
def submit():
    try:
        nama = nama_var.get()  # Mengambil nilai input nama
        biologi = int(biologi_var.get())  # Mengambil nilai input biologi dan mengonversinya ke integer
        fisika = int(fisika_var.get())  # Mengambil nilai input fisika dan mengonversinya ke integer
        inggris = int(inggris_var.get())  # Mengambil nilai input Inggris dan mengonversinya ke integer

        if not nama:  # Mengecek apakah nama kosong
            raise Exception("Nama siswa tidak boleh kosong.")

        # Menghitung prediksi fakultas berdasarkan nilai
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Menyimpan data ke database
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Menghapus input pada form
        populate_table()  # Memperbarui tabel
    except ValueError as e:  # Menangkap error jika input tidak valid
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data yang sudah ada
def update():
    try:
        if not selected_record_id.get():  # Mengecek apakah ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mendapatkan ID data yang dipilih
        nama = nama_var.get()  # Mengambil nilai input nama
        biologi = int(biologi_var.get())  # Mengambil nilai input biologi
        fisika = int(fisika_var.get())  # Mengambil nilai input fisika
        inggris = int(inggris_var.get())  # Mengambil nilai input Inggris

        if not nama:  # Mengecek apakah nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.")

        # Menghitung prediksi fakultas berdasarkan nilai
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Memperbarui data di database
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Menampilkan pesan sukses
        clear_inputs()  # Menghapus input
        populate_table()  # Memperbarui tabel
    except ValueError as e:  # Menangkap error jika input tidak valid
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data dari database
def delete():
    try:
        if not selected_record_id.get():  # Mengecek apakah ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mendapatkan ID data yang dipilih
        delete_database(record_id)  # Menghapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Menampilkan pesan sukses
        clear_inputs()  # Menghapus input
        populate_table()  # Memperbarui tabel
    except ValueError as e:  # Menangkap error jika input tidak valid
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus nilai input di form
def clear_inputs():
    nama_var.set("")  # Menghapus input nama
    biologi_var.set("")  # Menghapus input biologi
    fisika_var.set("")  # Menghapus input fisika
    inggris_var.set("")  # Menghapus input Inggris
    selected_record_id.set("")  # Menghapus ID data yang dipilih

# Fungsi untuk menampilkan data di tabel
def populate_table():
    # Menghapus semua data yang ada di tabel
    for row in tree.get_children():
        tree.delete(row)
    # Menambahkan data dari database ke tabel
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi form berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mendapatkan data yang dipilih di tabel
        selected_row = tree.item(selected_item)['values']  # Mendapatkan nilai dari data yang dipilih

        # Mengisi form dengan data yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:  # Menangkap error jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

BG_COLOR = "#FDE2E4"  # Latar belakang utama
BTN_COLOR = "#FADADD"  # Warna tombol
TXT_COLOR = "#F5B7B1"  # Warna teks dan border
FONT_COLOR = "#722F37"  # Warna teks utama

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")
root.configure(bg=BG_COLOR)

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Membuat label dan entry untuk input data
Label(root, text="Nama Siswa", bg=BG_COLOR, fg=FONT_COLOR).grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var, bg=TXT_COLOR, fg=FONT_COLOR).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi", bg=BG_COLOR, fg=FONT_COLOR).grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var, bg=TXT_COLOR, fg=FONT_COLOR).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika", bg=BG_COLOR, fg=FONT_COLOR).grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var, bg=TXT_COLOR, fg=FONT_COLOR).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris", bg=BG_COLOR, fg=FONT_COLOR).grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var, bg=TXT_COLOR, fg=FONT_COLOR).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol-tombol aksi
Button(root, text="Add", bg=BTN_COLOR, fg=FONT_COLOR, command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", bg=BTN_COLOR, fg=FONT_COLOR, command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", bg=BTN_COLOR, fg=FONT_COLOR, command=delete).grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

# Event untuk mengisi form berdasarkan data yang dipilih di tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Memperbarui tabel
populate_table()

# Menjalankan loop utama Tkinter
root.mainloop()