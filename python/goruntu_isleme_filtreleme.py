#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Goruntu Isleme ve Filtreleme
Bu modulde renk maskesi olusturma ve maskeyi temizleme adimlari bulunur.
"""

import cv2
import numpy as np


def renk_maskesi_olustur(hsv, araliklar):
    """Birden fazla HSV araligini tek bir ikili maskede birlestirir."""
    # Baslangicta tamamen siyah maske olusturulur; her aralik sonucu OR ile eklenir.
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for lower, upper in araliklar:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
    return mask


def cilt_maskesi_olustur(frame):
    """YCrCb renk uzayinda cilt tonlarini yaklasik olarak maskeleyen yardimci fonksiyon."""
    # Kirmizi tespitte cilt tonlarini elemek icin yardimci maske uretilir.
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    lower_skin = np.array([0, 133, 77], dtype=np.uint8)
    upper_skin = np.array([255, 173, 127], dtype=np.uint8)
    skin = cv2.inRange(ycrcb, lower_skin, upper_skin)

    # Kucuk gurultuleri temizlemek ve bosluklari kapatmak icin acma-kapama uygulanir.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, kernel)
    skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, kernel)
    return skin


def maskeyi_iyilestir(mask):
    """Ham maskeyi kontur cikarmaya uygun hale getirmek icin morfolojik filtre uygular."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Acma-kapama, tek piksel gurultuleri azaltir ve nesne butunlugunu artirir.
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Erozyon + dilasyon, kenarlari biraz daha stabil hale getirir.
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask
