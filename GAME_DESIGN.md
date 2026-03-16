## Void Escape – Oyun Tasarım Özeti

### Genel Bakış

- **Tür**: Tur bazlı, izometrik grid üzerinde taktiksel kaçış oyunu.
- **Tema**: Galaksinin merkezindeki Void boyutu kontrolden çıkmış, alan her tur daralıyor.
- **Oyuncu Sayısı**: 4 koşucu (Alpha, Beta, Gamma, Delta) tek bilgisayardan sırayla kontrol edilir.

### Amaç

- En az **2 anahtar** toplayan bir koşucuyu, Void tarafından yutulmadan önce **merkez kapsüle** ulaştır.
- Merkez kapsül, 12x12 gridin tam ortasındaki karede bulunur (mantıksal koordinat \[6, 6]).

### Harita ve Void Mekaniği

- Harita boyutu **12x12** griddir.
- Başlangıçta tüm karolar **NORMAL** durumdadır.
- Her **8 hamlede** Void seviyesi (**void_level**) 1 artar.
- Void, haritanın kenarlarından içeriye doğru ilerler:
  - Bir karonun kenarlara olan en küçük uzaklığı, o karonun \"katman\" mesafesidir.
  - Bu mesafe, `void_level` değerinden küçük olduğunda karo **VOID** olur ve artık üzerine basılamaz.
- Void ilerlediğinde:
  - Kenar karoları yutulur.
  - Oyuncular bu karolara giremez; eğer daha önce oradaysa tasarım gereği burada sıkışma olmaması hedeflenir.

### Karakterler

- Her koşucunun özellikleri:
  - **HP**: 100
  - **AMMO**: 6
  - **Anahtar Sayısı**: 0’dan başlar.
  - **Durum**: Yaşayan / Ölü
- Her sınıfın (TITAN, PHANTOM, SAGE, ROGUE) sadece rengi farklıdır; şu an için özel yetenek yoktur.
- Başlangıç pozisyonları haritanın dört köşesidir (0,0), (0,11), (11,0), (11,11).

### Anahtarlar ve Kapsül

- Oyun başında 4 anahtar rastgele olarak gridin iç bölgelerine dağılır.
- Bir oyuncu, anahtar olan bir kareye girdiğinde:
  - Anahtar kaybolur.
  - Oyuncunun **anahtar sayısı 1 artar**.
  - Olay, oyun günlüğüne (GameLog) mesaj olarak eklenir.
- Merkez kapsül:
  - Gridin merkezinde sabit bir karodur.
  - En az **2 anahtara sahip** bir oyuncu bu kareye girdiğinde oyunu kazanır.

### Tur Yapısı

- Oyun **tur bazlıdır** ve tek bir tur, aktif koşucunun tek bir hamlesinden oluşur.
- Sıra, koşucular arasında döner:
  - Tur sayacı her hamlede artar, `turn % 4` aktif oyuncuyu belirler.
- Bir hamlede:
  1. Oyuncu **W, A, S, D** tuşlarından biriyle hareket yönünü seçer.
  2. Hareket, hedef karo geçerli ise (harita sınırları içinde ve VOID değil) gerçekleşir.
  3. Hareket sonrası:
     - Anahtar toplanması, çatışma ve kazanma koşulları kontrol edilir.
     - Her 8. hamlede Void seviyesi artar ve harita daralır.

### Kontroller

- **W / A / S / D**: Aktif koşucuyu bir kare yukarı/sol/aşağı/sağa hareket ettirir.
- **ESC**:
  - PLAY esnasında ana menüye döner.
  - Menüdeyken oyundan çıkmanı sağlar.
- **SPACE**:
  - Hikâye ekranında bir sonraki aşamaya geçmek veya oyuna başlamak için kullanılır.
- **H** (yardım, oyunda planlanan):
  - Oyun sırasında temel kuralların ve kontrollerin yazdığı yardım panelini açıp kapatır.

### Çatışma ve Hasar

- İki farklı koşucu aynı karoya girdiğinde bir **çatışma** tetiklenir:
  - Hedef koşucunun **HP değeri 30 azalır**.
  - Saldıran koşucunun **AMMO değeri 1 azalır**.
- HP’si 0 veya altına düşen bir koşucu **ölü** kabul edilir ve artık haritada aktif rol oynamaz.
- Çatışma olayları oyun günlüğünde mesaj olarak gösterilir ve küçük ekran sarsıntısı ile vurgulanır.

### Kazanma ve Kaybetme Koşulları

- **Kazanma**:
  - Bir koşucu, en az **2 anahtara sahipken** merkez kapsül karesine girerse oyunu kazanır.
  - Ekranda o koşucunun rengiyle vurgulanan bir **\"TAHLİYE BAŞARILI\"** mesajı belirir.
- **Kaybetme / Diğer Durumlar**:
  - Tasarımın basit ilk sürümünde, diğer koşucular için ayrı bir kaybetme ekranı yoktur.
  - Void’in haritayı daraltması, oyuncuları stratejik hareket etmeye zorlayan temel tehdit unsurudur.

### Oyuncuya Gösterilen Bilgiler

- Ekranın sol üst panelinde:
  - Aktif koşucunun adı ve sınıf rengi.
  - HP ve AMMO değerleri.
  - Toplanan anahtar sayısı (örn. 0/2).
  - Mevcut Void seviyesi.
  - Kontroller ve kısaca hedef: \"WASD ile hareket et, 2 anahtar topla ve merkeze ulaş\".
- Sağ tarafta kayan oyun günlüğü (GameLog), önemli olayları metin olarak gösterir.

