#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kamera Kontrolu ve Programin Calistirilmasi
Bu modul kamera kaynak yonetimini ve uygulama giris noktasini icerir.
"""

import sys

import cv2
from PyQt5.QtWidgets import QApplication

from arayuz_gui_tasarimi import RenkTakipPenceresi
from kutuphaneler_ayarlar_renk_uzaylari import (
    KAMERA_FPS,
    KAMERA_GENISLIK,
    KAMERA_YUKSEKLIK,
)


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


def main():
    """Uygulamayi baslatan ana giris fonksiyonu."""
    app = QApplication(sys.argv)
    kamera_yoneticisi = KameraYoneticisi()
    pencere = RenkTakipPenceresi(kamera_yoneticisi)
    pencere.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
