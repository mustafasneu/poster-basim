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

IMZA = "powered by Ömer ÖZTÜRK & Mustafa ŞEKER"
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


def sekil(ad: str, baslik: str, aciklama: str = "", genislik: int = 1100, dar: bool = False) -> str:
    # Panel kırpıkları dar olduğu için sayfa genişliğine gerilirse bulanıklaşır;
    # "dar" bunları kendi gerçek ölçüsünde bırakır.
    alt = f"<figcaption>{baslik}{(' — ' + aciklama) if aciklama else ''}</figcaption>"
    sinif = ' class="dar"' if dar else ""
    return (
        f'<figure{sinif}><img src="{gomulu(ad, genislik)}" alt="{baslik}" loading="lazy">{alt}</figure>'
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
  ihtiyacı olan bileşenleri (görüntü işleme, PDF okuma-yazma, iPhone ve ham fotoğraf
  desteği) kendi klasörüne indirir; küçük bir pencerede “gerekli bileşenler kuruluyor”
  yazar. Bu yalnızca bir kez olur, sonraki açılışlar anında gerçekleşir.
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

<h3>En kısa yol: sürükle-bırak</h3>
<p>Dosyayı dosya yöneticisinden (Windows'ta Dosya Gezgini, macOS'ta Finder) tutup
<b>programın penceresine bırakın</b>. Pencerenin tamamı hedeftir; belirli bir yere
nişan almanız gerekmez. Düğmeye basmadan dosya açılır.</p>
<ul>
  <li><b>Poster modunda</b> tek görsel açılır. Birden fazla dosya bıraktıysanız program
      bunları tek bir A4 sayfaya dizmek isteyip istemediğinizi sorar; hayır derseniz
      yalnızca ilk dosya poster olarak açılır.</li>
  <li><b>Dizme modunda</b> her bırakış listeye <i>ekler</i>; önceki seçiminizi silmez.
      Fotoğrafları birkaç seferde, farklı klasörlerden toplayabilirsiniz.</li>
  <li>Aynı dosyayı iki kez bırakırsanız listede çoğalmaz.</li>
</ul>
<p>Sürükle-bırak, düğmeyle seçmenin yerine geçmez; hangisi kolayınıza gelirse onu
kullanın. Aşağıdaki dosya türlerinin hepsi iki yolla da açılır.</p>

<h3>Düğmeyle seçme</h3>
<p><code>Bilgisayardan Resim Seç</code> düğmesine basın. Açılan pencerede üstteki
<b>Klasör</b> kutusundan dosyanın bulunduğu klasöre gidin, sonra dosyaya çift tıklayın
(ya da bir kez tıklayıp sağdaki <b>Aç</b> düğmesine basın). Vazgeçmek için
<b>İptal</b>.</p>
<p>Telefonla çekilmiş fotoğrafların yön bilgisi otomatik düzeltilir. Desteklenen dosyalar:</p>
<table>
  <tr><th>Tür</th><th>Uzantılar</th><th>Not</th></tr>
  <tr><td>Resim</td><td><code>.jpg .jpeg .png .bmp .webp .tif .tiff .gif</code></td>
      <td>En yaygın kullanım</td></tr>
  <tr><td>Photoshop</td><td><code>.psd</code></td>
      <td>Kaydedilmiş birleşik görüntü kullanılır (katmanlara girilmez)</td></tr>
  <tr><td>PDF / Illustrator</td><td><code>.pdf .ai</code></td>
      <td>300 DPI taranır; en kaliteli kaynak</td></tr>
  <tr><td>iPhone fotoğrafı</td><td><code>.heic .heif</code></td>
      <td>Doğrudan açılır, dönüştürmeye gerek yok</td></tr>
  <tr><td>Ham fotoğraf (RAW)</td>
      <td><code>.cr2 .cr3 .nef .arw .dng .orf .rw2 .raf .srw .pef</code></td>
      <td>Fotoğraf makinesinin beyaz ayarıyla işlenir, birkaç saniye sürer</td></tr>
</table>
<div class="kutu kutu-bilgi">
  <b>SVG, EPS ve CorelDRAW (.cdr) dosyaları:</b> Bunlar için tasarım programınızdan
  <b>PDF olarak dışa aktarın</b> (Corel'de <i>Dosya → Dışa Aktar → PDF</i>). Tek adımdır,
  kalite kaybı olmaz ve PDF zaten en iyi sonucu veren kaynaktır.
</div>

<h3>PDF afiş / tasarım kullanma</h3>
<p>Afiş ve poster tasarımları çoğu zaman JPEG değil <b>PDF</b> olarak gelir. Programa
PDF'i doğrudan verebilirsiniz: <code>Bilgisayardan Resim Seç</code> ile <code>.pdf</code>
dosyasını seçin, gerisi resimle aynıdır.</p>
<p>PDF <b>vektörel</b> olduğu için program sayfayı <b>300 DPI</b> baskı çözünürlüğünde
tarar; büyütmede bozulma olmaz. Bu yüzden PDF kaynak, aynı tasarımın ekran görüntüsünü
almaktan <u>her zaman daha kalitelidir</u>.</p>
<p>PDF birden çok sayfa içeriyorsa hangi sayfanın postere dönüşeceği sorulur. Sayfayı
körlemesine seçmezsiniz: pencerede <b>o sayfanın küçük görüntüsü</b> durur.
<b>◀ ▶</b> düğmeleriyle (ya da klavyedeki sol/sağ ok tuşlarıyla) sayfalar arasında gezip
istediğinizi görünce <b>Bu Sayfayı Kullan</b> deyin.</p>
{sekil("02c_pdf_sayfa_secme.png", "PDF sayfa seçme penceresi", "seçilen sayfa önizlemede görünür", 760)}
<div class="kutu kutu-bilgi">
  <b>Tarama birkaç saniye sürebilir</b> — büyük afiş PDF'lerinde alt satırda
  “PDF taranıyor (300 DPI)…” yazar. Şifreli PDF'ler açılamaz; şifreyi kaldırıp
  yeniden deneyin.
</div>

<h3>İnternetteki bir görseli doğrudan kullanma</h3>
<p>Görsel bilgisayarınızda değil de bir web sayfasındaysa indirmenize gerek yok:
<code>İnternetten Link ile Al</code> düğmesine basın, açılan kutuya adresi yapıştırıp
<b>Resmi Al</b> deyin. Program kendisi indirir ve doğrudan yükler.
<b>Resim de PDF de</b> olabilir — PDF ise yine sayfası taranır ve gerekiyorsa hangi
sayfa olduğu sorulur.</p>
<p><b>Adresi nasıl alırım?</b> Tarayıcıda resmin üzerine <b>sağ tıklayın</b> →
<b>“Resim adresini kopyala”</b>. Panonuzda bir adres varsa kutuya zaten hazır gelir.</p>
{sekil("02b_link_penceresi.png", "Link ile alma penceresi", "adres yapıştırılıp Resmi Al denir", 760)}
<div class="kutu kutu-bilgi">
  <b>Dikkat edilecekler:</b> Adres <u>görselin kendisine</u> ait olmalı; sonu genelde
  <code>.jpg</code>, <code>.png</code> ya da <code>.pdf</code> ile biter. Sayfanın adresini
  yapıştırırsanız program “bu adres bir resim ya da PDF değil, web sayfası döndürüyor”
  uyarısını verir ve indirmez. En fazla 60 MB indirilebilir. Şifre isteyen ya da yalnızca
  üyelere açık sayfalardaki görseller indirilemez; o durumda görseli tarayıcıdan
  <b>sağ tık → Resmi farklı kaydet</b> ile bilgisayarınıza kaydedin ve
  <code>Bilgisayardan Dosya Seç</code> ile açın.
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
  <tr><td><b>Yazıcı Kenar Boşluğu</b></td>
      <td>Yazıcınızın kâğıdın kenarına <u>basamadığı</u> pay</td>
      <td><b>5 mm</b> (kenarlıksız basan yazıcıda 0)</td></tr>
  <tr><td><b>Kesim ve hizalama işaretleri</b></td>
      <td>Her sayfaya kesim çizgisi, köşe işareti, hizalama artıları ve parça etiketi</td>
      <td>Açık bırakın</td></tr>
  <tr><td><b>Montaj haritası</b></td>
      <td>PDF'in başına, parçaların nereye geleceğini gösteren bir sayfa ekler</td>
      <td>Açık bırakın</td></tr>
</table>

<div class="kutu kutu-uyari">
  <b>Yazıcı kenar boşluğu neden önemli?</b> Yazıcıların çoğu kâğıdın en kenarına basamaz;
  genellikle 3–5 mm'lik bir şerit boş kalır. Program bu payı hesaba katmazsa her sayfadan
  birkaç milimetre kaybolur ve parçalar yan yana geldiğinde <u>tutmaz</u>. Yazıcınızın
  değerini bilmiyorsanız <b>5 mm</b> iyi bir başlangıçtır; “kenarlıksız baskı”
  yapabiliyorsanız 0 girin. Bu ayar poster ölçüsünü de küçültür — üstteki ölçü yazısı
  buna göre güncellenir.
</div>

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

<h2 id="iyilestirme">6. Adım 4 — Baskı iyileştirme</h2>
<p>Bu bölüm, görseli <b>baskıya</b> hazırlar. Ekranda güzel duran bir görsel, kâğıtta
genellikle daha mat ve daha yumuşak çıkar; buradaki ayarlar bu farkı kapatır. Yaptığınız
her değişiklik sağdaki önizlemeye anında yansır.</p>

<h3>Önce: çözünürlük uyarısı</h3>
<p>Bölümün en üstünde, seçtiğiniz sayfa sayısına göre posterin <b>gerçek ölçüsü</b> ve
<b>baskı çözünürlüğü</b> yazar. Rengi size ne yapmanız gerektiğini söyler:</p>
<table>
  <tr><th>Renk</th><th>Anlamı</th><th>Ne yapmalı</th></tr>
  <tr><td><b>Yeşil</b> (200 DPI üstü)</td><td>Çözünürlük yeterli</td>
      <td>Devam edin</td></tr>
  <tr><td><b>Turuncu</b> (120–200 DPI)</td><td>Kabul edilebilir</td>
      <td>Birkaç adım uzaktan bakılan posterlerde sorun olmaz</td></tr>
  <tr><td><b>Kırmızı</b> (120 DPI altı)</td><td>Düşük — yakından pikselli görünür</td>
      <td>Sayfa sayısını azaltın ya da daha büyük bir görsel bulun</td></tr>
</table>
<div class="kutu kutu-uyari">
  <b>Bu uyarı kâğıt israfını önler.</b> 1920 × 1080 bir görseli 4 × 2 (yaklaşık 119 × 42 cm)
  bastırmak isterseniz baskı ~40 DPI olur; 8 sayfa kâğıt harcadıktan sonra sonucu
  beğenmezsiniz. Uyarı bunu <u>baskıdan önce</u> söyler.
</div>

<h3>Hazır ayarlar</h3>
<p>Tek tek ayar yapmak istemiyorsanız <b>Hazır Ayar</b> listesinden görselinize uyanı
seçin; program bütün değerleri sizin için doldurur.</p>
<table>
  <tr><th>Hazır ayar</th><th>Ne zaman</th></tr>
  <tr><td><b>Fotoğraf</b></td><td>Makine ya da telefonla çekilmiş normal fotoğraflar
      (varsayılan)</td></tr>
  <tr><td><b>Grafik / Afiş</b></td><td>Tasarlanmış afiş, logo, düz renkli grafik —
      renklere dokunulmaz, sadece kenarlar keskinleştirilir</td></tr>
  <tr><td><b>Tarama / Eski baskı</b></td><td>Taranmış belge ya da eski fotoğraf; gürültü
      azaltma devrede</td></tr>
  <tr><td><b>Telefon fotoğrafı</b></td><td>Loş ışıkta çekilmiş, hafif gürültülü kareler</td></tr>
  <tr><td><b>Dokunma (ham)</b></td><td>Hiçbir işlem yapılmasın; görsel olduğu gibi kalsın</td></tr>
</table>

<h3>Ayarlar tek tek</h3>
<table>
  <tr><th>Ayar</th><th>Ne yapar</th><th>Öneri</th></tr>
  <tr><td><b>Otomatik düzelt</b></td>
      <td>Soluk görüntünün kontrastını açar ve renk sapmasını (sarılık/mavilik) giderir.
          İki işi tek kutucukla yapar.</td>
      <td>Fotoğraflarda <b>açık</b>; tasarlanmış afişlerde <b>kapalı</b> (tasarımcının
          renklerini değiştirmesin)</td></tr>
  <tr><td><b>Düşük çözünürlükte akıllı büyüt</b></td>
      <td>Görsel seçtiğiniz boy için küçükse, baskı öncesi yumuşak geçişli büyütür ve
          ardından hafifçe keskinleştirir.</td>
      <td><b>Açık</b> bırakın</td></tr>
  <tr><td><b>Kâğıt türü</b></td>
      <td>Baskı yapacağınız kâğıda göre renk ve kontrastı önceden telafi eder. Mat ve
          fotokopi kâğıdı mürekkebi emer, renkleri söndürür; program bunu dengeler.</td>
      <td>Kâğıdınızı seçin; emin değilseniz <b>Belirtme</b></td></tr>
  <tr><td><b>Gürültü azaltma</b></td>
      <td>Loş ışıkta çekilmiş fotoğraflardaki benek benek görüntüyü temizler.</td>
      <td>Temiz fotoğraflarda <b>Kapalı</b>; benekliyse <b>Hafif</b> ya da <b>Orta</b></td></tr>
</table>

<h4>Keskinleştirme (unsharp mask)</h4>
<p>Baskıda kullanılan gerçek keskinleştirme yöntemidir; üç ayarı vardır:</p>
<table>
  <tr><th>Sürgü</th><th>Ne yapar</th><th>Öneri</th></tr>
  <tr><td><b>Yarıçap</b></td><td>Kenarların ne kadar kalın bir bant boyunca
      belirginleşeceği</td><td>1.0 – 1.5 (büyük posterlerde 2'ye kadar)</td></tr>
  <tr><td><b>Miktar</b></td><td>Etkinin gücü</td><td>%80 – %150</td></tr>
  <tr><td><b>Eşik</b></td><td>Bu değerin altındaki küçük farklara dokunulmaz; düz
      alanlardaki gürültünün keskinleşmesini önler</td><td>2 – 5 (fotoğraf), 0 (grafik)</td></tr>
</table>
<div class="kutu kutu-bilgi">
  <b>Fazla keskinleştirmeyin.</b> Miktarı %200'ün üstüne çıkarırsanız kenarlarda beyaz
  hâleler (halkalanma) belirir ve baskıda çirkin durur. Önizlemede kenarlara yakından bakın.
</div>

<h4>AI ile büyütme (isteğe bağlı eklenti)</h4>
<p><b>Bu nedir?</b> Yapay zekâ ile büyütme, küçük bir görseli büyütürken kaybolan detayı
<b>tahmin ederek yeniden üretir</b>. Klasik büyütme yalnızca pikselleri yumuşatır; AI,
kenarları ve dokuyu yeniden çizer. Küçük görsellerde gözle görülür fark yaratır.</p>

<p><b>Neden ayrı eklenti?</b> Bu iş için bir hesaplama motoru (~15 MB) ve model dosyası
(~21 MB) gerekir. Bunlar programın içinde gelseydi, bu özelliği hiç kullanmayacak herkes
de indirmek zorunda kalırdı. Bu yüzden isteğe bağlı bırakıldı:
<b>eklenti kurulmadan AI büyütme yapılamaz</b>. Panelde bu durum yazılı olarak görünür.</p>

<p><b>Nasıl kurulur?</b> <code>AI ile Büyüt (eklenti gerekir)</code> düğmesine basın.
Program ne indireceğini, boyutunu, kaynağını ve ne işe yaradığını anlatan bir pencere
açar; kabul ederseniz bir kez indirir ve program klasöründeki <code>eklentiler</code>
klasörüne koyar. Bir daha indirmez, internet de yalnızca o ilk seferde gerekir.</p>

<p><b>Ne kadar sürer?</b> Program, işleme başlamadan önce <u>sizin bilgisayarınızda</u>
küçük bir ölçüm yapar ve “bu görsel yaklaşık şu kadar sürecek” diye sorar. Karar sizindir.
İşlem sırasında kaç parçanın bittiği ve kalan sürenin tahmini görünür, istediğiniz an
<b>Durdur</b> diyebilirsiniz. Süre donanıma göre çok değişir: aynı iş güçlü bir
bilgisayarda yarım dakika, eski bir dizüstünde on dakika sürebilir.</p>

<div class="kutu kutu-uyari">
  <b>AI var olmayan detayı uydurur.</b> Küçük yazılar, yüz hatları ve logolar
  olduğundan farklı çıkabilir. Belge, metin ve kurumsal logo içeren işlerde klasik
  büyütmede kalmak daha güvenlidir. Sonucu önizlemede kontrol edin.
</div>

<div class="kutu kutu-bilgi">
  <b>Kaynak:</b> Model, Apache-2.0 lisanslı açık kaynak Swin2SR modelinin ONNX sürümüdür
  (huggingface.co/Xenova/swin2SR-classical-sr-x2-64). İnternete yalnızca indirme sırasında
  bağlanılır; görselleriniz hiçbir yere gönderilmez, tüm işlem kendi bilgisayarınızda yapılır.
</div>

<h4>Renk ve ton</h4>
<table>
  <tr><th>Sürgü</th><th>Aralık</th><th>Baskı için öneri</th></tr>
  <tr><td>Kontrast</td><td>0.5 – 2.5</td><td>1.1 – 1.3</td></tr>
  <tr><td>Renk Canlılığı</td><td>0.5 – 2.5</td><td>1.2 – 1.4 (mat kâğıt söndürür)</td></tr>
  <tr><td>Parlaklık</td><td>0.5 – 2.0</td><td>1.0 – 1.15</td></tr>
</table>
<p><code>Ayarları Sıfırla</code> her şeyi “Fotoğraf” hazır ayarına döndürür.</p>
{sekil("05_iyilestirme.png", "İyileştirme uygulanmış hali", "değişiklikler önizlemeye anında yansır")}

<div class="kutu kutu-bilgi">
  <b>Önizleme dürüsttür.</b> Önizleme küçültülmüş bir kopya üzerinde çalışır; program
  keskinleştirme yarıçapını bu küçültme oranına göre ayarlar. Böylece ekranda gördüğünüz
  keskinlik, kâğıtta göreceğinizle aynı olur — birçok programda bu yapılmadığı için
  önizleme olduğundan keskin görünür.
</div>

<h2 id="denetim">7. Baskıdan önce: rapor ve 1:1 önizleme</h2>
<p>Kâğıt harcamadan önce sonucu görmenizi sağlayan iki araç, üretim düğmelerinin hemen
üstündedir.</p>

<h3>Baskı Raporu</h3>
<p>Tek ekranda her şeyi özetler: kaynak görselin çözünürlüğü, matris, poster ve tek sayfa
ölçüsü, baskı DPI'ı ve değerlendirmesi, çakışma payı, <b>kesilecek toplam uzunluk</b>,
seçili iyileştirme ayarları ve varsa uyarılar. Aynı rapor, üretim sonrasında çıktı
klasörüne <code>baski_raporu.txt</code> olarak da yazılır — “bunu hangi ayarlarla
basmıştım?” sorusu bir daha sorulmaz.</p>
{sekil("11_baski_raporu.png", "Baskı raporu", "üretimden önce tek ekranda özet ve uyarılar", 900)}

<h3>1:1 Gerçek Boyut Önizleme</h3>
<p>Posterin küçük bir bölgesini <b>kâğıttaki gerçek ölçüsünde</b> gösterir. Pikselleşme
olup olmayacağını 8 sayfa bastıktan sonra değil, önceden görürsünüz. Pencerede sürükleyerek
görselin başka bölgelerine gezinebilirsiniz.</p>
<p>Üstteki <b>santimetre cetveli</b> kalibrasyon içindir: elinizdeki gerçek cetveli ekrana
dayayın; ölçüler tutmuyorsa alttaki <b>Ekran DPI</b> değerini tutana kadar değiştirin.
Böylece “gerçek boyut” gerçekten gerçek olur.</p>
{sekil("12_birebir_onizleme.png", "1:1 önizleme", "üstte kalibrasyon cetveli, altta baskı DPI bilgisi", 900)}

<h2 id="uretim">8. Adım 5 — PDF üretme</h2>

<h3>Üretmeden önce: çıktı formatı</h3>
<p>Sol paneldeki <b>ÇIKTI FORMATI</b> bölümü, dosyanın hangi biçimlerde kaydedileceğini
belirler. <b>Baskıya hazır PDF her zaman üretilir</b>; bu üç kutu PDF'i kapatmaz, onun
yanına ekleme yapar. Üçü de kapalı gelir ve çoğu iş için kapalı kalması yeterlidir.</p>
{sekil("04d_cikti_formati.png", "Çıktı formatı seçenekleri", "üçü de isteğe bağlıdır; PDF her hâlükârda üretilir", dar=True)}
<table>
  <tr><th>Seçenek</th><th>Ne işe yarar</th><th>Ne zaman açın</th></tr>
  <tr>
    <td><b>Kayıpsız baskı</b></td>
    <td>PDF'in içine gömülen parçalar JPEG yerine PNG olur; yani PDF'te hiç JPEG
        bozulması kalmaz.</td>
    <td>Afiş, logo, yazı ve keskin kenarlı grafiklerde. Bu tür görsellerde harf ve çizgi
        kenarındaki hafif gölgelenme tamamen kalkar, üstelik dosya çoğu zaman
        <i>küçülür</i>. Fotoğraf posterlerinde ise dosya belirgin büyür.</td>
  </tr>
  <tr>
    <td><b>Çok sayfalı TIFF</b></td>
    <td>Bütün sayfaları tek bir <code>.tif</code> dosyasında toplar. Kayıpsız, 300 DPI
        etiketli, sayfa sırası PDF ile aynı.</td>
    <td>Matbaaya iş verirken. Birçok matbaa PDF yerine TIFF ister; bu dosya doğrudan
        onlara gider.</td>
  </tr>
  <tr>
    <td><b>Sayfaları ayrıca PNG kaydet</b></td>
    <td>Her sayfayı ayrı bir kayıpsız PNG dosyası olarak da yazar.</td>
    <td>Tek bir sayfayı başka bir programda kullanacaksanız ya da yeniden
        bastıracaksanız.</td>
  </tr>
</table>
<div class="kutu">
  <strong>Not:</strong> “Kayıpsız baskı” zaten açıksa parçalar hâlihazırda PNG olarak
  yazılır; program ikinci bir kopya üretmez. Montaj haritası sayfası çizim olarak
  saklandığı için yalnızca PDF'te bulunur, TIFF'e girmez — bu yüzden TIFF'in sayfa sayısı
  PDF'inkinden bir eksik olabilir.
</div>

<h3>Üretim</h3>
<p><code>Oranı Koru ve Hazır PDF Üret</code> düğmesine basın. Alt satırda
“Parça üretiliyor: 3 / 6” gibi ilerleme görünür; büyük görsellerde bu birkaç saniye sürer.
Bitince özet penceresi açılır.</p>
{sekil("06_tamamlandi.png", "Üretim tamamlandı penceresi", "çıktı klasörünün tam yolunu gösterir")}
<p>Pencereyi <b>Tamam</b> ile kapattıktan sonra <code>Çıktı Klasörünü Aç</code> düğmesi
etkinleşir; dosya yöneticisini doğrudan o klasörde açar.</p>
{sekil("07_bitis_durumu.png", "Üretim sonrası ana ekran", "alt satırda üretilen PDF adı yazar")}

<h2 id="cikti">9. Çıktı klasöründe ne var?</h2>
<p>Her üretim, tarih-saat damgalı ayrı bir klasöre yazılır; eski çıktıların üzerine
<b>asla</b> yazılmaz.</p>
<pre><code>Masaüstü/
└── Poster_Parcalari/
    └── Poster_OranKorumali_20260805_100535/
        ├── Oran_Korumali_Baski_20260805_100535.pdf   ← yazdırılacak dosya
        ├── parca_satir1_sutun1.jpg                   ← tek tek parçalar
        ├── parca_satir1_sutun2.jpg
        ├── ...
        └── baski_raporu.txt                          ← hangi ayarla basıldığı</code></pre>
<p>Normalde sadece PDF'i yazdırmanız yeterlidir. JPEG parçalar, tek bir sayfayı yeniden
bastırmak veya başka bir programda kullanmak isterseniz durur.</p>
<p>Çıktı formatı kutularını açtıysanız (bkz. <a href="#uretim">bölüm 8</a>) aynı klasöre
şunlar da yazılır:</p>
<pre><code>        ├── Oran_Korumali_Baski_20260805_100535.tif   ← matbaa için
        ├── parca_satir1_sutun1.png                   ← kayıpsız sayfalar
        └── parca_satir1_sutun2.png</code></pre>
<p>“Kayıpsız baskı” açıkken parçalar <code>.jpg</code> yerine doğrudan <code>.png</code>
olarak yazılır; yani klasörde JPEG bulunmaz.</p>
{sekil("09_a4_sayfa_ornegi.png", "PDF'in ilk sayfası", "her sayfa tek bir parçayı taşır", 900)}

<h2 id="yazdirma">10. Yazdırma ayarları (en kritik adım)</h2>
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

<h2 id="birlestirme">11. Kesme ve birleştirme</h2>
<div class="kutu kutu-ok">
  <b>Program size yardım eder.</b> Kesim işaretleri açıkken her sayfada şunlar bulunur:
  kesikli <b>kesim çizgisi</b> (buradan kesin), köşelerde <b>kesim işaretleri</b>,
  bindirme şeridinin ortasında <b>kırmızı artı hedefleri</b> (iki sayfayı üst üste
  getirirken bu artılar çakışmalı) ve sayfanın altında <b>parça etiketi</b>
  (“Parca 2-3 · saginda 2-4, altinda 3-3”). PDF'in ilk sayfasındaki <b>montaj haritası</b>
  ise bütün parçaların yerleşimini tek bakışta gösterir.
</div>
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

<h2 id="dizme">12. Çok resmi tek A4'e dizme</h2>
<p>Programın ikinci modu, poster bölmenin tam tersini yapar: <b>birçok resmi tek A4
sayfaya ızgara halinde dizer</b>. Ürün fotoğrafları, katalog sayfası, öğrenci çalışmaları
ya da vesikalık baskısı gibi işlerde kâğıt israfını önler.</p>
<p>Sol panelin en üstündeki <b>“Çok resmi tek A4'e diz”</b> seçeneğini işaretleyin; panel
bu moda göre değişir.</p>
{sekil("10_dizme_modu.png", "Dizme modu", "sağda ilk sayfanın önizlemesi anında görünür")}

<h3>Adım adım</h3>
<ol>
  <li><b>Resimleri Seç (çoklu)</b> ile dosyaları seçin — pencerede Ctrl (macOS'ta Cmd)
      tuşuna basılı tutarak birden çok dosya işaretleyebilirsiniz. Bütün bir klasörü
      almak isterseniz <b>Klasördeki Tüm Resimler</b> düğmesini kullanın.</li>
  <li><b>Sütun</b> ve <b>satır</b> sayısını girin. Sayfa başına kaç resim düşeceğini ve
      toplam kaç sayfa çıkacağını program alt satırda kendisi yazar.</li>
  <li>Gerekirse <b>sayfa yönünü</b>, <b>kenar boşluğunu</b> ve <b>resimler arası
      boşluğu</b> ayarlayın (milimetre cinsinden). Önizleme her değişiklikte yenilenir.</li>
  <li><b>Resimleri A4 Sayfalara Diz</b> düğmesine basın.</li>
</ol>

<div class="kutu kutu-bilgi">
  <b>Resimler kırpılmaz ve gerilmez.</b> Her resim, kendi oranı korunarak hücresine
  sığdırılır ve hücrede ortalanır. Bu yüzden dikey ve yatay resimler bir arada olduğunda
  aralarda beyaz boşluk kalması normaldir — alternatifi, resmin kenarlarından kesmek
  olurdu.
</div>

<div class="kutu kutu-bilgi">
  <b>Sıralama:</b> Dosyalar adlarına göre, sayılar sayısal olarak sıralanır; yani
  <code>resim2</code> her zaman <code>resim10</code>'dan önce gelir. İstediğiniz sırayı
  elde etmek için dosyaları <code>01, 02, 03…</code> gibi adlandırmanız yeterlidir.
</div>

<p>Çıktı, poster modundaki gibi masaüstündeki <code>Poster_Parcalari</code> klasörüne
düşer: her sayfanın JPEG hali ve hepsini içeren tek bir PDF. Sayfalar 300 DPI, gerçek A4
ölçüsündedir (2480 × 3508 piksel); yazdırırken yine <b>%100 / Gerçek Boyut</b> seçin.</p>

<h2 id="sorun">13. Sık karşılaşılan durumlar</h2>
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

<h2 id="teknik">14. Teknik notlar</h2>
<ul>
  <li><b>Sünme yok:</b> Görsel, sayfa matrisinin oranına <i>doldurularak değil</i>, oranı
      korunarak yerleştirilir; artan alan beyaz bırakılır.</li>
  <li><b>Tek ölçek garantisi:</b> Kenar parçalarında eksik kalan bindirme payı beyazla
      tamamlanır; böylece bütün parçalar aynı piksel boyutunda üretilir ve tüm sayfalar
      birebir aynı ölçekle basılır.</li>
  <li><b>Kalite:</b> Parçalar JPEG kalite 95, renk alt örneklemesi kapalı (4:4:4),
      300 DPI etiketiyle kaydedilir. “Kayıpsız baskı” açıkken bunun yerine PNG (Flate)
      kullanılır ve PDF hiç JPEG akışı taşımaz.</li>
  <li><b>TIFF çıktısı:</b> Kayıpsız ZIP/deflate sıkıştırma, 300 DPI etiketi. Sayfalar
      üretildikleri anda tek tek dosyaya akıtılır, hepsi birden belleğe alınmaz. Klasik
      TIFF sayfa adreslerini 32 bitte tuttuğu için 4 GB'lık bir sınır vardır; iş bu sınıra
      dayanırsa TIFF orada durdurulur ve size bildirilir — bozuk dosya üretilmez.</li>
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

<h2 id="baglantilar">15. Bağlantılar</h2>
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

<h2 id="kurulum">16. Kaldırma, taşıma ve internetsiz kurulum</h2>
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
  <b>İnternetsiz bilgisayarda kurulum:</b> Bileşenlerin inebilmesi için ilk açılışta
  internet gerekir. Hedef bilgisayarda hiç internet olmayacaksa, internetli bir
  bilgisayarda şu komutla paketleri indirin:
  <code>pip download pillow reportlab pypdfium2 pillow-heif rawpy -d paketler</code>.
  Oluşan <code>paketler</code> klasörünü program klasörüyle birlikte taşıyın ve hedef
  makinede <code>pip install --no-index --find-links paketler pillow reportlab pypdfium2
  pillow-heif rawpy</code> komutunu bir kez çalıştırın.
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
  figure.dar img {{ width: auto; max-width: 100%; }}
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

# powered by Ömer ÖZTÜRK & Mustafa ŞEKER
