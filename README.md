# TaskManager

Python ve PyQt6 kullanılarak geliştirilen masaüstü görev yönetimi uygulaması.

> **Durum:** Geliştirme aşamasında 🚧

## 🎯 Projenin Amacı

Günlük görevleri takip etmek, tamamlanan görevlerden sanal mücevher kazanmak ve bu mücevherleri uygulama içerisindeki ödüllerde kullanmak.

Proje başlangıçta Excel + VBA ile oluşturulan bir görev ve ödül sisteminin, daha profesyonel bir masaüstü uygulamasına dönüştürülmesi amacıyla geliştirilmektedir.

## 🛠️ Kullanılan Teknolojiler

* Python
* PyQt6
* SQLite *(planlanıyor)*
* Git / GitHub

## 📌 Mevcut Özellikler

* [x] PyQt6 uygulama penceresi
* [x] Mücevher bakiyesinin gösterilmesi
* [x] Görev Ekle butonu
* [x] Buton tıklama olayının oluşturulması
* [x] Git ile sürüm kontrolü
* [x] GitHub repository bağlantısı

## 🚧 Planlanan Özellikler

* [ ] Görev ekleme arayüzü
* [ ] Görev listesi
* [ ] Görev tamamlama
* [ ] Mücevher kazanma sistemi
* [ ] Mücevher harcama sistemi
* [ ] Mağaza
* [ ] İşlem geçmişi
* [ ] Görev güncelleme
* [ ] Görev silme
* [ ] Silinen görevlerin 30 gün saklanması
* [ ] SQLite veritabanı
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

## 📁 Proje Yapısı

```text
TaskManager/
│
├── .venv/          # Sanal Python ortamı
├── .gitignore      # Git tarafından yok sayılan dosyalar
├── main.py         # Uygulamanın başlangıç dosyası
└── README.md       # Proje açıklaması
```

## 📈 Geliştirme Süreci

Bu proje küçük adımlarla geliştirilmektedir.

Her yeni özellik önce geliştirilir ve test edilir, ardından Git ile commit edilerek GitHub'a gönderilir.

## 📄 Lisans

Lisans henüz belirlenmemiştir.
