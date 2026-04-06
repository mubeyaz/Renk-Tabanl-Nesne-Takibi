#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renk Tabanlı Nesne Takip Sistemi
Yeşil, Kırmızı, Mavi, Sarı nesneleri algılar ve etrafına kare çizer
"""

import cv2
import numpy as np
import sys
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


def frame_isle(frame):
    frame = cv2.flip(frame, 1)

    frame_blur = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)
    cilt_maskesi = cilt_maskesi_olustur(frame_blur)

    for renk_adi, renk_bilgisi in RENKLER.items():
        mask = renk_maskesi_olustur(hsv, renk_bilgisi["ranges"])

        if renk_adi == "Kirmizi":
            mask = cv2.bitwise_and(mask, cv2.bitwise_not(cilt_maskesi))

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

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
        "PyQt pencere - Kapatmak icin pencereyi kapat",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        1,
    )
    return frame


class RenkTakipPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Renk Takip")
        self.resize(900, 700)
        self.cap = None

        self.video_label = QLabel("Kamera kapali. Baslat'a basin.")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(
            "background-color: #0f172a; color: #e2e8f0; border-radius: 8px;"
        )

        self.durum_label = QLabel("Durum: Hazir")
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
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

        if not self.cap.isOpened():
            self.durum_label.setText("Durum: Kamera acilamadi")
            self.video_label.setText("HATA: Kamera acilamadi")
            return

        self.timer.start(30)
        self.baslat_btn.setEnabled(False)
        self.durdur_btn.setEnabled(True)
        self.durum_label.setText("Durum: Kamera calisiyor")

    def kamerayi_durdur(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.cap = None
        self.baslat_btn.setEnabled(True)
        self.durdur_btn.setEnabled(False)
        self.durum_label.setText("Durum: Kamera durduruldu")
        self.video_label.setPixmap(QPixmap())
        self.video_label.setText("Kamera kapali. Baslat'a basin.")

    def kare_guncelle(self):
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self.video_label.setText("HATA: Kare okunamadi")
            return

        sonuc = frame_isle(frame)
        rgb = cv2.cvtColor(sonuc, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)
        self.video_label.setPixmap(
            pix.scaled(
                self.video_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def closeEvent(self, event):
        self.kamerayi_durdur()
        event.accept()


def main():
    app = QApplication(sys.argv)
    pencere = RenkTakipPenceresi()
    pencere.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
