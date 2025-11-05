from pydantic import BaseModel
from fastapi import APIRouter
from typing import List
import math
from itertools import combinations

router = APIRouter()  # Router khusus untuk tugas1

# Pydantic model untuk request body JourneyRequest
class JourneyRequest(BaseModel):
    stops: List[int]  # Daftar titik SPBU
    tank_capacity: int  # Kapasitas tangki bensin
    destination: int  # Jarak tujuan

# Fungsi Brute Force untuk menemukan pemberhentian minimal
def brute_force_fuel_stop(stops, tank_capacity, destination):
    min_stops = []  # Menyimpan rute pemberhentian yang optimal
    min_stop_count = math.inf  # Menyimpan jumlah pemberhentian minimum yang ditemukan
    
    # Menambahkan titik tujuan ke dalam daftar pemberhentian
    stops.append(destination)
    
    # Mencoba setiap kombinasi pemberhentian
    for i in range(1, len(stops)):  # Mulai dari 1 pemberhentian hingga semua pemberhentian
        # Mencoba setiap kombinasi memilih i SPBU
        for combination in combinations(stops, i):
            current_position = 0  # Posisi awal
            stop_count = 0  # Hitung jumlah pemberhentian
            valid_combination = True
            for stop in combination:
                # Jika jarak tempuh dari posisi terakhir ke SPBU lebih dari kapasitas tangki, kombinasi ini tidak valid
                if stop - current_position > tank_capacity:
                    valid_combination = False
                    break
                current_position = stop
                stop_count += 1
            # Cek apakah posisi terakhir mencapai tujuan dan valid
            if valid_combination and current_position == destination:
                if stop_count < min_stop_count:
                    min_stop_count = stop_count
                    min_stops = list(combination)
    
    return min_stops

# Fungsi untuk menentukan Big O, Big Theta, dan Big Omega
def calculate_complexities():
    # Fungsi waktu yang diberikan: T(n) = 4n^3 + 5n^2 + 7n + 3
    def T(n):
        return 4 * n**3 + 5 * n**2 + 7 * n + 3

    # Big O (upper bound)
    # Dominasi terbesar adalah n^3, maka T(n) = O(n^3)
    big_o = "O(n^3)"

    # Big Theta (tight bound)
    # Karena n^3 adalah dominan, T(n) = Θ(n^3)
    big_theta = "Θ(n^3)"

    # Big Omega (lower bound)
    # T(n) tidak akan lebih kecil dari n^3 pada n besar, jadi T(n) = Ω(n^3)
    big_omega = "Ω(n^3)"

    return big_o, big_theta, big_omega

# Endpoint untuk menghitung pemberhentian minimal dengan Brute Force
@router.post("/perjalanan")
async def perjalanan(request: JourneyRequest):
    # Mengambil data dari body request
    stops = request.stops
    tank_capacity = request.tank_capacity
    destination = request.destination
    
    # Memanggil fungsi untuk mencari pemberhentian optimal menggunakan DP
    optimal_stops = brute_force_fuel_stop(stops, tank_capacity, destination)

    # Menyiapkan respons
    response = {
        "bagaimana_kita_menempuh_tempat_pemberhentian": "Kita harus berhenti di SPBU yang jaraknya tidak lebih dari kapasitas tangki bensin dan mencapai tujuan dengan jumlah pemberhentian sesedikit mungkin.",
        "penyelesaian_algoritma_bruteforce": "Algoritma Brute Force mencoba semua kombinasi pemberhentian, sementara Dynamic Programming menyimpan hasil perhitungan intermediate untuk menghindari perhitungan ulang.",
        "kompleksitas_waktu_bruteforce": "Brute Force memiliki kompleksitas waktu O(2^n), sedangkan dengan Dynamic Programming, kompleksitasnya menjadi O(n^2).",
        "optimal_stops": optimal_stops
    }

    return response

# Endpoint untuk menghitung kompleksitas dari fungsi waktu
@router.get("/kompleksitas")
async def kompleksitas():
    big_o, big_theta, big_omega = calculate_complexities()

    # Mengembalikan hasil kompleksitas dalam response
    return {
        "big_o": big_o,
        "big_theta": big_theta,
        "big_omega": big_omega
    }
