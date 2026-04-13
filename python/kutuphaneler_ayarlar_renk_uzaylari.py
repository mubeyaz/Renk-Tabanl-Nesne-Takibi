#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kutuphaneler, Ayarlar ve Renk Uzaylari
Bu modulde renk takip sisteminin merkezi ayarlari tutulur.
"""

import numpy as np

# Takip edilecek renkler HSV uzayinda tanimlanir.
# HSV kullanimi, parlaklik degisimlerinden BGR'ye gore daha az etkilenir.
RENKLER = {
    "Kirmizi": {
        # Kirmizi, HSV cemberinde iki uca bolundugu icin iki aralikla temsil edilir.
        "ranges": [
            (np.array([0, 140, 80]), np.array([10, 255, 255])),
            (np.array([170, 140, 80]), np.array([180, 255, 255])),
        ],
        "BGR": (0, 0, 255),
    },
    "Yesil": {
        "ranges": [(np.array([40, 80, 70]), np.array([85, 255, 255]))],
        "BGR": (0, 255, 0),
    },
    "Mavi": {
        "ranges": [(np.array([95, 120, 70]), np.array([130, 255, 255]))],
        "BGR": (255, 0, 0),
    },
    "Sari": {
        "ranges": [(np.array([18, 120, 120]), np.array([35, 255, 255]))],
        "BGR": (0, 255, 255),
    },
    "Pembe": {
        "ranges": [(np.array([140, 80, 80]), np.array([169, 255, 255]))],
        "BGR": (203, 192, 255),
    },
    "Kahverengi": {
        "ranges": [(np.array([8, 110, 35]), np.array([20, 255, 160]))],
        "BGR": (42, 42, 165),
    },
}

# Tespit edilen kontur alani bu aralikta degilse gorsel gurultu kabul edilir.
MIN_ALAN = 700
MAX_ALAN = 90000

# Kamera acildiginda uygulanacak varsayilan goruntu parametreleri.
KAMERA_GENISLIK = 640
KAMERA_YUKSEKLIK = 480
KAMERA_FPS = 30

# Arayuz metinleri tek yerden yonetilsin diye sabitler halinde tutulur.
PENCERE_BASLIK = "PyQt Renk Takip"
DURUM_HAZIR = "Durum: Hazir"
DURUM_CALISIYOR = "Durum: Kamera calisiyor"
DURUM_DURDURULDU = "Durum: Kamera durduruldu"
DURUM_KAMERA_HATA = "Durum: Kamera acilamadi"
VIDEO_BASLANGIC = "Kamera kapali. Baslat'a basin."
VIDEO_HATA_KAMERA = "HATA: Kamera acilamadi"
VIDEO_HATA_KARE = "HATA: Kare okunamadi"
UST_BILGI_METNI = "PyQt pencere - Kapatmak icin pencereyi kapat"
