# Product

## Register

brand

## Platform

web

## Users

Öğretmen, kırtasiyeci, veli, esnaf. Bilgisayarla arası orta düzeyde olan, belirli bir işi bitirmeye çalışan insanlar: sınıf panosuna asılacak bir görsel, dükkân vitrinine bir afiş, doğum günü için bir pano. Ellerinde tek bir A4 yazıcı var ve çıktının büyüğünü istiyorlar. Arama motoruna "posteri A4 kağıtlara bölme" yazarak geliyorlar; bir program adı aramıyorlar, bir çözüm arıyorlar. İkincil olarak aynı sayfaya İngilizce arayan, PosteRazor benzeri bir masaüstü aracın Linux'ta çalışanını isteyen kullanıcılar geliyor.

## Product Purpose

Bir görseli oranını bozmadan A4 sayfalara bölüp baskıya hazır PDF üretmek; tersine, çok sayıda resmi tek A4 sayfaya dizmek. Program çevrimdışı çalışır, kurulum istemez ve dosyayı hiçbir sunucuya yüklemez. Başarı, sayfaya gelen kişinin programı indirip ilk posterini çıkarması; ikincil olarak Türkçe ve İngilizce aramalarda bulunabilir olması.

## Positioning

Tarayıcıya dosya yüklemeden, oranı bozmadan çalışan masaüstü poster bölücü. Rakiplerin tamamına yakını sunucuya yükleme isteyen web araçları; buradaki iş bilgisayarın kendi içinde bitiyor.

## Conversion & proof

- Birincil eylem: kullanıcının işletim sistemine uygun paketi indirmek. İkincil: programın ne yaptığını örnek çıktı ve ekran görüntüsüyle görmek.
- On saniye sonra akılda kalması gereken cümle: görseli A4'lere böler, sünme olmaz, dosya bilgisayardan çıkmaz.
- İnanç sırası: (1) bu benim işimi çözer, (2) çıktı kalitesi bozulmaz, (3) kurulum ve teknik bilgi gerektirmez, (4) dosyam bana ait kalır, (5) indirmek güvenli ve ücretsiz.
- Elde olan kanıt: programın kendi ekran görüntüleri (`manuel/gorseller/`), 1:1 önizleme ve baskı raporu çıktıları, açık kaynak deposu ve MIT lisansı.

## Brand Personality

Sakin, işini bilen, abartısız. Somut vaat konuşur, pazarlama sıfatı kullanmaz: "oranı korunur", "kesme payı eklenir", "dosya yüklenmez". Bir baskı atölyesindeki ustanın anlatımı gibi: kısa, kesin, gereksiz kelime yok.

## Anti-references

Rakip web araçlarının kalabalık, reklam kuşaklı, "ÜCRETSİZ! HEMEN DENE!" tonundaki sayfaları. SaaS şablonu: krem zemin, dev metrik kutuları, her başlık üstünde küçük büyük-harfli etiket. Editoryal dergi estetiği (italik serif başlık, ince çizgili sütunlar) — bu bir dergi değil, bir alet. Programın kendi Tk arayüzünü taklit etmek de yanlış olur; arayüz işlevsel, sayfa ise davetkâr olmalı.

## Design Principles

Sayfanın görsel dili ürünün çıktısı olsun: A4 karoları, kesme kılavuzları, hizalama işaretleri, numaralı sayfalar. Süsleme değil, işin kendisi.

Vaadi göster, anlatma. "Sünme yok" cümlesi yerine bozulan ve bozulmayan görselin yan yana durması.

İndirme yolu her zaman bir tık uzakta olsun; kullanıcı sayfanın neresindeyse orada.

İki dil eşit özenle. İngilizce sayfa çeviri artığı gibi durmasın, kendi arama ifadeleriyle yazılsın.

Teknik doğruluk pazarlamadan önce gelir. Yapmadığı bir şey vaat edilmez.

## Accessibility & Inclusion

WCAG 2.2 AA hedeflenir: gövde metninde en az 4.5:1 kontrast, klavyeyle tam gezinme, görünür odak halkası, anlamlı alternatif metinler. Hedef kitle yaş aralığı geniş olduğu için gövde metni 17px'ten küçük olmaz. `prefers-reduced-motion` seçen kullanıcıda hareket kapanır.
