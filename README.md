# TaskManager

Python ve PyQt6 kullanılarak geliştirilen masaüstü görev yönetimi uygulaması.

> **Durum:** Kasım 2026'da arayüz modernize edildi (gruplu kart düzeni,
> renkli kategori rozetleri, hover animasyonlu butonlar). Planlanan diğer
> tüm özellikler (işlem geçmişi, istatistikler, Ollama destekli kategori
> önerisi) tamamlandı. Yeni bir fikir geldiğinde buradan devam edilecek.

## 🎯 Projenin Amacı

Günlük görevleri takip etmek, tamamlanan görevlerden sanal mücevher kazanmak ve bu mücevherleri uygulama içerisindeki ödüllerde kullanmak.

Proje başlangıçta Excel + VBA ile oluşturulan bir görev ve ödül sisteminin, daha profesyonel bir masaüstü uygulamasına dönüştürülmesi amacıyla geliştirilmektedir.

## 🛠️ Kullanılan Teknolojiler

* Python
* PyQt6
* SQLite
* Git / GitHub

## 📌 Mevcut Özellikler

* [x] PyQt6 uygulama penceresi
* [x] Mücevher bakiyesinin gösterilmesi
* [x] Görev ekleme arayüzü
* [x] Görev listesi (QListWidget)
* [x] Görev tamamlama (onay kutusu, üstü çizili gösterim)
* [x] Görev güncelleme
* [x] Görev silme
* [x] Silinen görevlerin Çöp Kutusu'nda 30 gün saklanması (geri yükleme / kalıcı silme, otomatik temizlik)
* [x] SQLite veritabanı ile kalıcı saklama
* [x] Görevleri kategorilere ayırma (Genel, İş, Kişisel, Alışveriş, Sağlık) ve kategoriye göre filtreleme
* [x] Görevi başka bir kategoriye taşıma
* [x] Kategori adlarını düzenleme (yeniden adlandırma)
* [x] Mücevher kazanma sistemi (görev tamamlandığında mücevher kazanılır, işaret kaldırılınca geri alınır)
* [x] Görev listesinde seçili satırın renkle belirginleştirilmesi
* [x] Kullanıcı adının sorulup kalıcı saklanması ve açılışta hoş geldiniz mesajı
* [x] Görev ekleme/güncelleme/silme sonrası "başka bir işlem yapmak ister misiniz?" akışı
* [x] Mağaza (kullanıcının kendi ödüllerini ekleyip düzenleyip silebildiği) ve mücevher harcama sistemi
* [x] İşlem geçmişi (görev, kategori ve mağaza işlemlerinin kaydı; 30 gün saklanır)
* [x] Gruplanmış buton düzeni (görev işlemleri ve yönetim işlemleri ayrı satırlarda)
* [x] Proje mimarisinin ui / logic / data katmanlarına ayrılması
* [x] Git ile sürüm kontrolü
* [x] Tekrarlanan (günlük) görevler — her gün otomatik sıfırlanma, mücevher kazanımı her tamamlamada ayrı ayrı işler
* [x] GitHub repository bağlantısı
* [x] İstatistik ve grafikler (tamamlanma oranı, kategori dağılımı, mücevher kazanım/harcama özeti)
* [x] Tekrarlanan görevler için seri (streak) takibi — kaç gündür kesintisiz tamamlandığı listede gösterilir
* [x] Modern arayüz teması (merkezi QSS: indigo vurgu rengi, kart görünümlü gruplu araç çubuğu, yuvarlak köşeli butonlar)
* [x] Görev satırlarında renkli kategori rozetleri (kategori pozisyonuna göre renklendirilmiş pill etiketler)
* [x] Butonlarda hover animasyonu (metin rengi fare üzerine gelince yumuşakça canlanır, uzaklaşınca soluklaşır)
* [x] Akıllı kategori önerisi (anahtar kelime eşleştirme + Ollama ile, görev eklerken otomatik önerilir)

## 🚧 Planlanan Özellikler



## 💻 Kurulum

Projeyi klonladıktan sonra proje klasöründe sanal ortam oluşturun:

```bash
python -m venv .venv
```

Sanal ortamı etkinleştirin.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

Kategori önerisi özelliği için [Ollama](https://ollama.com) kurulu ve
çalışıyor olmalı. Önce temel model indirilmeli:

```bash
ollama pull qwen2.5:7b-instruct
```

Ardından proje köküne eklenmiş `Modelfile` ile, kategori önerisine özel
`taskmanager-kategori` modeli oluşturulmalı (sistem talimatı ve
`temperature` ayarı bu dosyada tanımlıdır, kodda tekrar edilmez):

```bash
ollama create taskmanager-kategori -f Modelfile
```

`Modelfile` içeriğini değiştirirseniz (örn. temel modeli veya sistem
talimatını güncellerseniz), yukarıdaki `ollama create` komutunu tekrar
çalıştırmanız gerekir — aksi halde değişiklik modele yansımaz.

Ollama kurulu değilse, `taskmanager-kategori` modeli oluşturulmamışsa
veya Ollama çalışmıyorsa, uygulama bundan etkilenmez — sadece anahtar
kelime eşleşmesi olmayan görevlerde kategori önerisi gösterilmez.

Uygulamayı çalıştırın:

```bash
python main.py
```

Uygulama ilk çalıştırmada proje klasöründe `gorevler.db` adlı bir SQLite veritabanı dosyası oluşturur (bu dosya Git'e dahil edilmez).

## 📁 Proje Yapısı

```text
TaskManager/
│
├── .venv/                      # Sanal Python ortamı
├── .gitignore                  # Git tarafından yok sayılan dosyalar
├── main.py                     # Uygulamanın başlangıç dosyası
├── Modelfile                   # Ollama "taskmanager-kategori" modeli tanımı
├── ui/                         # Arayüz katmanı
│   ├── ana_pencere.py          # Ana pencere (AnaPencere)
│   ├── animasyonlu_buton.py    # Hover'da metin rengi animasyonlu buton (AnimasyonluButon)
│   ├── gorev_satiri_widget.py  # Görev listesi satırı: checkbox + ad + kategori rozeti (GorevSatiriWidget)
│   ├── cop_kutusu_penceresi.py # Çöp Kutusu penceresi (CopKutusuPenceresi)
│   ├── kategori_duzenleme_penceresi.py # Kategori yeniden adlandırma penceresi
│   ├── magaza_penceresi.py     # Mağaza penceresi (MagazaPenceresi)
│   ├── islem_gecmisi_penceresi.py # İşlem Geçmişi penceresi (IslemGecmisiPenceresi)
│   ├── istatistikler_penceresi.py # İstatistikler penceresi (IstatistiklerPenceresi)
│   └── stil.qss                # Merkezi QSS teması
├── logic/                      # İş mantığı katmanı
│   ├── gorev_yonetimi.py       # GorevYonetimi, kategori listesi, IslemTuru
│   └── kategori_onerici.py     # Kategori önerisi (anahtar kelime + Ollama)
├── data/                       # Veri erişim katmanı
│   └── veritabani.py           # VeriTabani (SQLite CRUD işlemleri)
├── gorevler.db                 # SQLite veritabanı (Git'e dahil değil)
├── README.md                   # Proje açıklaması
└── requirements.txt            # Python bağımlılıkları

```

## 📈 Geliştirme Süreci

Bu proje küçük adımlarla geliştirilmektedir.

Her yeni özellik önce geliştirilir ve test edilir, ardından Git ile commit edilerek GitHub'a gönderilir.

## 📄 Lisans

Lisans henüz belirlenmemiştir.