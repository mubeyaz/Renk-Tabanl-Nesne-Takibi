#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nesne Tespiti (Kontur) ve Cizim
Bu modulde maske uzerinden kontur bulma, filtreleme ve kutu cizimi yapilir.
"""

import cv2

from goruntu_isleme_filtreleme import (
    cilt_maskesi_olustur,
    maskeyi_iyilestir,
    renk_maskesi_olustur,
)
from kutuphaneler_ayarlar_renk_uzaylari import (
    MAX_ALAN,
    MIN_ALAN,
    RENKLER,
    UST_BILGI_METNI,
)


def frame_isle(frame):
    """Tek bir kareyi isleyip renk bazli kutu ve etiketleri cizer."""
    # Ayna efekti, kullanicinin hareket yonu ile ekrandaki yonu uyumlu hale getirir.
    frame = cv2.flip(frame, 1)

    # Blur, yuksek frekansli gurultuyu azaltarak maske stabilitesini arttirir.
    frame_blur = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)
    cilt_maskesi = cilt_maskesi_olustur(frame_blur)

    for renk_adi, renk_bilgisi in RENKLER.items():
        # Her renk icin ilgili HSV araliklari tek maske haline getirilir.
        mask = renk_maskesi_olustur(hsv, renk_bilgisi["ranges"])

        # Kirmizi tonlarinda cilt kaynakli yalanci pozitifleri azaltmak icin cilt maskesi cikarilir.
        if renk_adi == "Kirmizi":
            mask = cv2.bitwise_and(mask, cv2.bitwise_not(cilt_maskesi))

        mask = maskeyi_iyilestir(mask)

        # Dis konturlar, bagimsiz nesne adaylarini temsil eder.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            alan = cv2.contourArea(contour)
            if alan < MIN_ALAN or alan > MAX_ALAN:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            if h == 0 or w == 0:
                continue

            # Geometrik filtreler asiri ince/uzun veya asiri daginik bolgeleri eler.
            oran = w / float(h)
            doluluk = alan / float(w * h)
            if oran < 0.25 or oran > 4.0:
                continue
            if doluluk < 0.35:
                continue

            # Nesne bulunduysa kutu ve renk adi cizilir.
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
