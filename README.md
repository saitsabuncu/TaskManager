# TaskManager

Python ve PyQt6 kullanılarak geliştirilen masaüstü görev yönetimi uygulaması.

> **Durum:** Kasım 2026'da arayüz modernize edildi (açılır menü butonları,
> renkli kategori rozetleri, hover animasyonlu birincil buton, anlık arama),
> `pytest` ile otomatik test altyapısı kuruldu ve kapsamlı klavye kısayolları
> eklendi. Planlanan diğer tüm özellikler (işlem geçmişi, istatistikler,
> Ollama destekli kategori önerisi) tamamlandı. Yeni bir fikir geldiğinde
> buradan devam edilecek.

## 🎯 Projenin Amacı

Günlük görevleri takip etmek, tamamlanan görevlerden sanal mücevher kazanmak ve bu mücevherleri uygulama içerisindeki ödüllerde kullanmak.

Proje başlangıçta Excel + VBA ile oluşturulan bir görev ve ödül sisteminin, daha profesyonel bir masaüstü uygulamasına dönüştürülmesi amacıyla geliştirilmektedir.

## 🛠️ Kullanılan Teknolojiler

* Python
* PyQt6
* SQLite
* Git / GitHub
* pytest (otomatik testler)

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
* [x] Yeni kategori ekleme
* [x] Kategori adlarını düzenleme (yeniden adlandırma)
* [x] Mücevher kazanma sistemi (görev tamamlandığında mücevher kazanılır, işaret kaldırılınca geri alınır)
* [x] Görev listesinde seçili satırın renkle belirginleştirilmesi
* [x] Kullanıcı adının sorulup kalıcı saklanması ve açılışta hoş geldiniz mesajı
* [x] Görev ekleme/güncelleme/silme sonrası "başka bir işlem yapmak ister misiniz?" akışı
* [x] Mağaza (kullanıcının kendi ödüllerini ekleyip düzenleyip silebildiği) ve mücevher harcama sistemi
* [x] İşlem geçmişi (görev, kategori ve mağaza işlemlerinin kaydı; 30 gün saklanır)
* [x] Proje mimarisinin ui / logic / data katmanlarına ayrılması
* [x] Git ile sürüm kontrolü
* [x] Tekrarlanan (günlük) görevler — her gün otomatik sıfırlanma, mücevher kazanımı her tamamlamada ayrı ayrı işler
* [x] GitHub repository bağlantısı
* [x] İstatistik ve grafikler (tamamlanma oranı, kategori dağılımı, mücevher kazanım/harcama özeti)
* [x] Tekrarlanan görevler için seri (streak) takibi — kaç gündür kesintisiz tamamlandığı listede gösterilir
* [x] Modern arayüz teması (merkezi QSS: indigo vurgu rengi, yuvarlak köşeli butonlar)
* [x] Araç çubuğu açılır menü butonlarında toplandı (Görev İşlemleri / Yönetim) — yeni özellik eklendikçe araç çubuğu büyümez
* [x] Görev satırlarında renkli kategori rozetleri (kategori pozisyonuna göre renklendirilmiş pill etiketler)
* [x] Birincil butonda hover animasyonu (metin rengi fare üzerine gelince yumuşakça canlanır, uzaklaşınca soluklaşır)
* [x] Akıllı kategori önerisi (anahtar kelime eşleştirme + Ollama ile, görev eklerken otomatik önerilir)
* [x] Görev adında anlık arama (kategori filtresiyle birlikte çalışır)
* [x] Görev önceliği (düşük/orta/yüksek) — ekleme sırasında seçilir, sonradan "Görev İşlemleri" menüsünden değiştirilebilir, satırlarda renkli rozetle gösterilir
* [x] Son tarih (deadline) — opsiyonel tarih seçimi, "Görev İşlemleri" menüsünden değiştirilebilir, tamamlanmamış ve süresi geçmiş görevler kırmızı etiketle vurgulanır
* [x] Otomatik testler (`pytest`) — `logic/gorev_yonetimi.py` ve `logic/kategori_onerici.py` için (Ollama çağrıları mock'lanır, geçici dosya tabanlı veritabanı fixture'ı kullanılır)
* [x] Klavye kısayolları — görev ekleme/güncelleme/silme/tamamlama, kategori ekleme/taşıma, öncelik/son tarih/tekrar değiştirme, pencere açma kısayolları ve liste/arama/filtre odaklama (bkz. "Klavye Kısayolları" bölümü)

## 🚧 Planlanan Özellikler

**Teknik borç**
* [ ] Çoklu kullanıcı / profil desteği (şimdilik bilinçli olarak ertelendi; `kullanici_id` kolonu ile ileride eklenecek)

**Özellik fikirleri**
* [ ] Sistem tepsisi bildirimi / hatırlatma
* [ ] Alt görevler (checklist)
* [ ] Esnek tekrar kuralları (haftada N gün, belirli günler)
* [ ] İstatistik/geçmişin CSV veya PDF olarak dışa aktarılması
* [ ] Rozet / başarım sistemi (mevcut mücevher sistemine ek)
* [ ] Ollama'nın kategori önerisi dışında (ör. haftalık özet) kullanılması

## ⌨️ Klavye Kısayolları

| Kısayol | İşlev |
|---|---|
| `Ctrl+N` | Görev Ekle |
| `Ctrl+E` | Görev Güncelle |
| `Delete` *(liste odaktayken)* | Görev Sil |
| `Space` *(liste odaktayken)* | Seçili görevi tamamlandı/tamamlanmadı işaretle |
| `Ctrl+K` | Kategori Taşı |
| `Ctrl+O` | Öncelik Değiştir |
| `Ctrl+D` | Son Tarih Belirle |
| `Ctrl+T` | Tekrarı Aç/Kapat |
| `Ctrl+Shift+N` | Yeni Kategori Ekle |
| `Ctrl+Shift+K` | Kategorileri Düzenle |
| `Ctrl+M` | Mağaza |
| `Ctrl+Shift+C` | Çöp Kutusu |
| `Ctrl+H` | İşlem Geçmişi |
| `Ctrl+I` | İstatistikler |
| `Ctrl+F` | Arama kutusuna odaklan |
| `Ctrl+Shift+F` | Kategori filtresine odaklan |
| `Ctrl+L` | Görev listesine odaklan (ardından Yukarı/Aşağı ok tuşlarıyla görev seçimi) |
| `Ctrl+Q` | Uygulamayı kapat |

Ayrıca onay diyaloglarında (örn. "Görevi Sil") **Tab** ile Evet/Hayır arası geçiş, **Enter** ile odaklanan/varsayılan butonu onaylama, **Esc** ile iptal — bunlar Qt'nin yerleşik diyalog davranışıdır, ek kod gerekmez.

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

### Testleri çalıştırma

```bash
pip install -r requirements-dev.txt
pytest
```

## 📁 Proje Yapısı

```text
TaskManager/
│
├── .venv/                      # Sanal Python ortamı
├── .gitignore                  # Git tarafından yok sayılan dosyalar
├── main.py                     # Uygulamanın başlangıç dosyası
├── Modelfile                   # Ollama "taskmanager-kategori" modeli tanımı
├── pytest.ini                  # pytest yapılandırması (pythonpath, testpaths)
├── requirements-dev.txt        # Geliştirme bağımlılıkları (pytest)
├── ui/                         # Arayüz katmanı
│   ├── ana_pencere.py          # Ana pencere (AnaPencere) — klavye kısayolları dahil
│   ├── animasyonlu_buton.py    # Hover'da metin rengi animasyonlu buton (AnimasyonluButon)
│   ├── gorev_satiri_widget.py  # Görev listesi satırı: checkbox + ad + son tarih/öncelik/kategori rozetleri (GorevSatiriWidget)
│   ├── son_tarih_dialog.py     # Görev için opsiyonel son tarih seçim diyaloğu (SonTarihDialog)
│   ├── cop_kutusu_penceresi.py # Çöp Kutusu penceresi (CopKutusuPenceresi)
│   ├── kategori_duzenleme_penceresi.py # Kategori yeniden adlandırma penceresi
│   ├── magaza_penceresi.py     # Mağaza penceresi (MagazaPenceresi)
│   ├── islem_gecmisi_penceresi.py # İşlem Geçmişi penceresi (IslemGecmisiPenceresi)
│   ├── istatistikler_penceresi.py # İstatistikler penceresi (IstatistiklerPenceresi)
│   └── stil.qss                # Merkezi QSS teması
├── logic/                      # İş mantığı katmanı
│   ├── gorev_yonetimi.py       # GorevYonetimi, kategori listesi, öncelik etiketleri, IslemTuru
│   └── kategori_onerici.py     # Kategori önerisi (anahtar kelime + Ollama)
├── data/                       # Veri erişim katmanı
│   └── veritabani.py           # VeriTabani (SQLite CRUD işlemleri)
├── tests/                      # pytest test paketi
│   ├── conftest.py             # Geçici dosya tabanlı VeriTabani/GorevYonetimi fixture'ları
│   ├── test_gorev_yonetimi.py  # Ekleme, silme, tamamlama/bakiye, öncelik, son tarih testleri
│   └── test_kategori_onerici.py # Anahtar kelime eşleşmesi ve mock'lanmış Ollama testleri
├── gorevler.db                 # SQLite veritabanı (Git'e dahil değil)
├── README.md                   # Proje açıklaması
└── requirements.txt            # Python bağımlılıkları

```

## 📈 Geliştirme Süreci

Bu proje küçük adımlarla geliştirilmektedir.

Her yeni özellik önce geliştirilir, test edilir (manuel ve/veya `pytest` ile), ardından Git ile commit edilerek GitHub'a gönderilir.

## 📄 Lisans

Lisans henüz belirlenmemiştir.