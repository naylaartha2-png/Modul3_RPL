from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()
    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()


# ----------------------------------------------------------------------
# Tugas 3: Unit Test untuk get_all_buku()
# ----------------------------------------------------------------------
def test_get_all_buku_berhasil():
    model = BukuModel()

    # Mock koneksi dan cursor agar tidak menyentuh database asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Data palsu yang seolah-olah dikembalikan oleh database
    data_palsu = [
        {"id_buku": 1, "judul": "Pemrograman Python", "penulis": "Andi", "tahun_terbit": 2023},
        {"id_buku": 2, "judul": "Basis Data", "penulis": "Budi", "tahun_terbit": 2024},
    ]
    mock_cursor.fetchall.return_value = data_palsu

    # Eksekusi fungsi yang diuji
    hasil = model.get_all_buku()

    # Verifikasi: query dijalankan sekali dan hasil sama dengan data palsu
    mock_cursor.execute.assert_called_once()
    assert hasil == data_palsu
    assert len(hasil) == 2
    assert hasil[0]["judul"] == "Pemrograman Python"