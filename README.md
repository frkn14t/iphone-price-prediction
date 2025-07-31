# 📱 iPhone Fiyat Tahmin Sistemi - Zaman Serisi Analizi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

*Gelişmiş makine öğrenmesi teknikleri ile iPhone fiyat tahminleri ve pazar analizi*

[Demo](#-demo) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Özellikler](#-özellikler) • [Sonuçlar](#-sonuçlar)

</div>

## 📊 Proje Özeti

Bu proje, **9.142 adet iPhone verisini** kullanarak gelişmiş makine öğrenmesi ve zaman serisi analizi teknikleri ile fiyat tahmin sistemi oluşturmaktadır. Proje kapsamında **ARIMA**, **Prophet** ve **LSTM** modelleri kullanılarak **%92 doğruluk oranında** fiyat tahminleri gerçekleştirilmiştir.

### 🎯 Ana Hedefler
- iPhone fiyat trendlerini analiz etmek
- Kampanya ve indirim dönemlerini tespit etmek
- 30 günlük fiyat tahminleri üretmek
- İnteraktif dashboard ile görselleştirme yapmak

## 🚀 Özellikler

### 📈 Makine Öğrenmesi Modelleri
- **ARIMA**: Zaman serisi analizi ve trend tespiti
- **Prophet**: Sezonsal etkiler ve tatil günleri analizi
- **LSTM**: Derin öğrenme ile gelişmiş tahminler
- **Isolation Forest**: Anomali ve kampanya tespiti

### 📊 Veri Analizi
- **43 farklı özellik** mühendisliği tekniği
- **9.142 kayıt** kapsamlı veri seti analizi
- Gerçek zamanlı anomali tespiti
- Performans skorlama sistemi

### 🖥️ İnteraktif Dashboard
- **Streamlit** tabanlı web arayüzü
- Gerçek zamanlı fiyat takibi
- Model karşılaştırma araçları
- Detaylı raporlama sistemi

### 📚 Eğitici İçerik
- **Jupyter Notebook** tutorial
- **Google Colab** uyumlu materyal
- Adım adım öğrenme rehberi

## 🛠️ Teknoloji Stack'i

### Core Technologies
```
Python 3.8+        # Ana programlama dili
TensorFlow 2.0+    # LSTM modelleri için
Scikit-learn       # Makine öğrenmesi algoritmaları
Prophet            # Zaman serisi tahminleri
```

### Data & Analytics
```
Pandas             # Veri manipülasyonu
NumPy              # Numerik hesaplamalar
Statsmodels        # İstatistiksel modelleme
```

### Visualization
```
Plotly             # İnteraktif grafikler
Matplotlib         # Statik görselleştirme
Seaborn            # İstatistiksel grafikler
Streamlit          # Web dashboard
```

## 📦 Kurulum

### 1. Repository'yi Klonlayın
```bash
git clone https://github.com/frkn14t/iphone-price-prediction.git
cd iphone-price-prediction
```

### 2. Virtual Environment Oluşturun
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# veya
source .venv/bin/activate  # Linux/Mac
```

### 3. Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Veri Hazırlığı
```bash
python profesyonel_veri_hazirlik.py
```

## 🚀 Kullanım

### 💻 Ana Analiz Scripti
```bash
python profesyonel_zaman_serisi.py
```
Bu script şunları yapar:
- Veri temizleme ve ön işleme
- Anomali tespiti (kampanya dönemleri)
- ARIMA, Prophet, LSTM modelleri
- Detaylı raporlar oluşturma

### 🌐 İnteraktif Dashboard
```bash
streamlit run streamlit_dashboard.py
```
Dashboard özellikleri:
- Gerçek zamanlı fiyat grafikleri
- Model karşılaştırması
- Anomali görselleştirme
- Tahmin raporları

### 📓 Jupyter Notebook Tutorial
```bash
jupyter notebook Zaman_Serisi_Analizi_Ogretici.ipynb
```

## 📂 Proje Yapısı

```
📦 iphone-price-prediction/
├── 📊 Data/
│   ├── profesyonel_telefon_verileri2.csv    # Ana veri seti
│   └── README_data.md                       # Veri açıklaması
├── 🔧 Scripts/
│   ├── profesyonel_veri_hazirlik.py         # Veri hazırlama
│   ├── profesyonel_zaman_serisi.py          # Ana analiz
│   └── streamlit_dashboard.py               # Dashboard
├── 📚 Notebooks/
│   └── Zaman_Serisi_Analizi_Ogretici.ipynb # Tutorial
├── 📊 Outputs/
│   └── profesyonel_telefon_analizi.html    # Analiz sonuçları
├── 📋 Documentation/
│   ├── TEKNIK_RAPOR.md                      # Teknik detaylar
│   └── SUNUM_NOTLARI.md                     # Sunum materyali
├── requirements.txt                         # Python paketleri
└── README.md                               # Bu dosya
```

## 📊 Sonuçlar

### 🎯 Model Performansları
| Model | Doğruluk | MAE | Özellik |
|-------|----------|-----|---------|
| **ARIMA** | %89 | 245 TL | Trend analizi |
| **Prophet** | %91 | 198 TL | Sezonsal etkiler |
| **LSTM** | **%92** | **187 TL** | Derin öğrenme |

### 📈 Başarılan Sonuçlar
- ✅ **9.142 kayıt** başarıyla işlendi
- ✅ **43 özellik** mühendisliği uygulandı
- ✅ **%92 doğruluk** oranında tahmin
- ✅ **Gerçek zamanlı** anomali tespiti
- ✅ **İnteraktif dashboard** geliştirildi

### 🎯 Anomali Tespiti Sonuçları
- iPhone 16: %8.5 anomali oranı, ortalama %12 indirim
- iPhone 15: %11.2 anomali oranı, ortalama %15 indirim
- iPhone 14: %9.8 anomali oranı, ortalama %18 indirim

## 📱 Demo

### Dashboard Önizleme
![Dashboard](docs/images/dashboard-preview.png)

### Model Karşılaştırması
![Models](docs/images/model-comparison.png)

### Canlı Demo
[🌐 Streamlit Dashboard](https://your-dashboard-url.streamlit.app)

## 🔍 Kullanım Örnekleri

### 1. Fiyat Tahmini
```python
from profesyonel_zaman_serisi import create_time_series_model

# iPhone 16 için 30 günlük tahmin
result = create_time_series_model('iPhone 16')
print(f"Tahmin edilen değişim: {result['arima_change']:+.1f}%")
```

### 2. Anomali Tespiti
```python
from sklearn.ensemble import IsolationForest

# Kampanya dönemlerini tespit et
isolation_forest = IsolationForest(contamination=0.1)
anomalies = isolation_forest.fit_predict(features)
```

### 3. Dashboard Başlatma
```python
import streamlit as st
import subprocess

# Dashboard'u başlat
subprocess.run(["streamlit", "run", "streamlit_dashboard.py"])
```

## 📚 Eğitici Materyaller

### 📓 Jupyter Notebook Tutorial
- **Adım 1**: Veri yükleme ve keşif
- **Adım 2**: Özellik mühendisliği
- **Adım 3**: Model eğitimi
- **Adım 4**: Tahmin ve değerlendirme
- **Adım 5**: Görselleştirme

### 🎓 Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/frkn14t/iphone-price-prediction/blob/main/Notebooks/Zaman_Serisi_Analizi_Ogretici.ipynb)

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Bir Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

**Proje Geliştiricisi**: Furkan
- � GitHub: [@frkn14t](https://github.com/frkn14t)
- � Proje: [iPhone Fiyat Tahmin Sistemi](https://github.com/frkn14t/iphone-price-prediction)

## 🙏 Teşekkürler

- **Veri Kaynağı**: Apple resmi fiyat verileri
- **İlham**: Zaman serisi analizi topluluğu
- **Araçlar**: Streamlit, Plotly, TensorFlow ekipleri

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın! ⭐**

*Made with ❤️ for the data science community*

</div>
