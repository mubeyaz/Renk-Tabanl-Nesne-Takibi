#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renk Tabanlı Nesne Takip Sistemi
Yeşil, Kırmızı, Mavi, Sarı nesneleri algılar ve etrafına kare çizer
"""

import cv2
import numpy as np

# Renk tanımlamaları (HSV)
RENKLER = {
    "Kirmizi": {
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
}

MIN_ALAN = 700
MAX_ALAN = 90000


def renk_maskesi_olustur(hsv, araliklar):
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for lower, upper in araliklar:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
    return mask


def cilt_maskesi_olustur(frame):
    # YCrCb uzayında cilt tonu aralığı.
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    lower_skin = np.array([0, 133, 77], dtype=np.uint8)
    upper_skin = np.array([255, 173, 127], dtype=np.uint8)
    skin = cv2.inRange(ycrcb, lower_skin, upper_skin)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, kernel)
    skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, kernel)
    return skin


def main():
    # Kamerayı aç
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("HATA: Kamera açılamadı!")
        return
    
    # Kamera ayarları
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("Renk Tabanlı Nesne Takip Sistemi başlatılıyor...")
    print("Çıkmak için: 'q' tuşuna basın")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("HATA: Kare okunamadı")
            break
        
        # Kareyi flip et (daha iyi görüş için)
        frame = cv2.flip(frame, 1)
        
        # Gürültüyü azalt ve ardından HSV'ye dönüştür.
        frame_blur = cv2.GaussianBlur(frame, (7, 7), 0)
        hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)
        cilt_maskesi = cilt_maskesi_olustur(frame_blur)
        
        # Her renk için nesne bul
        for renk_adi, renk_bilgisi in RENKLER.items():
            # Maske oluştur (tek veya çoklu HSV aralığı).
            mask = renk_maskesi_olustur(hsv, renk_bilgisi["ranges"])

            # Kırmızıda cilt bölgelerini çıkar (yüz/ten yanlış pozitiflerini azaltır).
            if renk_adi == "Kirmizi":
                mask = cv2.bitwise_and(mask, cv2.bitwise_not(cilt_maskesi))
            
            # Morfolojik işlemler (gürültü azalt)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=1)
            
            # Kontur bul
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Her kontürü işle
            for contour in contours:
                alan = cv2.contourArea(contour)
                
                # Alan filtresi
                if alan < MIN_ALAN or alan > MAX_ALAN:
                    continue
                
                # Bounding box
                x, y, w, h = cv2.boundingRect(contour)

                # Geometrik kalite filtresi
                if h == 0 or w == 0:
                    continue
                oran = w / float(h)
                doluluk = alan / float(w * h)
                if oran < 0.25 or oran > 4.0:
                    continue
                if doluluk < 0.35:
                    continue
                
                # Kare çiz
                cv2.rectangle(frame, (x, y), (x + w, y + h), renk_bilgisi["BGR"], 2)
                
                # Renk adını yaz
                cv2.putText(frame, renk_adi, (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, renk_bilgisi["BGR"], 2)
                
                # Alan bilgisini yaz
                cv2.putText(frame, f"Alan: {alan:.0f}", (x, y + h + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, renk_bilgisi["BGR"], 1)
        
        # Yardım metni
        cv2.putText(frame, "q: Cik", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Ekranda göster
        cv2.imshow("Nesne Takip Sistemi", frame)
        
        # Tuş kontrolü
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\nUygulama kapatılıyor...")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Sistem kapatıldı.")


if __name__ == "__main__":
    main()
