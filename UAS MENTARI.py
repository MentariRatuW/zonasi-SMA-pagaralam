import turtle
import math
import tkinter as tk
from tkinter import messagebox  

# ----------------- Setup Turtle -----------------
screen = turtle.Screen()
screen.title("Zonasi Sekolah SMA – Kota Pagar Alam")
screen.bgcolor("white")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# ----------------- Data Sekolah -----------------
schools = [
    (-200, 150, "SMA 1 PAGAR ALAM"),
    (0,   200, "SMA 2 PAGAR ALAM"),
    (200, 150, "SMA 3 PAGAR ALAM"),
    (-100,-100,"SMA 4 PAGAR ALAM"),
    (100,-120,"SMA 5 PAGAR ALAM"),
    (0,     0,"SMA 6 PAGAR ALAM"),
    (-350,150,"SMA 1 MUHAMMADIYAH")
]

# ----------------- Fungsi Gambar -----------------
def draw_node(x, y, label, color, radius=20, font_size=10):
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.color("black", color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()
    pen.penup()
    pen.goto(x, y - 5)
    pen.write(label, align="center", font=("Arial", font_size, "bold"))

def draw_edge(x1, y1, x2, y2, label=""):
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.color("gray")
    pen.width(2)
    pen.goto(x2, y2)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        pen.penup()
        pen.goto(mx + 10, my + 10)
        pen.write(label, align="center", font=("Arial", 9, "normal"))
    pen.width(1)
    pen.penup()

def draw_radius_zone(x, y, radius=200):
    pen.penup()
    pen.goto(x, y - radius)
    pen.color("red")
    pen.pendown()
    pen.circle(radius)
    pen.penup()

def draw_legend():
    base_x, base_y = -350, -260
    spacing = 30
    legend_items = [
        ("skyblue",   "Sekolah"),
        ("lightgreen","Rumah Siswa"),
        ("gold",      "Sekolah Terdekat"),
        ("gray",      "Jarak Zonasi"),
        ("red",       "Radius 200 m")
    ]
    for i, (color, label) in enumerate(legend_items):
        pen.penup()
        pen.goto(base_x, base_y - i * spacing)
        pen.color("black", color)
        pen.begin_fill()
        pen.circle(10)
        pen.end_fill()
        pen.goto(base_x + 25, base_y - i * spacing - 5)
        pen.write(f"= {label}", font=("Arial", 10, "normal"))

# ----------------- Logika Zonasi -----------------
def distance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def proses_zonasi(nama, x, y):
    pen.clear()

    # 1) Gambar semua sekolah
    for sx, sy, sname in schools:
        draw_node(sx, sy, sname, "skyblue", font_size=11)

    # 2) Gambar rumah siswa
    draw_node(x, y, nama, "lightgreen", font_size=10)

    # 3) Hitung jarak terdekat & daftar dalam radius
    nearest = None
    min_dist = float("inf")
    dalam_radius = []

    for sx, sy, sname in schools:
        d = distance(x, y, sx, sy)
        if d <= 200:
            dalam_radius.append((sx, sy, sname, d))
            draw_radius_zone(sx, sy, 200)
        if d < min_dist:
            min_dist = d
            nearest = (sx, sy, sname, d)

    dalam_radius.sort(key=lambda item: item[3])


    # 4) Tandai sekolah terdekat
    if nearest:
        draw_node(nearest[0], nearest[1], nearest[2], "gold", font_size=11)
        draw_edge(x, y, nearest[0], nearest[1], f"{nearest[3]} m")

    # 5) Tambah garis ke sekolah lain dalam radius
    khusus_list = []
    for sx, sy, sname, d in dalam_radius:
        if (sx, sy, sname) != nearest[:3]:
            draw_edge(x, y, sx, sy, f"{d} m")
            khusus_list.append(f"{sname} ({d} m)")

    # 6) Tentukan status
    if nearest[3] <= 200:
        status = "Lulus Zonasi"
    elif len(dalam_radius) > 1:
        status = "Zonasi Khusus"
    elif len(dalam_radius) == 1:
        status = "Lulus Menengah"
    else:
        status = "Lulus Jalur Non‑Zonasi"

    # 7) Gambar legenda
    draw_legend()

    # 8) Cetak hasil di console (opsional)
    print("\n--- HASIL ZONASI ---")
    print(f"Nama Siswa        : {nama}")
    print(f"Koordinat Rumah   : ({x}, {y})")
    print(f"Sekolah Terdekat  : {nearest[2]}")
    print(f"Jarak ke Sekolah  : {nearest[3]} meter")
    print(f"Status Zonasi     : {status}")
    if khusus_list:
        print("Masuk Radius Lain :")
        for info in khusus_list:
            print(f"  • {info}")

    # 9) Tampilkan kotak informasi (tidak meminta input lagi)
    messagebox.showinfo(
        title="Hasil Zonasi",
        message=(
            f"Nama: {nama}\n"
            f"Sekolah Terdekat: {nearest[2]}\n"
            f"Jarak: {nearest[3]} meter\n"
            f"Status: {status}"
            + ("\n\nJuga masuk radius:\n" + "\n".join(khusus_list) if khusus_list else "")
        )
    )


try:
    nama = screen.textinput("Input Nama", "Masukkan nama siswa:")
    if not nama:
        raise ValueError("Nama tidak boleh kosong.")
    x = int(screen.textinput("Koordinat X", "Masukkan koordinat X rumah:"))
    y = int(screen.textinput("Koordinat Y", "Masukkan koordinat Y rumah:"))
    proses_zonasi(nama, x, y)
except ValueError as e:
    turtle.bye()
    print(f"Input Error: {e}")
finally:
    turtle.done()
