# iPhone Fiyat Tahmin Sistemi - Veri Seti Açıklaması

## 📊 Veri Seti Genel Bilgileri

**Dosya Adı**: `profesyonel_telefon_verileri2.csv`
**Toplam Kayıt**: 9.142 adet
**Özellik Sayısı**: 43 adet
**Tarih Aralığı**: 2023-2024 dönemi
**Boyut**: ~2.5 MB

## 📋 Sütun Açıklamaları

### 🗓️ Zaman Bilgisi
- **TARIH**: Fiyat kaydının alındığı tarih (YYYY-MM-DD formatında)

### 📱 Ürün Bilgileri
- **MODEL**: iPhone model adı (iPhone 13, 14, 15, 16)
- **KAPASITE**: Depolama kapasitesi (128GB, 256GB, 512GB, 1TB)
- **RENK**: Ürün rengi
- **URUN_KODU**: Benzersiz ürün kimlik kodu

### 💰 Fiyat Bilgileri
- **FIYAT**: Güncel satış fiyatı (TL cinsinden)
- **ORJINAL_FIYAT**: Apple'ın resmi fiyatı
- **INDIRIM_ORANI**: İndirim yüzdesi
- **KAMPANYA_DURUMU**: Kampanya kategorisi

### 🔧 Teknik Özellikler
- **RAM_GB**: RAM kapasitesi (GB)
- **DAHILI_DEPOLAMA**: Depolama alanı (GB)
- **BATARYA_MAH**: Batarya kapasitesi (mAh)
- **KAMERA_MP**: Ana kamera çözünürlüğü (MP)
- **CHIPSET**: İşlemci modeli
- **EKRAN_BOYUTU**: Ekran boyutu (inç)
- **EKRAN_COZUNURLUGU**: Ekran çözünürlüğü
- **5G_DESTEGI**: 5G ağ desteği (Evet/Hayır)
- **SU_GECIRMEZLIK_SEVIYESI**: Su geçirmezlik standardı

### 📊 Performans Metrikleri
- **DXOMARK_PUAN**: DxOMark kamera puanı
- **PERFORMANS_SKORU**: Hesaplanan genel performans skoru
- **FIYAT_PERFORMANS_ORANI**: Fiyat/performans dengesi
- **GENEL_PUAN**: Toplam değerlendirme puanı

### 🛍️ Pazar Bilgileri
- **STOK_DURUMU**: Ürün stok bilgisi
- **SATICI**: Satıcı bilgisi
- **GARANTI_SURESI**: Garanti süresi (ay)
- **URUN_YASI_GUN**: Ürünün piyasada olma süresi (gün)

### 🏷️ Kategori Bilgileri
- **KAMPANYA_KATEGORI**: Kampanya türü
- **HEDEF_KITLE**: Hedef kullanıcı segmenti
- **PAZARLAMA_ETIKETI**: Pazarlama kategorisi

## 🎯 Veri Örnekleri

### Örnek Kayıt
```csv
TARIH,MODEL,KAPASITE,FIYAT,PERFORMANS_SKORU,KAMPANYA_DURUMU
2024-01-15,iPhone 15,256GB,45999,158.5,Normal Fiyat
2024-01-16,iPhone 15,256GB,41399,158.5,İndirim
2024-01-17,iPhone 14,128GB,35999,142.3,Normal Fiyat
```

## 📈 Veri Dağılımları

### Model Dağılımı
- iPhone 16: %25 (2.286 kayıt)
- iPhone 15: %30 (2.743 kayıt) 
- iPhone 14: %28 (2.560 kayıt)
- iPhone 13: %17 (1.553 kayıt)

### Kapasite Dağılımı
- 128GB: %35
- 256GB: %40
- 512GB: %20
- 1TB: %5

### Kampanya Durumu
- Normal Fiyat: %78
- İndirim: %15
- Büyük İndirim: %5
- Mega İndirim: %2

## 🔄 Veri Hazırlama Süreci

### 1. Ham Veri Toplama
- Apple resmi fiyat listeleri
- Yetkili satıcı fiyatları
- Teknik özellik veritabanları

### 2. Veri Temizleme
- Eksik değer kontrolü
- Outlier tespiti ve temizleme
- Format standardizasyonu

### 3. Özellik Mühendisliği
- Performans skoru hesaplama
- Fiyat/performans oranı
- Ürün yaşı hesaplama
- Kampanya kategorilendirme

### 4. Veri Zenginleştirme
- DxOMark puanları ekleme
- Pazar segmentasyonu
- Sezonsal etiketleme

## ⚠️ Veri Kısıtlamaları

### Eksik Veriler
- Bazı modellerde DxOMark puanı eksik
- Eski modellerde yeni özellikler yok
- Kampanya verilerinde tarih boşlukları

### Veri Kalitesi
- %95 veri tamlığı
- %3 outlier oranı
- %2 eksik değer oranı

## 📊 Kullanım Önerileri

### Analiz İçin
```python
# Veri yükleme
df = pd.read_csv('profesyonel_telefon_verileri2.csv')
df['TARIH'] = pd.to_datetime(df['TARIH'])
df['FIYAT'] = pd.to_numeric(df['FIYAT'])

# Temel istatistikler
print(df.describe())
print(df.info())
```

### Filtreleme Örnekleri
```python
# iPhone 15 verileri
iphone15_data = df[df['MODEL'] == 'iPhone 15']

# 2024 verileri
data_2024 = df[df['TARIH'].dt.year == 2024]

# İndirimli ürünler
indirimliler = df[df['KAMPANYA_DURUMU'].str.contains('İndirim')]
```

## 🔐 Veri Gizliliği

- Kişisel bilgi içermez
- Sadece halka açık fiyat bilgileri
- Ticari hassas bilgi yok
- GDPR uyumlu

## 📞 Veri Desteği

Veri seti ile ilgili sorularınız için:
- 📧 Email: furkanturker2003@gmail.com
- 📋 Issue: GitHub repository
- 📚 Dokümantasyon: README.md

---

*Bu veri seti akademik ve eğitim amaçlı kullanım için hazırlanmıştır.*
