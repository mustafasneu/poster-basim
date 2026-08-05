"""Ekran görüntülerini gömerek tek dosyalık resimli kullanım kılavuzu üretir.

Kullanım:  .venv/bin/python manuel/manuel_uret.py
Çıktı:     KULLANIM_KILAVUZU.html  (görseller içine gömülü, tek başına taşınır)
"""

from __future__ import annotations

import base64
import io
import os

from PIL import Image

PROJE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GORSEL = os.path.join(PROJE, "manuel", "gorseller")
CIKTI = os.path.join(PROJE, "KULLANIM_KILAVUZU.html")

IMZA = "powered by Omer OZTURK"


def gomulu(ad: str, en_fazla_genislik: int = 1100, kalite: int = 80) -> str:
    """PNG'yi küçültüp JPEG olarak base64 data-URI'ye çevirir (dosya tek parça kalsın)."""
    with Image.open(os.path.join(GORSEL, ad)) as im:
        im = im.convert("RGB")
        if im.width > en_fazla_genislik:
            oran = en_fazla_genislik / im.width
            im = im.resize((en_fazla_genislik, int(im.height * oran)), Image.LANCZOS)
        tampon = io.BytesIO()
        im.save(tampon, "JPEG", quality=kalite, optimize=True, subsampling=0)
    return "data:image/jpeg;base64," + base64.b64encode(tampon.getvalue()).decode("ascii")


def sekil(ad: str, baslik: str, aciklama: str = "", genislik: int = 1100) -> str:
    alt = f"<figcaption>{baslik}{(' — ' + aciklama) if aciklama else ''}</figcaption>"
    return (
        f'<figure><img src="{gomulu(ad, genislik)}" alt="{baslik}" loading="lazy">{alt}</figure>'
    )


GOVDE = f"""
<div class="container">

<header>
  <h1>📐 Poster Bölücü — Resimli Kullanım Kılavuzu</h1>
  <p class="ozet">Bir görseli oranını bozmadan A4 sayfalara böler, baskıya hazır tek bir PDF
  üretir. Sayfaları kesip yapıştırdığınızda tek büyük poster elde edersiniz.
  Bu kılavuzdaki bütün ekran görüntüleri programın kendisi çalıştırılarak alınmıştır.</p>
</header>

<div class="kutu kutu-ok">
  <strong>Kurulum gerekmiyor.</strong> Program ilk açılışta eksik bileşenleri (Pillow,
  ReportLab) kendi klasörüne kurar; siz hiçbir şey yüklemezsiniz. Masaüstü kısayolu
  varsa <b>“Poster Bölücü” simgesine çift tıklamanız</b> yeterlidir.
  Kısayol yoksa program klasöründe bir kez <code>python3 kurulum.py</code> çalıştırın
  (Windows'ta <code>python kurulum.py</code>).
</div>

<p>Program <b>Windows, macOS ve Linux</b> üzerinde aynı şekilde çalışır. Kısayol
kullanmadan başlatmak isterseniz, kendi sisteminizin satırındaki dosyaya çift tıklayın:</p>

<table>
  <tr><th>İşletim sistemi</th><th>Çift tıklanacak dosya</th><th>Terminalden</th></tr>
  <tr><td><b>Windows</b> 10 / 11</td><td><code>Poster Bolucu.bat</code></td>
      <td><code>py -3 poster_bolme.py</code></td></tr>
  <tr><td><b>macOS</b> 11+</td><td><code>Poster Bolucu.command</code></td>
      <td><code>./calistir.sh</code></td></tr>
  <tr><td><b>Linux</b></td><td><code>calistir.sh</code></td>
      <td><code>./calistir.sh</code></td></tr>
</table>

<p>Tek şart, bilgisayarda <b>Python 3.10 veya üstü</b> bulunmasıdır — Linux ve macOS'ta
zaten kuruludur, Windows'ta yoksa <code>python.org</code> üzerinden bir kez kurulur.</p>

<h2 id="genel">1. Program açıldığında</h2>
<p>Pencere iki bölümden oluşur: solda <b>ayar paneli</b>, sağda <b>önizleme alanı</b>.
Resim seçilene kadar alttaki iki buton pasiftir (soluk görünür) — bu normaldir.</p>
{sekil("01_baslangic.png", "Açılış ekranı", "sol panel ayarlar, sağ panel önizleme")}

<h2 id="resim">2. Adım 1 — Resim seçme</h2>
<p><code>Bilgisayardan Resim Seç</code> düğmesine basın. Açılan pencerede
<b>Directory</b> kutusundan klasöre gidin, dosyayı çift tıklayın ya da seçip
<b>Open</b>'a basın.</p>
<p>Desteklenen biçimler: <code>.jpg .jpeg .png .bmp .webp .tif .tiff</code>.
Telefonla çekilmiş fotoğrafların yön bilgisi otomatik düzeltilir.</p>
{sekil("02_dosya_secme.png", "Dosya seçme penceresi", "sistemin standart Tk penceresidir")}

<div class="kutu kutu-bilgi">
  <b>Hangi çözünürlük yeterli?</b> Kaba ölçü: her A4 sayfa için yaklaşık
  <b>1000 piksel genişlik</b> hedefleyin. 3×2 poster için ~3000 × 2000 piksel iyi sonuç verir.
  Daha düşük çözünürlükte baskıda pikselleşme görünür; keskinlik sürgüsü bunu bir miktar
  toparlar ama yok etmez.
</div>

<h2 id="onizleme">3. Adım 2 — Önizleme</h2>
<p>Resim yüklendiğinde dosya adı sol panelde, kaynak çözünürlük ise sağ altta yazar.
Önizleme hız için küçültülmüş kopyadır; <b>PDF her zaman tam çözünürlükten üretilir</b>.</p>
{sekil("03_resim_yuklendi.png", "Resim yüklendikten sonra", "sağ altta kaynak çözünürlük bilgisi")}

<h2 id="bolme">4. Adım 3 — Poster ölçüsünü belirleme</h2>
{sekil("04b_bolme_paneli.png", "Bölme ayarları", "", 620)}
<table>
  <tr><th>Ayar</th><th>Ne işe yarar</th><th>Öneri</th></tr>
  <tr><td><b>Sütun Sayısı (X)</b></td><td>Yatayda yan yana gelecek A4 sayısı</td><td>3–4</td></tr>
  <tr><td><b>Satır Sayısı (Y)</b></td><td>Dikeyde alt alta gelecek A4 sayısı</td><td>2–3</td></tr>
  <tr><td><b>Sayfa Yönü</b></td><td>Kâğıdın yazıcıya veriliş yönü</td>
      <td>Geniş görsellerde <b>Yatay</b>, uzun görsellerde <b>Dikey</b></td></tr>
  <tr><td><b>Çakışma Payı</b></td><td>Komşu sayfalarda tekrar basılan bindirme şeridi</td>
      <td><b>15</b> (kesip yapıştıracaksanız 20–30)</td></tr>
</table>

<p>Yaklaşık poster ölçüsü (çakışma payı kadar birkaç milimetre küçülür):</p>
<table>
  <tr><th>Matris</th><th>Yön</th><th>Kâğıt</th><th>Yaklaşık poster ölçüsü</th></tr>
  <tr><td>2 × 2</td><td>Yatay</td><td>4 A4</td><td>~58 × 41 cm</td></tr>
  <tr><td>3 × 2</td><td>Yatay</td><td>6 A4</td><td>~86 × 41 cm</td></tr>
  <tr><td>4 × 2</td><td>Yatay</td><td>8 A4</td><td>~115 × 41 cm</td></tr>
  <tr><td>2 × 3</td><td>Dikey</td><td>6 A4</td><td>~41 × 86 cm</td></tr>
  <tr><td>3 × 4</td><td>Dikey</td><td>12 A4</td><td>~61 × 115 cm</td></tr>
</table>

<div class="kutu kutu-bilgi">
  <b>Resim oranı ile matris oranı tutmuyorsa ne olur?</b> Program görseli asla germez;
  matris alanına ortalar ve artan yerleri <b>beyaz</b> bırakır. Bu beyaz şeritler kenar
  sayfalarda çıkar, kesilerek atılabilir. Beyaz kalmasını istemiyorsanız matrisi resmin
  oranına yaklaştırın (örneğin 2:1 bir görsel için 4×2 yatay).
</div>

<h2 id="iyilestirme">5. Adım 4 — Görüntü iyileştirme</h2>
<p>Dört sürgü doğrudan önizlemeye yansır; değişiklik anında görünür. Baskı, ekrandan daha
mat çıktığı için hafif kontrast ve canlılık artışı genellikle işe yarar.</p>
{sekil("05b_surgu_paneli.png", "İyileştirme sürgüleri", "", 620)}
<table>
  <tr><th>Sürgü</th><th>Aralık</th><th>Ne yapar</th><th>Baskı için öneri</th></tr>
  <tr><td>Detay Netliği</td><td>1.0 – 4.0</td><td>Kenar keskinliği + detay filtresi</td>
      <td>1.5 – 2.5 (fazlası halkalanma yapar)</td></tr>
  <tr><td>Dinamik Kontrast</td><td>0.5 – 2.5</td><td>Açık/koyu ayrımı</td><td>1.1 – 1.4</td></tr>
  <tr><td>Renk Canlılığı</td><td>0.5 – 2.5</td><td>Renk doygunluğu</td><td>1.2 – 1.5</td></tr>
  <tr><td>Genel Parlaklık</td><td>0.5 – 2.0</td><td>Toplam aydınlık</td><td>1.0 – 1.2</td></tr>
</table>
<p><code>Ayarları Sıfırla</code> dört sürgüyü de 1.0'a döndürür.</p>
{sekil("05_iyilestirme.png", "İyileştirme uygulanmış hali", "sürgüler sağa alındığında önizleme anında güncellenir")}

<h2 id="uretim">6. Adım 5 — PDF üretme</h2>
<p><code>Oranı Koru ve Hazır PDF Üret</code> düğmesine basın. Alt satırda
“Parça üretiliyor: 3 / 6” gibi ilerleme görünür; büyük görsellerde bu birkaç saniye sürer.
Bitince özet penceresi açılır.</p>
{sekil("06_tamamlandi.png", "Üretim tamamlandı penceresi", "çıktı klasörünün tam yolunu gösterir")}
<p>Pencereyi <b>OK</b> ile kapattıktan sonra <code>Çıktı Klasörünü Aç</code> düğmesi
etkinleşir; dosya yöneticisini doğrudan o klasörde açar.</p>
{sekil("07_bitis_durumu.png", "Üretim sonrası ana ekran", "alt satırda üretilen PDF adı yazar")}

<h2 id="cikti">7. Çıktı klasöründe ne var?</h2>
<p>Her üretim, tarih-saat damgalı ayrı bir klasöre yazılır; eski çıktıların üzerine
<b>asla</b> yazılmaz.</p>
<pre><code>Masaüstü/
└── Bolu_Parcalanmis_Resimler/
    └── Poster_OranKorumali_20260805_100535/
        ├── Oran_Korumali_Baski_20260805_100535.pdf   ← yazdırılacak dosya
        ├── parca_satir1_sutun1.jpg                   ← tek tek parçalar
        ├── parca_satir1_sutun2.jpg
        └── ...</code></pre>
<p>Normalde sadece PDF'i yazdırmanız yeterlidir. JPEG parçalar, tek bir sayfayı yeniden
bastırmak veya başka bir programda kullanmak isterseniz durur.</p>
{sekil("09_a4_sayfa_ornegi.png", "PDF'in ilk sayfası", "her sayfa tek bir parçayı taşır", 900)}

<h2 id="yazdirma">8. Yazdırma ayarları (en kritik adım)</h2>
<div class="kutu kutu-uyari">
  <strong>⚠️ “Sayfaya Sığdır / Fit to Page” seçeneğini KAPATIN.</strong><br>
  Yazdırma penceresinde ölçeklendirmeyi <b>“Gerçek Boyut (Actual Size)”</b> veya
  <b>“Ölçek: %100”</b> yapın. Sığdırma açık kalırsa her sayfa biraz farklı küçülür ve
  parçalar birleşmez.
</div>
<ul>
  <li><b>Kâğıt boyutu:</b> A4</li>
  <li><b>Yön:</b> programda seçtiğinizle aynı (Yatay/Dikey)</li>
  <li><b>Kenar boşluğu:</b> mümkün olan en küçük değer (“kenarlıksız” varsa idealdir)</li>
  <li><b>Kalite:</b> fotoğraf / yüksek</li>
</ul>

<h2 id="birlestirme">9. Kesme ve birleştirme</h2>
<p>Program her sayfaya, komşusuyla ortak olan bir <b>bindirme şeridi</b> basar. Bu şerit
sayesinde parçalar üst üste bindirilerek hizalanır.</p>
<ol>
  <li>Sayfaları satır satır yere veya masaya dizin (sol üstten sağa doğru).</li>
  <li>Her sayfanın <b>sağ</b> ve <b>alt</b> kenarındaki bindirme şeridini kesmeyin;
      <b>sol</b> ve <b>üst</b> kenarındaki beyaz boşluğu kesin.</li>
  <li>Kesilmiş kenarı, komşu sayfanın deseniyle çakışacak şekilde bindirin; desen tutunca
      arkadan bantlayın.</li>
  <li>En dıştaki beyaz kenarları en son, poster bittiğinde düzeltin.</li>
</ol>
<p>Doğru yapıldığında sonuç kesintisiz olur — aşağıdaki görsel, üretilen 6 parçanın
yeniden birleştirilmiş halidir (daireler yuvarlak, çizgiler sürekli):</p>
{sekil("08_montaj_dogrulama.png", "6 parçanın birleştirilmiş hali", "ek yerlerinde kayma veya sünme yok")}

<h2 id="sorun">10. Sık karşılaşılan durumlar</h2>
<table>
  <tr><th>Durum</th><th>Sebep / Çözüm</th></tr>
  <tr><td>Parçalar birleşmiyor, kayıyor</td>
      <td>Yazdırırken “Sayfaya Sığdır” açık kalmış. %100 ölçekle yeniden yazdırın.</td></tr>
  <tr><td>Kenarlarda beyaz şeritler var</td>
      <td>Resmin oranı seçtiğiniz matrise uymuyor. Matrisi değiştirin ya da beyazı kesin.</td></tr>
  <tr><td>Baskı bulanık / pikselli</td>
      <td>Kaynak çözünürlük düşük. Sayfa sayısını azaltın veya daha büyük bir görsel kullanın.</td></tr>
  <tr><td>Renkler soluk çıkıyor</td>
      <td>Renk Canlılığı 1.3, Kontrast 1.2 deneyin; mat kâğıt her zaman ekrandan sönük basar.</td></tr>
  <tr><td>Düğmeler soluk / basılmıyor</td>
      <td>Henüz resim seçilmemiştir. Önce 2. adımı yapın.</td></tr>
  <tr><td>Büyük resimde program donmuş gibi</td>
      <td>Donmadı; alt satırdaki “Parça üretiliyor: n / m” ilerlemesini izleyin.</td></tr>
  <tr><td><b>Windows:</b> çift tıklayınca pencere açılmıyor</td>
      <td>Python kurulu değil. <code>python.org</code> üzerinden kurun; kurulumda
          “Add python.exe to PATH” ve “tcl/tk and IDLE” işaretli kalsın.</td></tr>
  <tr><td><b>macOS:</b> “geliştirici doğrulanamadı” uyarısı</td>
      <td>Dosyaya sağ tıklayıp <b>Aç</b> deyin ve bir kez onaylayın; sonraki açılışlarda
          sormaz. Kod imzalı bir uygulama değil, düz bir betiktir.</td></tr>
  <tr><td><b>macOS:</b> <code>.command</code> dosyası açılmıyor</td>
      <td>Terminalde bir kez: <code>chmod +x "Poster Bolucu.command"</code></td></tr>
  <tr><td><b>Linux:</b> “tkinter bulunamadı” uyarısı</td>
      <td>Bir kez: <code>sudo apt install -y python3-tk</code> (Fedora:
          <code>sudo dnf install -y python3-tkinter</code>).</td></tr>
  <tr><td>İlk açılış uzun sürüyor</td>
      <td>Yalnızca ilk seferde bileşenler indirilir (~30 sn). Sonraki açılışlar anındadır.</td></tr>
</table>

<h2 id="teknik">11. Teknik notlar</h2>
<ul>
  <li><b>Sünme yok:</b> Görsel, sayfa matrisinin oranına <i>doldurularak değil</i>, oranı
      korunarak yerleştirilir; artan alan beyaz bırakılır.</li>
  <li><b>Tek ölçek garantisi:</b> Kenar parçalarında eksik kalan bindirme payı beyazla
      tamamlanır; böylece bütün parçalar aynı piksel boyutunda üretilir ve tüm sayfalar
      birebir aynı ölçekle basılır.</li>
  <li><b>Kalite:</b> Parçalar JPEG kalite 95, renk alt örneklemesi kapalı (4:4:4),
      300 DPI etiketiyle kaydedilir.</li>
  <li><b>Kullanılan kütüphaneler:</b> Pillow (görüntü işleme), ReportLab (PDF), Tkinter (arayüz).</li>
  <li><b>Çalıştığı sistemler:</b> Windows 10/11, Linux ve macOS. Aynı dosyalar üç sistemde
      de çalışır; masaüstü kısayolu <code>kurulum.py</code> ile her sistemde oluşturulur.</li>
  <li><b>Program dosyaları:</b> <code>poster_bolme.py</code> (program),
      <code>kurulum.py</code> (kısayol oluşturucu), <code>Poster Bolucu.bat</code> /
      <code>Poster Bolucu.command</code> / <code>calistir.sh</code> (başlatıcılar),
      <code>.venv/</code> (bağımlılıklar, ilk açılışta oluşur).</li>
  <li><b>Kaynak kodu:</b> <code>github.com/mustafasneu/poster-bolucu</code></li>
</ul>

<h2 id="kurulum">12. Kurulum — başka bir bilgisayara taşıma</h2>
<p>Program tek bir klasörden ibarettir. Klasörü kopyalayın ya da
<code>github.com/mustafasneu/poster-bolucu</code> adresinden indirin; üç sistemde de
aşağıdaki iki adım yeterlidir.</p>

<h3>Adım 1 — Python'un bulunması</h3>
<table>
  <tr><th>Sistem</th><th>Yapılacak</th></tr>
  <tr><td><b>Windows</b></td>
      <td><code>python.org/downloads</code> → Python 3 kurun. Kurulum ekranında
          <b>“Add python.exe to PATH”</b> ve <b>“tcl/tk and IDLE”</b> işaretli kalsın.</td></tr>
  <tr><td><b>macOS</b></td>
      <td>Genelde kuruludur. Arayüz açılmazsa bir kez:
          <code>brew install python-tk</code></td></tr>
  <tr><td><b>Linux</b></td>
      <td>Kuruludur. Arayüz açılmazsa bir kez:
          <code>sudo apt install -y python3-tk</code> (Fedora:
          <code>sudo dnf install -y python3-tkinter</code>, Arch:
          <code>sudo pacman -S --needed tk</code>)</td></tr>
</table>

<h3>Adım 2 — Kısayolu oluşturma</h3>
<p>Program klasöründe bir kez şunu çalıştırın; masaüstüne çift tıklanabilir bir simge
koyar (Windows'ta <code>.lnk</code>, macOS'ta <code>.command</code>, Linux'ta
<code>.desktop</code>):</p>
<pre><code>python3 kurulum.py</code></pre>
<p>Windows'ta komut <code>python kurulum.py</code> biçimindedir. Kısayolu kaldırmak için
<code>python3 kurulum.py --kaldir</code>.</p>

<div class="kutu kutu-ok">
  <strong>Pillow ve ReportLab'ı elle kurmanıza gerek yok.</strong> Program ilk açılışta
  kendi klasöründe bir <code>.venv</code> ortamı oluşturup bu iki bileşeni oraya indirir;
  sisteminizdeki Python'a hiçbir şey yazmaz. Bu yüzden ilk açılış ~30 saniye sürer,
  sonrakiler anında açılır. Programı silmek için klasörü ve kısayolu silmek yeterlidir.
</div>

<div class="kutu kutu-bilgi">
  <b>İnternetsiz kurulum:</b> Bileşenlerin inebilmesi için ilk açılışta internet gerekir.
  İnternetsiz bir bilgisayara taşıyacaksanız, çalışan makinedeki <code>.venv</code>
  klasörünü değil, şu komutla hazırlanan tekerlek dosyalarını taşıyın:
  <code>pip download pillow reportlab -d paketler</code>, sonra hedef makinede
  <code>pip install --no-index --find-links paketler pillow reportlab</code>.
</div>

<footer>
  <span>{IMZA}</span>
</footer>

</div>
"""

SAYFA = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Poster Bölücü — Resimli Kullanım Kılavuzu</title>
<style>
  :root {{
    --ana: #2563eb; --zemin: #f1f5f9; --kart: #ffffff; --metin: #1e293b;
    --kenar: #e2e8f0; --soluk: #64748b;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.65; color: var(--metin); background: var(--zemin);
    margin: 0; padding: 24px 16px;
  }}
  .container {{
    max-width: 980px; margin: 0 auto; background: var(--kart);
    padding: 40px; border-radius: 14px; box-shadow: 0 4px 16px rgba(15,23,42,.08);
  }}
  header h1 {{ color: var(--ana); margin: 0 0 10px; font-size: 1.9rem; }}
  .ozet {{ color: var(--soluk); margin-top: 0; }}
  h2 {{
    color: var(--ana); margin-top: 44px; padding-bottom: 8px;
    border-bottom: 2px solid var(--kenar); font-size: 1.35rem;
  }}
  h3 {{ margin-top: 26px; margin-bottom: 6px; font-size: 1.08rem; color: var(--metin); }}
  figure {{ margin: 22px 0; }}
  figure img {{
    width: 100%; height: auto; border: 1px solid var(--kenar);
    border-radius: 8px; display: block;
  }}
  figcaption {{ color: var(--soluk); font-size: .9rem; margin-top: 8px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 18px 0; font-size: .96rem; }}
  th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--kenar);
            vertical-align: top; }}
  th {{ background: #f8fafc; }}
  code {{ background: #eef2ff; padding: 2px 6px; border-radius: 4px;
          font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .92em; }}
  pre {{ background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 8px;
         overflow-x: auto; }}
  pre code {{ background: none; color: inherit; padding: 0; }}
  .kutu {{ padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 20px 0; }}
  .kutu-ok {{ background: #ecfdf5; border-left: 4px solid #10b981; }}
  .kutu-bilgi {{ background: #eff6ff; border-left: 4px solid var(--ana); }}
  .kutu-uyari {{ background: #fffbeb; border-left: 4px solid #f59e0b; }}
  ol, ul {{ padding-left: 22px; }}
  li {{ margin: 6px 0; }}
  footer {{ margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--kenar);
            text-align: right; color: var(--soluk); font-size: .9rem; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .container {{ box-shadow: none; padding: 0; max-width: none; }}
    h2 {{ break-after: avoid; }}
    figure {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
{GOVDE}
</body>
</html>
"""


def main():
    with open(CIKTI, "w", encoding="utf-8") as f:
        f.write(SAYFA)
    print(f"{CIKTI}  ({os.path.getsize(CIKTI) / 1_048_576:.2f} MB)")


if __name__ == "__main__":
    main()

# powered by Omer OZTURK
