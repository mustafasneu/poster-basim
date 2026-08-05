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
DEPO = "https://github.com/mustafasneu/poster-basim"


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
  <h1>📐 Poster Basım — Resimli Kullanım Kılavuzu</h1>
  <p class="ozet">Bir görseli oranını bozmadan A4 sayfalara böler, baskıya hazır tek bir PDF
  üretir. Sayfaları kesip yapıştırdığınızda tek büyük poster elde edersiniz.
  Bu kılavuzdaki bütün ekran görüntüleri programın kendisi çalıştırılarak alınmıştır.</p>
</header>

<div class="kutu kutu-ok">
  <strong>Bu bölümü sırayla takip ederseniz program 5 dakikada çalışır.</strong>
  Bilgisayar bilgisi gerekmez, komut yazmanız gerekmez — sadece indirip çift tıklayacaksınız.
  Program <b>Windows, macOS ve Linux</b>'ta aynı şekilde çalışır.
</div>

<h2 id="indirme">1. Programı indirme ve açma</h2>

<h3>1.1. Önce Python'u kontrol edin</h3>
<p>Program çalışabilmek için bilgisayarda <b>Python</b> adlı ücretsiz bir alt yazılıma
ihtiyaç duyar. Bunu bir kez kurarsınız, sonra unutursunuz.</p>
<table>
  <tr><th>Bilgisayarınız</th><th>Ne yapmanız gerekiyor</th></tr>
  <tr><td><b>Windows</b></td>
      <td>Genelde kurulu <u>değildir</u>. <a href="https://www.python.org/downloads/">
      python.org/downloads</a> adresine gidin, sarı <b>“Download Python”</b> düğmesine
      basın. İnen dosyaya çift tıklayın. Açılan pencerede
      <b>“Add python.exe to PATH”</b> yazan kutucuğu <b>işaretleyin</b>, sonra
      <b>“Install Now”</b>a basın. Bitince <b>Close</b> deyin. (~2 dakika)</td></tr>
  <tr><td><b>macOS</b></td>
      <td>Kuruludur, şimdilik hiçbir şey yapmayın. Programı ilk açtığınızda Apple
      <b>“command line developer tools”</b> kurmak isterse — bu Apple'ın kendi
      penceresidir — <b>Install</b> deyip bitmesini bekleyin (~2 dakika), sonra
      programı yeniden açın.</td></tr>
  <tr><td><b>Linux</b></td>
      <td>Kuruludur. Hiçbir şey yapmayın, 1.2'ye geçin.</td></tr>
</table>

<h3>1.2. Programı indirin</h3>
<p>Programın adresi:
<a href="https://github.com/mustafasneu/poster-basim">github.com/mustafasneu/poster-basim</a></p>
<p>Bu sayfada yeşil <b>“Code”</b> düğmesine, açılan listede de <b>“Download ZIP”</b>
satırına basın. Uğraşmak istemezseniz doğrudan indirme bağlantısı:</p>
<p><a href="https://github.com/mustafasneu/poster-basim/archive/refs/heads/main.zip">
https://github.com/mustafasneu/poster-basim/archive/refs/heads/main.zip</a></p>
<p><code>poster-basim-main.zip</code> adlı bir dosya iner; genelde <b>İndirilenler</b>
(Downloads) klasörüne düşer.</p>

<h3>1.3. İnen dosyayı klasöre çıkarın</h3>
<p>İnen dosya sıkıştırılmıştır; önce açılması gerekir.</p>
<table>
  <tr><th>Bilgisayarınız</th><th>Nasıl açılır</th></tr>
  <tr><td><b>Windows</b></td>
      <td>Dosyaya <b>sağ tıklayın</b> → <b>“Tümünü ayıkla”</b> → <b>“Ayıkla”</b>.</td></tr>
  <tr><td><b>macOS</b></td>
      <td>Dosyaya <b>çift tıklayın</b>; kendisi açar.</td></tr>
  <tr><td><b>Linux</b></td>
      <td>Dosyaya <b>sağ tıklayın</b> → <b>“Buraya çıkart”</b>.</td></tr>
</table>
<p>Sonuçta <code>poster-basim-main</code> adında bir klasör oluşur. Bu klasörü
<b>Masaüstü</b> ya da <b>Belgeler</b> gibi kalıcı bir yere taşıyın — program hep oradan
çalışacak.</p>

<div class="kutu kutu-uyari">
  <b>Bu adımı atlamayın.</b> Windows, sıkıştırılmış dosyanın içini normal bir klasör gibi
  gösterir; oradaki dosyalara çift tıklarsanız program <u>çalışmaz</u> ya da açılıp hemen
  kapanır. Önce <b>“Tümünü ayıkla”</b> deyip gerçek klasörü oluşturduğunuzdan emin olun —
  gerçek klasörün yol satırında artık <code>.zip</code> yazmaz.
</div>

<h3>1.4. Programı açın</h3>
<p>Klasörün içine girin ve <b>kendi bilgisayarınıza ait olan</b> dosyaya çift tıklayın:</p>
<table>
  <tr><th>Bilgisayarınız</th><th>Çift tıklanacak dosya</th><th>Not</th></tr>
  <tr><td><b>Windows</b></td><td><code>Poster Basim.bat</code></td>
      <td>Windows “bilinmeyen yayımcı” uyarısı verirse
      <b>Ek bilgi</b> → <b>Yine de çalıştır</b>.</td></tr>
  <tr><td><b>macOS</b></td><td><code>Poster Basim.command</code></td>
      <td>İlk açışta <b>sağ tıklayıp “Aç”</b> deyin, çıkan uyarıda yine <b>“Aç”</b>a
      basın; bir kez yeterli. Arkada siyah bir <b>Terminal</b> penceresi açılır, bu
      normaldir — kapatmayın, program penceresi onun üzerinde belirir.</td></tr>
  <tr><td><b>Linux</b></td><td><code>calistir.sh</code></td>
      <td>Çıkan soruda <b>“Çalıştır”</b> deyin. Çift tık dosyayı metin düzenleyicide
      açıyorsa, klasörde sağ tık → <b>“Terminalde aç”</b> deyip
      <code>./calistir.sh</code> yazın.</td></tr>
</table>

<div class="kutu kutu-bilgi">
  <b>İlk açılış yaklaşık yarım dakika sürer ve internet gerektirir.</b> Program bu sırada
  ihtiyacı olan iki parçayı kendi klasörüne indirir; küçük bir pencerede
  “gerekli bileşenler kuruluyor” yazar. Bu bir kez olur, sonraki açılışlar anındadır.
</div>

<h3>1.5. Masaüstüne kısayol koyun (tavsiye edilir)</h3>
<p>Her seferinde klasörü açmamak için masaüstüne simge koyabilirsiniz. Aynı klasörde,
yine <b>kendi bilgisayarınıza ait</b> dosyaya bir kez çift tıklayın:</p>
<table>
  <tr><th>Bilgisayarınız</th><th>Çift tıklanacak dosya</th></tr>
  <tr><td><b>Windows</b></td><td><code>Kisayol Olustur.bat</code></td></tr>
  <tr><td><b>macOS</b></td><td><code>Kisayol Olustur.command</code></td></tr>
  <tr><td><b>Linux</b></td><td><code>kisayol-olustur.sh</code></td></tr>
</table>
<p>Masaüstünde <b>“Poster Basım”</b> simgesi belirir. Bundan sonra programı hep o
simgeye çift tıklayarak açın. Kısayolu istemezseniz masaüstünden silmeniz yeterlidir.</p>

<div class="kutu kutu-uyari">
  <b>Program klasörünü silmeyin ve yerini değiştirmeyin.</b> Masaüstündeki simge o klasörü
  işaret eder; klasör taşınırsa simge çalışmaz. Taşımanız gerekirse, taşıdıktan sonra
  yukarıdaki kısayol dosyasına bir kez daha çift tıklayın.
</div>

<h3>1.6. Açılmazsa</h3>
<table>
  <tr><th>Durum</th><th>Çözüm</th></tr>
  <tr><td><b>Windows:</b> siyah pencere açılıp “Python bulunamadi” yazıyor</td>
      <td>1.1 adımı atlanmış. Python'u kurun ve kurulumda
      <b>“Add python.exe to PATH”</b> kutucuğunu işaretlemeyi unutmayın.</td></tr>
  <tr><td><b>macOS:</b> “geliştirici doğrulanamadı” uyarısı</td>
      <td>Dosyaya <b>sağ tıklayıp “Aç”</b> deyin ve uyarıda yine <b>“Aç”</b>a basın.
      Program imzalı bir mağaza uygulaması olmadığı için macOS bir kez sorar.</td></tr>
  <tr><td><b>macOS:</b> sağ tık → Aç yaptım, yine de açılmıyor</td>
      <td>Yeni macOS sürümlerinde onay ayrı bir yerden verilir:
      <b>Sistem Ayarları</b> → <b>Gizlilik ve Güvenlik</b> → sayfayı aşağı kaydırın →
      <code>Poster Basim.command</code> için <b>“Yine de Aç”</b> düğmesine basın.</td></tr>
  <tr><td><b>macOS:</b> Apple “command line developer tools” kurulmasını istiyor</td>
      <td>Apple'ın kendi penceresidir; <b>Install</b> deyin, bitince programı yeniden
      açın. Kurmak istemezseniz <a href="https://www.python.org/downloads/">python.org</a>
      üzerinden Python kurmak da aynı işi görür.</td></tr>
  <tr><td><b>macOS:</b> “tkinter bulunamadı” uyarısı</td>
      <td>Terminali açıp bir kez şunu çalıştırın:
      <code>brew install python-tk</code> (Homebrew yoksa python.org kurulumu bu parçayı
      zaten içerir).</td></tr>
  <tr><td><b>Linux:</b> “tkinter bulunamadı” uyarısı</td>
      <td>Terminali açıp bir kez şunu çalıştırın:
      <code>sudo apt install -y python3-tk</code></td></tr>
  <tr><td><b>Windows:</b> pencere bir anda açılıp kapanıyor</td>
      <td>Büyük ihtimalle dosyalar hâlâ sıkıştırılmış klasörün içinde. 1.3 adımına dönüp
      <b>“Tümünü ayıkla”</b> yapın, sonra çıkan gerçek klasördeki dosyaya çift tıklayın.</td></tr>
  <tr><td><b>Linux:</b> çift tıklayınca dosya metin olarak açılıyor</td>
      <td>Klasörde boş bir yere sağ tıklayıp <b>“Terminalde aç”</b> deyin, sonra
      <code>./calistir.sh</code> yazıp Enter'a basın.</td></tr>
  <tr><td>“Bileşenler kurulamadı” yazıyor</td>
      <td>İlk açılışta internet gerekir. Bağlantıyı kontrol edip programı yeniden açın.
      Kurum ağındaysanız güvenlik duvarı engelliyor olabilir; başka bir ağda deneyin.</td></tr>
  <tr><td>Masaüstündeki simge artık açmıyor</td>
      <td>Program klasörü taşınmış ya da silinmiştir. Klasörü bulup 1.5 adımındaki kısayol
      dosyasına bir kez daha çift tıklayın.</td></tr>
  <tr><td>Hiçbir şey olmuyor gibi</td>
      <td>İlk açılış yarım dakika sürer ve bu sırada ekranda bir şey görünmeyebilir.
      Yarım dakika bekleyin; sonraki açılışlar anında olur.</td></tr>
</table>

<div class="kutu kutu-ok">
  <b>Yönetici (admin) yetkisi gerekmez.</b> Program her şeyi kendi klasörüne yazar;
  kurum bilgisayarlarında da tek başınıza kurabilirsiniz. Tek istisna, Windows'ta
  Python'un ilk kurulumudur — orada işletim sistemi izin isteyebilir.
</div>

<h2 id="genel">2. Program açıldığında</h2>
<p>Pencere iki bölümden oluşur: solda <b>ayar paneli</b>, sağda <b>önizleme alanı</b>.
Resim seçilene kadar alttaki iki buton pasiftir (soluk görünür) — bu normaldir.</p>
<p>Sol paneldeki <b>Oranı Koru ve Hazır PDF Üret</b> ile <b>Çıktı Klasörünü Aç</b> düğmeleri
her zaman panelin en altında durur. Ekranınız kısaysa ayarlar bölümü kendi içinde kayar
(sağında ince bir kaydırma çubuğu çıkar, fare tekerleğiyle de gezebilirsiniz); düğmeler
yine de yerinde kalır.</p>
{sekil("01_baslangic.png", "Açılış ekranı", "sol panel ayarlar, sağ panel önizleme")}

<h2 id="resim">3. Adım 1 — Resim seçme</h2>
<p><code>Bilgisayardan Resim Seç</code> düğmesine basın. Açılan pencerede üstteki
<b>Klasör</b> kutusundan resmin bulunduğu klasöre gidin, sonra dosyaya çift tıklayın
(ya da bir kez tıklayıp sağdaki <b>Aç</b> düğmesine basın). Vazgeçmek için
<b>İptal</b>.</p>
<p>Desteklenen biçimler: <code>.jpg .jpeg .png .bmp .webp .tif .tiff</code>.
Telefonla çekilmiş fotoğrafların yön bilgisi otomatik düzeltilir.</p>

<h3>İnternetteki bir resmi doğrudan kullanma</h3>
<p>Resim bilgisayarınızda değil de bir web sayfasındaysa indirmenize gerek yok:
<code>İnternetten Link ile Al</code> düğmesine basın, açılan kutuya resmin adresini
yapıştırıp <b>Resmi Al</b> deyin. Program resmi kendisi indirir ve doğrudan yükler.</p>
<p><b>Adresi nasıl alırım?</b> Tarayıcıda resmin üzerine <b>sağ tıklayın</b> →
<b>“Resim adresini kopyala”</b>. Panonuzda bir adres varsa kutuya zaten hazır gelir.</p>
{sekil("02b_link_penceresi.png", "Link ile alma penceresi", "adres yapıştırılıp Resmi Al denir", 760)}
<div class="kutu kutu-bilgi">
  <b>Dikkat edilecekler:</b> Adres <u>resmin kendisine</u> ait olmalı (sonu genelde
  <code>.jpg</code> / <code>.png</code> ile biter); sayfanın adresi işe yaramaz, program
  “bu adres bir resim değil” uyarısı verir. En fazla 60 MB indirilir. Şifre isteyen ya da
  yalnızca üyelere açık sayfalardaki resimler indirilemez — o durumda resmi tarayıcıdan
  <b>sağ tık → Resmi farklı kaydet</b> ile bilgisayarınıza kaydedip
  <code>Bilgisayardan Resim Seç</code> ile açın.
</div>
{sekil("02_dosya_secme.png", "Dosya seçme penceresi", "Klasör · Dosya adı · Aç · İptal")}

<div class="kutu kutu-bilgi">
  <b>Hangi çözünürlük yeterli?</b> Kaba ölçü: her A4 sayfa için yaklaşık
  <b>1000 piksel genişlik</b> hedefleyin. 3×2 poster için ~3000 × 2000 piksel iyi sonuç verir.
  Daha düşük çözünürlükte baskıda pikselleşme görünür; keskinlik sürgüsü bunu bir miktar
  toparlar ama yok etmez.
</div>

<h2 id="onizleme">4. Adım 2 — Önizleme</h2>
<p>Resim yüklendiğinde dosya adı sol panelde, kaynak çözünürlük ise sağ altta yazar.
Önizleme hız için küçültülmüş kopyadır; <b>PDF her zaman tam çözünürlükten üretilir</b>.</p>
{sekil("03_resim_yuklendi.png", "Resim yüklendikten sonra", "sağ altta kaynak çözünürlük bilgisi")}

<h2 id="bolme">5. Adım 3 — Poster ölçüsünü belirleme</h2>
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

<h2 id="iyilestirme">6. Adım 4 — Görüntü iyileştirme</h2>
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

<h2 id="uretim">7. Adım 5 — PDF üretme</h2>
<p><code>Oranı Koru ve Hazır PDF Üret</code> düğmesine basın. Alt satırda
“Parça üretiliyor: 3 / 6” gibi ilerleme görünür; büyük görsellerde bu birkaç saniye sürer.
Bitince özet penceresi açılır.</p>
{sekil("06_tamamlandi.png", "Üretim tamamlandı penceresi", "çıktı klasörünün tam yolunu gösterir")}
<p>Pencereyi <b>Tamam</b> ile kapattıktan sonra <code>Çıktı Klasörünü Aç</code> düğmesi
etkinleşir; dosya yöneticisini doğrudan o klasörde açar.</p>
{sekil("07_bitis_durumu.png", "Üretim sonrası ana ekran", "alt satırda üretilen PDF adı yazar")}

<h2 id="cikti">8. Çıktı klasöründe ne var?</h2>
<p>Her üretim, tarih-saat damgalı ayrı bir klasöre yazılır; eski çıktıların üzerine
<b>asla</b> yazılmaz.</p>
<pre><code>Masaüstü/
└── Poster_Parcalari/
    └── Poster_OranKorumali_20260805_100535/
        ├── Oran_Korumali_Baski_20260805_100535.pdf   ← yazdırılacak dosya
        ├── parca_satir1_sutun1.jpg                   ← tek tek parçalar
        ├── parca_satir1_sutun2.jpg
        └── ...</code></pre>
<p>Normalde sadece PDF'i yazdırmanız yeterlidir. JPEG parçalar, tek bir sayfayı yeniden
bastırmak veya başka bir programda kullanmak isterseniz durur.</p>
{sekil("09_a4_sayfa_ornegi.png", "PDF'in ilk sayfası", "her sayfa tek bir parçayı taşır", 900)}

<h2 id="yazdirma">9. Yazdırma ayarları (en kritik adım)</h2>
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

<h2 id="birlestirme">10. Kesme ve birleştirme</h2>
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

<h2 id="sorun">11. Sık karşılaşılan durumlar</h2>
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
  <tr><td>“Oranı Koru ve Hazır PDF Üret” düğmesini göremiyorum</td>
      <td>Pencereyi biraz büyütün ya da tam ekran yapın. Düğmeler panelin en altındadır;
          ayarlar bölümü sığmazsa kendi içinde kayar.</td></tr>
  <tr><td><b>macOS:</b> PDF üretilemiyor / izin hatası</td>
      <td>macOS, programların Masaüstü klasörüne erişimini izne bağlar. Çıkan izin
          penceresinde <b>İzin Ver</b> deyin. Yanlışlıkla reddettiyseniz
          <b>Sistem Ayarları → Gizlilik ve Güvenlik → Dosyalar ve Klasörler</b> yolundan
          izni açın. İzin verilmezse program çıktıyı <b>Belgeler</b> klasörüne yazar;
          tamamlandı penceresinde tam yol görünür.</td></tr>
  <tr><td>Büyük resimde program donmuş gibi</td>
      <td>Donmadı; alt satırdaki “Parça üretiliyor: n / m” ilerlemesini izleyin.</td></tr>
  <tr><td><b>Windows:</b> çift tıklayınca pencere açılmıyor</td>
      <td>Python kurulu değil. <code>python.org</code> üzerinden kurun; kurulumda
          “Add python.exe to PATH” ve “tcl/tk and IDLE” işaretli kalsın.</td></tr>
  <tr><td><b>macOS:</b> “geliştirici doğrulanamadı” uyarısı</td>
      <td>Dosyaya sağ tıklayıp <b>Aç</b> deyin ve bir kez onaylayın; sonraki açılışlarda
          sormaz. Kod imzalı bir uygulama değil, düz bir betiktir.</td></tr>
  <tr><td><b>macOS:</b> <code>.command</code> dosyası açılmıyor</td>
      <td>Terminalde bir kez: <code>chmod +x "Poster Basim.command"</code></td></tr>
  <tr><td><b>Linux:</b> “tkinter bulunamadı” uyarısı</td>
      <td>Bir kez: <code>sudo apt install -y python3-tk</code> (Fedora:
          <code>sudo dnf install -y python3-tkinter</code>).</td></tr>
  <tr><td>İlk açılış uzun sürüyor</td>
      <td>Yalnızca ilk seferde bileşenler indirilir (~30 sn). Sonraki açılışlar anındadır.</td></tr>
</table>

<h2 id="teknik">12. Teknik notlar</h2>
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
  <li><b>Program dosyaları:</b> <code>poster_bolme.py</code> (programın kendisi);
      başlatıcılar <code>Poster Basim.bat</code> (Windows),
      <code>Poster Basim.command</code> (macOS), <code>calistir.sh</code> (Linux);
      kısayol oluşturucular <code>Kisayol Olustur.bat</code>,
      <code>Kisayol Olustur.command</code>, <code>kisayol-olustur.sh</code> ve bunların
      çağırdığı <code>kurulum.py</code>; <code>.venv/</code> (bağımlılıklar, ilk açılışta
      oluşur).</li>
  <li><b>Kaynak kodu:</b> <code>github.com/mustafasneu/poster-basim</code></li>
</ul>

<h2 id="baglantilar">13. Bağlantılar</h2>
<p>İhtiyaç duyabileceğiniz bütün adresler:</p>
<table>
  <tr><th>Ne için</th><th>Adres</th></tr>
  <tr><td><b>Programın sayfası</b> (her şey burada)</td>
      <td><a href="{DEPO}">{DEPO}</a></td></tr>
  <tr><td><b>Programı indir</b> (ZIP, doğrudan)</td>
      <td><a href="{DEPO}/archive/refs/heads/main.zip">{DEPO}/archive/refs/heads/main.zip</a></td></tr>
  <tr><td><b>Bu kılavuz</b> (PDF)</td>
      <td><a href="{DEPO}/raw/main/KULLANIM_KILAVUZU.pdf">{DEPO}/raw/main/KULLANIM_KILAVUZU.pdf</a></td></tr>
  <tr><td><b>Bu kılavuz</b> (web sayfası)</td>
      <td><a href="{DEPO}/raw/main/KULLANIM_KILAVUZU.html">{DEPO}/raw/main/KULLANIM_KILAVUZU.html</a></td></tr>
  <tr><td><b>Python indirme</b> (yalnızca Windows'ta gerekir)</td>
      <td><a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a></td></tr>
  <tr><td><b>Sorun bildirme / soru sorma</b></td>
      <td><a href="{DEPO}/issues">{DEPO}/issues</a></td></tr>
</table>

<h2 id="kurulum">14. Kaldırma, taşıma ve internetsiz kurulum</h2>
<div class="kutu kutu-ok">
  <strong>Programı kaldırmak:</strong> <code>poster-basim-main</code> klasörünü ve
  masaüstündeki “Poster Basım” simgesini silin. Bu kadar — program bilgisayarınızın
  başka hiçbir yerine dosya yazmaz, kayıt defterine dokunmaz. Ürettiğiniz posterler
  masaüstündeki <code>Poster_Parcalari</code> klasöründe kalır; onları da
  istemiyorsanız ayrıca silin.
</div>
<div class="kutu kutu-bilgi">
  <b>Başka bir bilgisayara taşımak:</b> Klasörü olduğu gibi kopyalamanız yeterli
  (USB bellek de olur). Yeni bilgisayarda 1.4 ve 1.5 adımlarını tekrarlayın. İşletim
  sistemi farklı olsa bile aynı klasör çalışır.
</div>
<div class="kutu kutu-bilgi">
  <b>Telefon ve tabletler:</b> Program masaüstü bilgisayarlar içindir; Android ve
  iPhone'da çalışmaz. Telefonunuzdaki bir fotoğrafı bölmek isterseniz fotoğrafı önce
  bilgisayara aktarın (kablo, e-posta ya da bulut ile).
</div>
<div class="kutu kutu-bilgi">
  <b>İnternetsiz bilgisayarda kurulum:</b> İlk açılışta iki bileşenin inmesi için internet
  gerekir. Hiç internet olmayacaksa, internetli bir bilgisayarda
  <code>pip download pillow reportlab -d paketler</code> komutuyla hazırlanan
  <code>paketler</code> klasörünü de taşıyın ve hedef makinede
  <code>pip install --no-index --find-links paketler pillow reportlab</code> çalıştırın.
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
<title>Poster Basım — Resimli Kullanım Kılavuzu</title>
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
  a {{ color: var(--ana); word-break: break-all; }}
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
