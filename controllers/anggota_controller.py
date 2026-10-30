import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView


class AnggotaController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # id_anggota dari baris tabel yang sedang dipilih
        self.id_terpilih = None

        # Binding tombol View -> fungsi Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_update.configure(command=self.perbarui_data)

        # Event klik baris tabel
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        self.muat_data_tabel()

    # READ
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_anggota = self.model.get_all_anggota()

        for anggota in data_anggota:
            self.view.tabel.insert(
                "", "end",
                values=(anggota['id_anggota'], anggota['nama'], anggota['alamat'])
            )

    def bersihkan_form(self):
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_alamat.delete(0, 'end')
        self.id_terpilih = None

    # EVENT: klik baris tabel
    def pilih_baris(self, event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return

        # values = (id_anggota, nama, alamat)
        nilai = self.view.tabel.item(pilihan[0])['values']
        self.id_terpilih = nilai[0]

        self.view.entry_nama.delete(0, 'end')
        self.view.entry_nama.insert(0, nilai[1])
        self.view.entry_alamat.delete(0, 'end')
        self.view.entry_alamat.insert(0, nilai[2])

    # CREATE
    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_anggota(nama, alamat)

        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    # DELETE
    def hapus_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data anggota di tabel yang ingin dihapus!")
            return

        if not messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            return

        berhasil = self.model.delete_anggota(self.id_terpilih)

        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    # UPDATE
    def perbarui_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data anggota di tabel yang ingin diperbarui!")
            return

        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_anggota(self.id_terpilih, nama, alamat)

        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def run(self):
        self.view.mainloop()