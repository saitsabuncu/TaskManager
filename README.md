# TaskManager

Python ve PyQt6 kullanılarak geliştirilen masaüstü görev yönetimi uygulaması.

> **Durum:** Geliştirme aşamasında 🚧

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
* [x] GitHub repository bağlantısı

## 🚧 Planlanan Özellikler
* [ ] İstatistik ve grafikler
* [ ] Modern kullanıcı arayüzü
* [ ] Ollama entegrasyonu

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
pip install PyQt6
```

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
├── ui/                         # Arayüz katmanı
│   ├── ana_pencere.py          # Ana pencere (AnaPencere)
│   ├── cop_kutusu_penceresi.py # Çöp Kutusu penceresi (CopKutusuPenceresi)
│   ├── kategori_duzenleme_penceresi.py # Kategori yeniden adlandırma penceresi
│   ├── magaza_penceresi.py     # Mağaza penceresi (MagazaPenceresi)
│   └── islem_gecmisi_penceresi.py # İşlem Geçmişi penceresi (IslemGecmisiPenceresi)
├── logic/                      # İş mantığı katmanı
│   └── gorev_yonetimi.py       # GorevYonetimi, kategori listesi, IslemTuru
├── data/                       # Veri erişim katmanı
│   └── veritabani.py           # VeriTabani (SQLite CRUD işlemleri)
├── gorevler.db                 # SQLite veritabanı (Git'e dahil değil)
└── README.md                   # Proje açıklaması
```

## 📈 Geliştirme Süreci

Bu proje küçük adımlarla geliştirilmektedir.

Her yeni özellik önce geliştirilir ve test edilir, ardından Git ile commit edilerek GitHub'a gönderilir.

## 📄 Lisans

Lisans henüz belirlenmemiştir.