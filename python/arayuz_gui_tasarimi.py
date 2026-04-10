#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arayuz (GUI) Tasarimi
Bu modulde PyQt pencere bilesenleri, butonlar ve goruntu gosterimi tanimlanir.
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kutuphaneler_ayarlar_renk_uzaylari import (
    DURUM_CALISIYOR,
    DURUM_DURDURULDU,
    DURUM_HAZIR,
    DURUM_KAMERA_HATA,
    PENCERE_BASLIK,
    VIDEO_BASLANGIC,
    VIDEO_HATA_KAMERA,
    VIDEO_HATA_KARE,
)
from nesne_tespiti_kontur_cizim import frame_isle


class RenkTakipPenceresi(QMainWindow):
    """Renk takip uygulamasinin ana penceresi."""

    def __init__(self, kamera_yoneticisi):
        super().__init__()
        self.kamera = kamera_yoneticisi

        self.setWindowTitle(PENCERE_BASLIK)
        self.resize(900, 700)

        # Video alani canli goruntuyu ya da durum mesajlarini gosterir.
        self.video_label = QLabel(VIDEO_BASLANGIC)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(
            "background-color: #0f172a; color: #e2e8f0; border-radius: 8px;"
        )

        # Durum metni, kullaniciya kamera/uygulama durumunu net sekilde aktarir.
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

        # Timer, kameradan periyodik kare alip GUI'nin akici kalmasini saglar.
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
        # PyQt5 bazi ortamlarda numpy memoryview'i dogrudan kabul etmez;
        # bu nedenle goruntuyu contiguous RGB baytlarina ceviriyoruz.
        rgb = sonuc[:, :, ::-1].copy()  # BGR -> RGB
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
