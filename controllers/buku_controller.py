import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role

        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Menyimpan id_buku dari baris tabel yang sedang dipilih
        self.id_terpilih = None

        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_logout.configure(command=self.logout)

        # Event klik pada baris tabel
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan semua tombol manipulasi
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_hapus.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert(
                "", "end",
                values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit'])
            )

    def bersihkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.id_terpilih = None

    # ------------------------------------------------------------------
    # EVENT: baris tabel diklik
    # ------------------------------------------------------------------
    def pilih_baris(self, event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return

        # values = (id_buku, judul, penulis, tahun_terbit)
        nilai = self.view.tabel.item(pilihan[0])['values']
        self.id_terpilih = nilai[0]

        self.view.entry_judul.delete(0, 'end')
        self.view.entry_judul.insert(0, nilai[1])
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_penulis.insert(0, nilai[2])
        self.view.entry_tahun.delete(0, 'end')
        self.view.entry_tahun.insert(0, nilai[3])

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def simpan_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data buku di tabel yang ingin dihapus!")
            return

        yakin = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if not yakin:
            return

        berhasil = self.model.delete_buku(self.id_terpilih)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def perbarui_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data buku di tabel yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_buku(self.id_terpilih, judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def logout(self):
        # Import di dalam method untuk menghindari circular import
        from controllers.auth_controller import AuthController

        self.view.destroy()
        AuthController().run()

    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()