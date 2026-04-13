#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renk tabanli nesne takip sistemi tek dosya surumu.
Bu dosya, projedeki tum modulleri tek giris noktasinda toplar.
"""

import sys

import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


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
    "Pembe": {
        "ranges": [(np.array([140, 80, 80]), np.array([169, 255, 255]))],
        "BGR": (203, 192, 255),
    },
    "Kahverengi": {
        "ranges": [(np.array([8, 110, 35]), np.array([20, 255, 160]))],
        "BGR": (42, 42, 165),
    },
}

MIN_ALAN = 700
MAX_ALAN = 90000

KAMERA_GENISLIK = 640
KAMERA_YUKSEKLIK = 480
KAMERA_FPS = 30

PENCERE_BASLIK = "PyQt Renk Takip"
DURUM_HAZIR = "Durum: Hazir"
DURUM_CALISIYOR = "Durum: Kamera calisiyor"
DURUM_DURDURULDU = "Durum: Kamera durduruldu"
DURUM_KAMERA_HATA = "Durum: Kamera acilamadi"
VIDEO_BASLANGIC = "Kamera kapali. Baslat'a basin."
VIDEO_HATA_KAMERA = "HATA: Kamera acilamadi"
VIDEO_HATA_KARE = "HATA: Kare okunamadi"
UST_BILGI_METNI = "PyQt pencere - Kapatmak icin pencereyi kapat"


def renk_maskesi_olustur(hsv, araliklar):
    """Birden fazla HSV araligini tek bir ikili maskede birlestirir."""
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for lower, upper in araliklar:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
    return mask


def cilt_maskesi_olustur(frame):
    """YCrCb renk uzayinda cilt tonlarini yaklasik olarak maskeleyen yardimci fonksiyon."""
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    lower_skin = np.array([0, 133, 77], dtype=np.uint8)
    upper_skin = np.array([255, 173, 127], dtype=np.uint8)
    skin = cv2.inRange(ycrcb, lower_skin, upper_skin)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, kernel)
    skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, kernel)
    return skin


def maskeyi_iyilestir(mask):
    """Ham maskeyi kontur cikarmaya uygun hale getirmek icin morfolojik filtre uygular."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask


def cilt_maskesini_cikar(mask, cilt_maskesi):
    """Cilt tonlariyla cakisan bolgeleri maskeden cikarir."""
    return cv2.bitwise_and(mask, cv2.bitwise_not(cilt_maskesi))


def frame_isle(frame):
    """Tek bir kareyi isleyip renk bazli kutu ve etiketleri cizer."""
    frame = cv2.flip(frame, 1)
    frame_blur = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)
    cilt_maskesi = cilt_maskesi_olustur(frame_blur)

    for renk_adi, renk_bilgisi in RENKLER.items():
        mask = renk_maskesi_olustur(hsv, renk_bilgisi["ranges"])
        if renk_adi in ("Kirmizi", "Kahverengi"):
            mask = cilt_maskesini_cikar(mask, cilt_maskesi)

        mask = maskeyi_iyilestir(mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            alan = cv2.contourArea(contour)
            if alan < MIN_ALAN or alan > MAX_ALAN:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            if h == 0 or w == 0:
                continue

            oran = w / float(h)
            doluluk = alan / float(w * h)
            if oran < 0.25 or oran > 4.0:
                continue
            if doluluk < 0.35:
                continue

            cv2.rectangle(frame, (x, y), (x + w, y + h), renk_bilgisi["BGR"], 2)
            cv2.putText(
                frame,
                renk_adi,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                renk_bilgisi["BGR"],
                2,
            )

    cv2.putText(
        frame,
        UST_BILGI_METNI,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        1,
    )
    return frame


class KameraYoneticisi:
    """OpenCV kamera acma/okuma/kapatma islemlerini tek noktada yoneten sinif."""

    def __init__(self):
        self.cap = None

    def baslat(self):
        """Varsayilan kamerayi acmaya calisir."""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, KAMERA_GENISLIK)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, KAMERA_YUKSEKLIK)
            self.cap.set(cv2.CAP_PROP_FPS, KAMERA_FPS)

        if not self.cap.isOpened():
            self.durdur()
            return False
        return True

    def kare_al(self):
        """Kameradan bir kare okur; hata durumunda None doner."""
        if self.cap is None or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def durdur(self):
        """Kamera kaynagini guvenli sekilde serbest birakir."""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.cap = None


class RenkTakipPenceresi(QMainWindow):
    """Renk takip uygulamasinin ana penceresi."""

    def __init__(self, kamera_yoneticisi):
        super().__init__()
        self.kamera = kamera_yoneticisi

        self.setWindowTitle(PENCERE_BASLIK)
        self.resize(900, 700)

        self.video_label = QLabel(VIDEO_BASLANGIC)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(
            "background-color: #0f172a; color: #e2e8f0; border-radius: 8px;"
        )

        self.durum_label = QLabel(DURUM_HAZIR)
        self.durum_label.setStyleSheet("font-size: 14px; color: #0f172a;")

        self.baslat_btn = QPushButton("Baslat")
        self.baslat_btn.setCursor(Qt.PointingHandCursor)
        self.baslat_btn.clicked.connect(self.kamerayi_baslat)
        self.baslat_btn.setStyleSheet(
            "QPushButton {background:#16a34a;color:white;padding:10px 20px;"
            "border:none;border-radius:8px;font-weight:600;}"
            "QPushButton:disabled {background:#86efac;color:#14532d;}"
        )

        self.durdur_btn = QPushButton("Durdur")
        self.durdur_btn.setCursor(Qt.PointingHandCursor)
        self.durdur_btn.clicked.connect(self.kamerayi_durdur)
        self.durdur_btn.setEnabled(False)
        self.durdur_btn.setStyleSheet(
            "QPushButton {background:#dc2626;color:white;padding:10px 20px;"
            "border:none;border-radius:8px;font-weight:600;}"
            "QPushButton:disabled {background:#fecaca;color:#7f1d1d;}"
        )

        ana_widget = QWidget()
        ana_widget.setStyleSheet("background-color: #f8fafc;")
        duzen = QVBoxLayout(ana_widget)
        duzen.setContentsMargins(16, 16, 16, 16)
        duzen.setSpacing(12)

        buton_duzeni = QHBoxLayout()
        buton_duzeni.setSpacing(10)
        buton_duzeni.addWidget(self.baslat_btn)
        buton_duzeni.addWidget(self.durdur_btn)
        buton_duzeni.addStretch()

        duzen.addWidget(self.durum_label)
        duzen.addLayout(buton_duzeni)
        duzen.addWidget(self.video_label)
        self.setCentralWidget(ana_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.kare_guncelle)

    def kamerayi_baslat(self):
        """Kamera akisini baslatir ve arayuz durumunu gunceller."""
        if not self.kamera.baslat():
            self.durum_label.setText(DURUM_KAMERA_HATA)
            self.video_label.setText(VIDEO_HATA_KAMERA)
            return

        self.timer.start(30)
        self.baslat_btn.setEnabled(False)
        self.durdur_btn.setEnabled(True)
        self.durum_label.setText(DURUM_CALISIYOR)

    def kamerayi_durdur(self):
        """Kamera akisini durdurur ve arayuzu baslangic durumuna alir."""
        if self.timer.isActive():
            self.timer.stop()
        self.kamera.durdur()

        self.baslat_btn.setEnabled(True)
        self.durdur_btn.setEnabled(False)
        self.durum_label.setText(DURUM_DURDURULDU)
        self.video_label.setPixmap(QPixmap())
        self.video_label.setText(VIDEO_BASLANGIC)

    def kare_guncelle(self):
        """Kameradan gelen kareyi isleyip etikette gosterir."""
        frame = self.kamera.kare_al()
        if frame is None:
            self.video_label.setText(VIDEO_HATA_KARE)
            return

        sonuc = frame_isle(frame)
        rgb = sonuc[:, :, ::-1].copy()
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)

        self.video_label.setPixmap(
            pix.scaled(
                self.video_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def closeEvent(self, event):
        """Pencere kapatilirken kaynaklarin temizlenmesini garanti eder."""
        self.kamerayi_durdur()
        event.accept()


def main():
    """Uygulamayi baslatan ana giris fonksiyonu."""
    app = QApplication(sys.argv)
    kamera_yoneticisi = KameraYoneticisi()
    pencere = RenkTakipPenceresi(kamera_yoneticisi)
    pencere.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()