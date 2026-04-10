# Renk Tabanlı Nesne Takip Sistemi

Bu proje, kameradan alınan görüntüde belirli renkleri gerçek zamanlı olarak tespit eden ve tespit edilen bölgelerin etrafına kutu çizen bir masaüstü uygulamasıdır.

Uygulama, PyQt5 arayüzü ile çalışır; OpenCV ile görüntü işleme yapar ve modüler bir yapıyla geliştirilmiştir.

## Amaç

- Renk tabanlı nesne tespitinin temel prensiplerini göstermek
- HSV renk uzayını kullanarak ışık değişimlerine karşı daha dayanıklı takip yapmak
- Kodun okunabilirliğini ve bakımını kolaylaştırmak için modüler mimari kullanmak

## Özellikler

- Gerçek zamanlı kamera akışı
- Birden fazla renk tespiti:
  - Kırmızı
  - Yeşil
  - Mavi
  - Sarı
  - Pembe
  - Kahverengi
- Kontur tabanlı nesne bulma
- Alan, oran ve doluluk filtresi ile yalancı tespitleri azaltma
- Başlat/Durdur butonlarıyla kolay kontrol
- Durum metinleri ile kullanıcı geri bildirimi

## Kullanılan Teknolojiler

- Python
- OpenCV
- NumPy
- PyQt5

Gereken paketler [python/requirements.txt](python/requirements.txt) dosyasında bulunur.

## Proje Yapısı

- [python/main.py](python/main.py): Uygulamanın giriş noktası
- [python/kutuphaneler_ayarlar_renk_uzaylari.py](python/kutuphaneler_ayarlar_renk_uzaylari.py): Renk aralıkları, eşikler, kamera ve arayüz sabitleri
- [python/goruntu_isleme_filtreleme.py](python/goruntu_isleme_filtreleme.py): Maske oluşturma ve morfolojik filtreleme adımları
- [python/nesne_tespiti_kontur_cizim.py](python/nesne_tespiti_kontur_cizim.py): Kontur bulma, geometri filtreleri, kutu ve etiket çizimi
- [python/arayuz_gui_tasarimi.py](python/arayuz_gui_tasarimi.py): PyQt pencere, butonlar, zamanlayıcı ve görüntü gösterimi
- [python/kamera_kontrol_calistirma.py](python/kamera_kontrol_calistirma.py): Kamera yönetimi ve uygulama çalıştırma akışı

## Mimari Akış

1. Kamera açılır ve kareler okunur.
2. Kare ön işleme alınır:
   - Ayna efekti (flip)
   - Bulanıklaştırma (Gaussian blur)
   - HSV dönüşümü
3. Her renk için maske üretilir.
4. Maske, gürültü azaltma işlemlerinden geçer.
5. Konturlar bulunur ve filtrelenir:
   - Alan
   - En-boy oranı
   - Doluluk
6. Geçerli konturlara kutu ve etiket çizilir.
7. Sonuç kare GUI üzerinde gösterilir.

## Kurulum

1. Proje dizinine geçin.
2. Sanal ortam oluşturun ve aktif edin.
3. Paketleri kurun.

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Not: Kullanılan ortama göre sanal ortam yolu değişebilir.

## Çalıştırma

```bash
cd python
python main.py
```

## Renk Tespiti Ayarları

Renk aralıkları ve genel sabitler [python/kutuphaneler_ayarlar_renk_uzaylari.py](python/kutuphaneler_ayarlar_renk_uzaylari.py) dosyasından yönetilir.

Değiştirilebilecek temel parametreler:

- RENKLER: HSV renk aralıkları
- MIN_ALAN / MAX_ALAN: Kontur alan eşikleri
- KAMERA_GENISLIK / KAMERA_YUKSEKLIK / KAMERA_FPS: Kamera performans parametreleri

## Sık Karşılaşılan Durumlar

1. Kamera açılmıyor
- Başka bir uygulama kamerayı kullanıyor olabilir.
- Sistem izinlerinde terminal/IDE için kamera izni verilmelidir.

2. Renkler zayıf algılanıyor
- Ortam ışığı değişmişse HSV aralıkları yeniden ayarlanmalıdır.
- MIN_ALAN ve MAX_ALAN değerleri hedef nesne boyutuna göre güncellenmelidir.

3. Arayüz açılıyor ama görüntü gelmiyor
- Kamera indeksi (VideoCapture parametresi) farklı olabilir.
- Kamera yöneticisindeki açma adımları kontrol edilmelidir.

## Geliştirme Fikirleri

- Renk kalibrasyon paneli eklemek
- Birden fazla nesneyi ID ile takip etmek
- FPS ve gecikme ölçümü eklemek
- Tespit edilen nesnelerin kaydını tutmak
- Ekran görüntüsü/video kaydı özelliği eklemek

## Hazır Sunum (Doğrudan Kullanıma Uygun)

Bu bölüm, 6 kişilik ekip için doğrudan sunulabilecek şekilde hazırlanmıştır.

### Sunum Süresi ve Akış

1. Yönetici açılış: 2 dakika
2. Konuşmacı 1: 2,5 dakika
3. Konuşmacı 2: 2,5 dakika
4. Konuşmacı 3: 2,5 dakika
5. Konuşmacı 4: 2,5 dakika
6. Konuşmacı 5: 2,5 dakika
7. Canlı demo: 3 dakika
8. Yönetici kapanış ve soru-cevap: 2,5 dakika

Toplam: Yaklaşık 20 dakika

### Slayt 1 - Proje Tanıtımı (Yönetici)

Başlık:
Renk Tabanlı Nesne Takip Sistemi

Konuşma metni:
Merhaba, biz 6 kişilik bir ekip olarak gerçek zamanlı çalışan bir renk tabanlı nesne takip uygulaması geliştirdik. Projemizin temel amacı, kameradan alınan görüntüde belirlenen renkleri tespit etmek ve bu nesneleri kutularla işaretleyerek canlı olarak takip etmek. Bu projede OpenCV ile görüntü işleme, PyQt5 ile masaüstü arayüz ve modüler Python mimarisi kullandık.

### Slayt 2 - Problem ve Hedef (Yönetici)

Başlık:
Neyi Çözüyoruz?

Konuşma metni:
Klasik kamera uygulamalarında nesneleri güvenilir şekilde ayırt etmek zor olabilir. Biz bu sorunu renk tabanlı yaklaşımla çözüyoruz. Hedefimiz, ışık değişimlerine mümkün olduğunca dayanıklı bir sistem kurmak, kodun bakımını kolaylaştırmak ve ekip içinde görevleri net şekilde paylaşılabilir hale getirmekti.

### Slayt 3 - Kütüphaneler, Ayarlar ve Renk Uzayları (Konuşmacı 1)

Dosya:
[python/kutuphaneler_ayarlar_renk_uzaylari.py](python/kutuphaneler_ayarlar_renk_uzaylari.py)

Konuşma metni:
Bu dosya projenin merkezi ayar noktasıdır. Tespit edeceğimiz renklerin HSV aralıkları burada tanımlanır. Kırmızı için iki ayrı aralık kullanıyoruz çünkü HSV renk çemberinde kırmızı hem başlangıç hem bitiş bölümüne düşer. Ayrıca pembe ve kahverengi renklerini de sisteme ekledik. Alan eşikleri, kamera çözünürlüğü ve FPS gibi değerler de bu dosyada tutulduğu için sistemi tek bir yerden kalibre etmek mümkün oluyor.

### Slayt 4 - Görüntü İşleme ve Filtreleme (Konuşmacı 2)

Dosya:
[python/goruntu_isleme_filtreleme.py](python/goruntu_isleme_filtreleme.py)

Konuşma metni:
Bu bölümde ham görüntüyü daha temiz bir veriye dönüştürüyoruz. Önce ilgili renk için maske oluşturuluyor. Sonra morfolojik işlemlerle, yani açma-kapama, erozyon ve dilasyon adımlarıyla gürültü azaltılıyor. Kırmızı renk için ayrıca cilt maskesi kullanarak yalancı pozitifleri düşürüyoruz. Bu adım, kontur tespitine daha sağlam bir giriş verisi sağlıyor.

### Slayt 5 - Nesne Tespiti ve Çizim (Konuşmacı 3)

Dosya:
[python/nesne_tespiti_kontur_cizim.py](python/nesne_tespiti_kontur_cizim.py)

Konuşma metni:
Bu dosyada kontur bulma ve doğrulama aşaması var. Önce maske üzerinden dış konturları çıkarıyoruz. Ardından alan, en-boy oranı ve doluluk gibi geometrik filtrelerle hatalı adayları eliyoruz. Geçerli nesneler için ekranda renk adına uygun kutu çiziliyor ve etiket basılıyor. Böylece kullanıcı hangi renk nesnenin algılandığını anlık olarak görebiliyor.

### Slayt 6 - Arayüz Tasarımı (Konuşmacı 4)

Dosya:
[python/arayuz_gui_tasarimi.py](python/arayuz_gui_tasarimi.py)

Konuşma metni:
Burada PyQt5 tabanlı arayüzü yönetiyoruz. Başlat ve Durdur butonları, durum etiketleri ve canlı görüntü alanı bu dosyada tanımlı. Zamanlayıcı mekanizmasıyla her 30 milisaniyede bir kare güncelleniyor. Ayrıca görüntüyü OpenCV formatından PyQt görüntü formatına doğru şekilde çevirerek stabil bir canlı izleme deneyimi sunuyoruz.

### Slayt 7 - Kamera Kontrolü ve Çalıştırma (Konuşmacı 5)

Dosya:
[python/kamera_kontrol_calistirma.py](python/kamera_kontrol_calistirma.py)

Destek dosyası:
[python/main.py](python/main.py)

Konuşma metni:
Bu katman kamera yaşam döngüsünü yönetir: başlatma, kare okuma ve güvenli kapatma. Kamera yöneticisi sınıfı sayesinde kaynak yönetimi merkezi ve kontrollü hale gelir. Uygulamanın ana giriş noktası olan main fonksiyonu da burada çalışır; QApplication başlatılır, pencere açılır ve olay döngüsü devreye alınır.

### Slayt 8 - Canlı Demo Akışı (Yönetici Moderasyonu)

Demo adımları:
1. Uygulamayı çalıştırın: python main.py
2. Başlat butonuna basın.
3. Kırmızı, yeşil, mavi, sarı, pembe, kahverengi nesneleri sırayla kameraya gösterin.
4. Algılanan nesnelerde kutu ve etiket çıktısını canlı gösterin.
5. Durdur butonuyla kamera akışını sonlandırın.

Konuşma metni:
Şimdi sistemi canlı olarak çalıştırıyoruz. Her renk için kutu ve etiketin doğru şekilde oluştuğunu göreceksiniz. Böylece hem tespit katmanını hem arayüz katmanını birlikte doğrulamış olacağız.

### Slayt 9 - Teknik Değerlendirme ve Riskler (Yönetici)

Başlık:
Güçlü Yönler ve İyileştirme Alanları

Konuşma metni:
Modüler mimari sayesinde kodun bakımını ve görev dağılımını kolaylaştırdık. Ancak ışık koşulları çok değiştiğinde HSV aralıklarının yeniden kalibre edilmesi gerekebilir. Gelecekte otomatik kalibrasyon, çoklu nesne kimlik takibi ve performans ölçüm panelleri eklemeyi planlıyoruz.

### Slayt 10 - Kapanış (Yönetici)

Konuşma metni:
Özetle, gerçek zamanlı çalışan, çok renkli nesne tespiti yapan, modüler ve geliştirilebilir bir sistem ortaya koyduk. Ekip içinde her modül net bir sorumlulukla geliştirildi. Dinlediğiniz için teşekkür ederiz, sorularınızı memnuniyetle alabiliriz.

## Kod Alıntılarıyla Detaylı Sunum Senaryosu

Bu bölümde sunumu daha teknik ve etkileyici yapmak için doğrudan proje kodundan alıntılar verilmiştir. Her alıntının hemen altında, sahnede kullanılabilecek anlatım metni bulunur.

### Konuşmacı 1 - Kütüphaneler, Ayarlar ve Renk Uzayları

Kaynak dosya:
[python/kutuphaneler_ayarlar_renk_uzaylari.py](python/kutuphaneler_ayarlar_renk_uzaylari.py)

Kod alıntısı 1:
```python
RENKLER = {
   "Kirmizi": {
      "ranges": [
         (np.array([0, 140, 80]), np.array([10, 255, 255])),
         (np.array([170, 140, 80]), np.array([180, 255, 255])),
      ],
      "BGR": (0, 0, 255),
   },
   "Pembe": {
      "ranges": [(np.array([140, 80, 80]), np.array([169, 255, 255]))],
      "BGR": (203, 192, 255),
   },
   "Kahverengi": {
      "ranges": [(np.array([8, 90, 40]), np.array([22, 255, 180]))],
      "BGR": (42, 42, 165),
   },
}
```

Sunumda söyle:
Bu kısımda sistemin hangi renkleri hangi HSV aralığında algılayacağını tanımlıyoruz. Kırmızı iki aralıkla tanımlandı çünkü HSV çemberinin iki ucuna yayılıyor. Pembe ve kahverengiyi de burada ekleyerek sistemi genişlettik.

Kod alıntısı 2:
```python
MIN_ALAN = 700
MAX_ALAN = 90000

KAMERA_GENISLIK = 640
KAMERA_YUKSEKLIK = 480
KAMERA_FPS = 30
```

Sunumda söyle:
Bu sabitler sistemin davranışını doğrudan etkiliyor. Alan eşikleri küçük gürültüleri ve aşırı büyük bölgeleri eliyor, kamera ayarları ise performans ve görüntü kararlılığını dengeliyor.

### Konuşmacı 2 - Görüntü İşleme ve Filtreleme

Kaynak dosya:
[python/goruntu_isleme_filtreleme.py](python/goruntu_isleme_filtreleme.py)

Kod alıntısı 1:
```python
def renk_maskesi_olustur(hsv, araliklar):
   mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
   for lower, upper in araliklar:
      mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
   return mask
```

Sunumda söyle:
Burada birden fazla HSV aralığını tek bir maske içinde birleştiriyoruz. Bu yaklaşım, özellikle kırmızı gibi parçalı renk aralıklarında kritik önem taşıyor.

Kod alıntısı 2:
```python
def cilt_maskesi_olustur(frame):
   ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
   lower_skin = np.array([0, 133, 77], dtype=np.uint8)
   upper_skin = np.array([255, 173, 127], dtype=np.uint8)
   skin = cv2.inRange(ycrcb, lower_skin, upper_skin)
```

Sunumda söyle:
Kırmızı tespitinde el veya yüz gibi bölgeler yanlış alarm üretebiliyor. Bu yüzden YCrCb uzayında cilt maskesi oluşturup kırmızı maske ile birlikte kullanıyoruz.

Kod alıntısı 3:
```python
def maskeyi_iyilestir(mask):
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
   mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
   mask = cv2.erode(mask, kernel, iterations=1)
   mask = cv2.dilate(mask, kernel, iterations=1)
   return mask
```

Sunumda söyle:
Bu adımda maskeyi temizliyoruz. Açma-kapama ile gürültüyü azaltıyoruz, erozyon ve dilasyonla da kenarları daha tutarlı hale getiriyoruz.

### Konuşmacı 3 - Nesne Tespiti (Kontur) ve Çizim

Kaynak dosya:
[python/nesne_tespiti_kontur_cizim.py](python/nesne_tespiti_kontur_cizim.py)

Kod alıntısı 1:
```python
frame_blur = cv2.GaussianBlur(frame, (7, 7), 0)
hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)
cilt_maskesi = cilt_maskesi_olustur(frame_blur)
```

Sunumda söyle:
Nesne tespitinden önce görüntüyü yumuşatıp HSV uzayına geçiriyoruz. Böylece renk segmentasyonu daha kararlı oluyor.

Kod alıntısı 2:
```python
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
   alan = cv2.contourArea(contour)
   if alan < MIN_ALAN or alan > MAX_ALAN:
      continue
```

Sunumda söyle:
Burada aday nesneleri kontur olarak çıkarıyoruz. Alan filtresiyle hedefe uygun olmayan bölgeleri doğrudan eliyoruz.

Kod alıntısı 3:
```python
oran = w / float(h)
doluluk = alan / float(w * h)
if oran < 0.25 or oran > 4.0:
   continue
if doluluk < 0.35:
   continue
```

Sunumda söyle:
Sadece alan değil, şekil bilgisi de kullanıyoruz. Aşırı ince-uzun bölgeleri ve içi fazla boş adayları eleyerek doğruluğu artırıyoruz.

Kod alıntısı 4:
```python
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
```

Sunumda söyle:
Bu satırlar kullanıcıya görünen nihai çıktıyı üretiyor. Tespit edilen nesnenin etrafına kutu çizip hangi renk olduğunu etiketliyoruz.

### Konuşmacı 4 - Arayüz (GUI) Tasarımı

Kaynak dosya:
[python/arayuz_gui_tasarimi.py](python/arayuz_gui_tasarimi.py)

Kod alıntısı 1:
```python
self.baslat_btn.clicked.connect(self.kamerayi_baslat)
self.durdur_btn.clicked.connect(self.kamerayi_durdur)
```

Sunumda söyle:
Arayüz tarafında kullanıcı etkileşimini bu bağlantılarla yönetiyoruz. Başlat ve Durdur butonları doğrudan kamera yaşam döngüsüne bağlı.

Kod alıntısı 2:
```python
self.timer = QTimer(self)
self.timer.timeout.connect(self.kare_guncelle)
```

Sunumda söyle:
Canlı görüntü akışını zamanlayıcı ile sürdürüyoruz. Her tetiklemede yeni kare alınıp işleniyor ve arayüze yansıtılıyor.

Kod alıntısı 3:
```python
rgb = sonuc[:, :, ::-1].copy()
h, w, ch = rgb.shape
bytes_per_line = ch * w
qimg = QImage(rgb.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
```

Sunumda söyle:
Burada OpenCV çıktısını PyQt’nin kabul ettiği formata çeviriyoruz. Özellikle tobytes kullanımı, memoryview kaynaklı tip hatalarını engelleyerek görüntü aktarımını stabil hale getiriyor.

### Konuşmacı 5 - Kamera Kontrolü ve Programın Çalıştırılması

Kaynak dosya:
[python/kamera_kontrol_calistirma.py](python/kamera_kontrol_calistirma.py)

Kod alıntısı 1:
```python
if self.cap is None:
   self.cap = cv2.VideoCapture(0)
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, KAMERA_GENISLIK)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, KAMERA_YUKSEKLIK)
   self.cap.set(cv2.CAP_PROP_FPS, KAMERA_FPS)
```

Sunumda söyle:
Kamera başlatma aşamasında çözünürlük ve FPS değerlerini merkezi ayarlardan okuyarak uyguluyoruz. Bu sayede performans ayarları tek yerden kontrol ediliyor.

Kod alıntısı 2:
```python
ret, frame = self.cap.read()
if not ret:
   return None
return frame
```

Sunumda söyle:
Kare okuma başarısızsa sistemi zorlamıyoruz, güvenli şekilde None dönüyoruz. GUI tarafı da bunu yakalayıp kullanıcıya hata mesajı gösteriyor.

Kod alıntısı 3:
```python
app = QApplication(sys.argv)
kamera_yoneticisi = KameraYoneticisi()
pencere = RenkTakipPenceresi(kamera_yoneticisi)
pencere.show()
sys.exit(app.exec_())
```

Sunumda söyle:
Uygulamanın yaşam döngüsü burada başlıyor. Kamera yöneticisini ve pencereyi bağlayıp olay döngüsünü çalıştırıyoruz.

### Yönetici - Bütünleşik Mimari Anlatımı

Kaynak dosyalar:
[python/main.py](python/main.py), [python/arayuz_gui_tasarimi.py](python/arayuz_gui_tasarimi.py), [python/nesne_tespiti_kontur_cizim.py](python/nesne_tespiti_kontur_cizim.py)

Kod alıntısı:
```python
# main.py
from kamera_kontrol_calistirma import main

if __name__ == "__main__":
   main()
```

Sunumda söyle:
Mimariyi tek cümlede şöyle özetleyebiliriz: main başlatır, kamera katmanı kareyi sağlar, işleme katmanı nesneyi bulur, GUI katmanı sonucu kullanıcıya gösterir. Modüler yapı sayesinde ekip içinde paralel geliştirme mümkün oldu.

### Sahnede Kullanılacak Kısa Geçiş Cümleleri

1. Bir dosyadan diğerine geçerken:
Bu kısmı burada çözdük, şimdi bir sonraki modülde bu çıktıyı nasıl kullandığımızı göstereceğiz.

2. Kod alıntısı gösterirken:
Bu satırlar projenin kritik noktası; burada yaptığımız işlem doğrudan algılama kalitesini belirliyor.

3. Demo öncesi:
Şimdi teorik kısmı canlı çıktıyla doğruluyoruz; her renk için kutu ve etiketin gerçek zamanlı oluştuğunu göreceksiniz.

## Lisans

Eğitim ve geliştirme amaçlı örnek proje yapısındadır. Gerekirse bu bölüme kurumunuzun lisans bilgisini ekleyebilirsiniz.
