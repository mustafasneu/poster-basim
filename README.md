# Poster Basım

Bir görseli **oranını bozmadan** A4 sayfalara böler ve baskıya hazır tek bir PDF üretir.
Sayfaları kesip yapıştırdığınızda tek büyük poster elde edersiniz.

**Windows, Linux ve macOS** üzerinde aynı şekilde çalışır. Kurulum gerektirmez: program
ilk açılışta eksik bileşenleri kendi klasörüne indirir, sisteminizdeki Python'a hiçbir şey
yazmaz.

![Program arayüzü](manuel/gorseller/05_iyilestirme.png)

## Ne yapar

- **Sünme yok** — görsel, sayfa matrisinin oranına doldurularak değil, oranı korunarak
  yerleştirilir; artan alan beyaz bırakılır. Daireler basık, yüzler uzamış çıkmaz.
- **Link ile resim alma** — resim internetteyse indirmenize gerek yok; adresi yapıştırın,
  program indirip yükler.
- **Tek ölçek garantisi** — kenar parçalarında eksik kalan bindirme payı beyazla
  tamamlanır, böylece bütün sayfalar birebir aynı ölçekle basılır ve parçalar tutar.
- **Çakışma payı (bindirme)** — komşu sayfalarda tekrar basılan şerit sayesinde kesip
  yapıştırırken tolerans kalır.
- **Görüntü iyileştirme** — keskinlik, kontrast, renk canlılığı ve parlaklık sürgüleri;
  önizleme anında güncellenir, PDF her zaman tam çözünürlükten üretilir.
- **Baskı kalitesi** — parçalar JPEG kalite 95, renk alt örneklemesi kapalı (4:4:4),
  300 DPI etiketiyle kaydedilir.

## Kurulum

Tek şart, bilgisayarda **Python 3.10 veya üstü** bulunmasıdır. Linux ve macOS'ta zaten
kuruludur; Windows'ta yoksa [python.org](https://www.python.org/downloads/) üzerinden bir
kez kurulur (kurulum ekranında **“Add python.exe to PATH”** ve **“tcl/tk and IDLE”**
işaretli kalsın).

**Terminal gerekmez.** [ZIP olarak indirin](https://github.com/mustafasneu/poster-basim/archive/refs/heads/main.zip),
çıkarın, sonra kendi sisteminizin dosyasına çift tıklayın:

| İşletim sistemi | Programı aç             | Masaüstü kısayolu koy (bir kez) |
| --------------- | ----------------------- | ------------------------------- |
| Windows 10 / 11 | `Poster Basim.bat`     | `Kisayol Olustur.bat`           |
| macOS 11+       | `Poster Basim.command` | `Kisayol Olustur.command`       |
| Linux           | `calistir.sh`           | `kisayol-olustur.sh`            |

macOS ilk açılışta “geliştirici doğrulanamadı” derse: dosyaya **sağ tık → Aç → Aç**.

Terminali tercih ederseniz:

```bash
git clone https://github.com/mustafasneu/poster-basim.git
cd poster-basim
python3 kurulum.py          # masaüstü kısayolu (--kaldir ile geri alınır)
./calistir.sh               # programı başlat
```

Kısayol her sistemin kendi biçiminde oluşur: Windows'ta `.lnk`, macOS'ta `.command`,
Linux'ta `.desktop` (uygulama menüsüne de eklenir).

İlk açılış, bileşenler indirildiği için ~30 saniye sürer ve internet gerektirir; sonraki
açılışlar anındadır.

## Kullanım

1. **Bilgisayardan Resim Seç** ile görseli yükleyin (`.jpg .jpeg .png .bmp .webp .tif .tiff`)
   ya da **İnternetten Link ile Al** ile resmin web adresini yapıştırın.
2. **Sütun** ve **satır** sayısını girerek poster ölçüsünü belirleyin (örn. 4 × 2 = 8 A4).
3. Gerekirse **çakışma payını** ayarlayın — kesip yapıştıracaksanız 20–30 iyi gelir.
4. Sürgülerle keskinlik / kontrast / renk ayarını yapın.
5. **Oranı Koru ve Hazır PDF Üret** deyin. Çıktı, masaüstünüzdeki
   `Poster_Parcalari` klasörüne tarih damgalı bir alt klasör olarak düşer:
   yazdırılacak PDF ve her parçanın JPEG hali.

> [!IMPORTANT]
> Yazdırırken **“Sayfaya Sığdır / Fit to Page”** seçeneğini **işaretlemeyin**. Her zaman
> **“Gerçek Boyut / Actual Size”** ya da **%100 ölçek** ile yazdırın. Aksi halde sayfalar
> farklı ölçekte basılır ve parçalar birleşmez.

## Ayrıntılı kılavuz

Ekran görüntülü tam kullanım kılavuzu depoda: **[KULLANIM_KILAVUZU.pdf](KULLANIM_KILAVUZU.pdf)**
(aynı içeriğin HTML hali: [KULLANIM_KILAVUZU.html](KULLANIM_KILAVUZU.html)). Kurulum,
adım adım kullanım, yazdırma ayarları, kesme-birleştirme ve sık karşılaşılan durumlar
orada anlatılıyor.

## Dosyalar

| Dosya                   | İşlevi                                              |
| ----------------------- | --------------------------------------------------- |
| `poster_bolme.py`       | Programın kendisi (arayüz + bölme + PDF)            |
| `kurulum.py`            | Masaüstü kısayolu oluşturucu (üç sistem)            |
| `calistir.sh`           | Linux / macOS başlatıcısı                            |
| `Poster Basim.bat`     | Windows başlatıcısı                                  |
| `Poster Basim.command` | macOS başlatıcısı                                    |
| `manuel/`               | Kılavuzu ve ekran görüntülerini üreten betikler      |

## Teknik

Python 3.10+, Tkinter (arayüz), [Pillow](https://python-pillow.org/) (görüntü işleme),
[ReportLab](https://www.reportlab.com/) (PDF). Bağımlılıklar programın yanındaki `.venv`
klasörüne kurulur; sistem Python'ı değiştirilmez.

## Lisans

MIT — bkz. [LICENSE](LICENSE).

---

powered by Omer OZTURK
