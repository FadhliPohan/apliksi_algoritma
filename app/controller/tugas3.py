from pydantic import BaseModel
from fastapi import APIRouter, Query
from typing import Optional, Literal
from collections import Counter
import unicodedata

router = APIRouter()  # Router khusus untuk tugas1

def jumlah_huruf(text: str, letters_to_count: str) -> dict:
    """
    Menghitung jumlah kemunculan huruf yang ditentukan dalam teks (case-insensitive).
    Huruf yang dihitung adalah huruf yang diberikan dalam parameter `letters_to_count`.

    Return:
        dict dengan kunci huruf-huruf yang diminta dan hasil dalam kalimat.
    """
    # Normalisasi agar aksen/diakritik konsisten, lalu ambil hanya huruf
    normalized = unicodedata.normalize("NFKD", text)
    letters = [ch.upper() for ch in normalized if ch.isalpha()]

    # Hitung frekuensi semua huruf
    counts = Counter(letters)

    # Ambil hanya huruf yang diminta, jika tidak ada -> 0
    result = {k: counts.get(k, 0) for k in letters_to_count.upper()}

    # Membuat kalimat yang lebih manusiawi
    result_sentence = "Jumlah kemunculan huruf dalam teks yang diberikan:\n"
    for huruf, jumlah in result.items():
        result_sentence += f"Huruf {huruf} muncul sebanyak {jumlah} kali.\n"
    
    return {"jumlah_huruf": result_sentence, "details": result}

@router.get("/hitung_huruf")
async def jumlah_huruf_endpoint(
    text: str = Query("MATEMATIKA", description="Teks bebas untuk dihitung jumlah huruf."),
    letters_to_count: str = Query("MATIK", description="Huruf-huruf yang ingin dihitung (misalnya 'A', 'B', 'C').")
):
    # Menghitung jumlah huruf yang ditentukan dan mengembalikan hasilnya dalam kalimat
    result = jumlah_huruf(text, letters_to_count)
    return {
        "input": text,
        "huruf_yang_dihitung": letters_to_count,
        "hasil": result["jumlah_huruf"],
        "details": result["details"]
    }


def _normalize_letters(text: str):
    # Normalisasi aksen (é -> e) lalu ambil hanya huruf, uppercase untuk case-insensitive
    normalized = unicodedata.normalize("NFKD", text)
    return [ch.upper() for ch in normalized if ch.isalpha()]

def hitung_semua_huruf(text: str) -> dict:
    """
    Hitung semua huruf yang muncul pada 'text' (case-insensitive, hanya A-Z).
    Return: dict {'A': nA, 'B': nB, ...} untuk huruf yang muncul (nilai > 0).
    """
    letters = _normalize_letters(text)
    counts = Counter(letters)
    # Hanya kembalikan huruf yang benar-benar muncul (count > 0)
    return dict(counts)

def _format_sentence(counts: dict) -> str:
    """
    Buat kalimat ringkas berbasis hasil hitung.
    Contoh: "Huruf A: 4x; B: 2x; C: 1x."
    """
    if not counts:
        return "Tidak ada huruf yang terdeteksi pada teks."
    parts = [f"Huruf {k} muncul {v} kali" for k, v in counts.items()]
    return "; ".join(parts) + "."
@router.get("/hitung_huruf_otomatis")
async def hitung_huruf_otomatis(
    text: str = Query("Aku suka Matematika! 123", description="Teks bebas—semua huruf akan dihitung otomatis."),
    sort_by: Literal["jumlah", "huruf"] = Query("jumlah", description="Urutkan berdasarkan 'jumlah' atau 'huruf'."),
    order: Literal["desc", "asc"] = Query("desc", description="Arah pengurutan hasil."),
    top: Optional[int] = Query(None, ge=1, description="Ambil Top-N hasil teratas (opsional).")
):
    """
    Menghitung SEMUA huruf yang muncul di 'text' secara otomatis.
    - Case-insensitive, hanya huruf (simbol/angka diabaikan).
    - Bisa diurutkan berdasarkan jumlah/huruf.
    - Bisa dibatasi Top-N.
    """
    counts = hitung_semua_huruf(text)

    # Urutkan
    if sort_by == "jumlah":
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=(order == "desc"))
    else:  # sort_by == "huruf"
        sorted_items = sorted(counts.items(), key=lambda x: x[0], reverse=(order == "desc"))

    # Top-N bila diminta
    if top is not None:
        sorted_items = sorted_items[:top]

    # Susun kembali ke dict terurut untuk response rapi
    ordered_counts = {k: v for k, v in sorted_items}

    # Kalimat ringkas
    sentence = _format_sentence(ordered_counts)

    return {
        "input": text,
        "unique_letters": len(counts),
        "sorted_by": sort_by,
        "order": order,
        "top": top,
        "details": ordered_counts,
        "summary": sentence
    }
