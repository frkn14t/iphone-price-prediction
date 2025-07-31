import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Zaman serisi kütüphaneleri
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from prophet import Prophet

# Machine Learning kütüphaneleri
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

# Deep Learning (LSTM)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# Dosyayı oku
print("🚀 Profesyonel iPhone Fiyat Analizi ve Tahmin Sistemi")
print("=" * 80)

import os
os.chdir(r"C:\Users\FURKAN\excel_temizlik")

try:
    df = pd.read_csv('profesyonel_telefon_verileri2.csv')
    print(f"📊 Veri seti başarıyla yüklendi: {len(df)} kayıt, {len(df.columns)} özellik")
except Exception as e:
    print(f"❌ Profesyonel veri seti bulunamadı: {e}")
    print("Önce veri hazırlama scriptini çalıştırın.")
    exit()

# Tarih formatını otomatik algıla ve düzelt
try:
    df['TARIH'] = pd.to_datetime(df['TARIH'])
except:
    try:
        df['TARIH'] = pd.to_datetime(df['TARIH'], format='%d.%m.%Y')
    except:
        df['TARIH'] = pd.to_datetime(df['TARIH'], format='%Y-%m-%d')

df['FIYAT'] = pd.to_numeric(df['FIYAT'])

# Eksik sütunları kontrol et ve ekle
if 'PERFORMANS_SKORU' not in df.columns:
    df['PERFORMANS_SKORU'] = 150.0  # Default değer
if 'FIYAT_PERFORMANS_ORANI' not in df.columns:
    df['FIYAT_PERFORMANS_ORANI'] = df['FIYAT'] / 150.0
if 'URUN_YASI_GUN' not in df.columns:
    df['URUN_YASI_GUN'] = 365  # Default 1 yıl

# Numerik dönüşümler
df['PERFORMANS_SKORU'] = pd.to_numeric(df['PERFORMANS_SKORU'], errors='coerce').fillna(150.0)
df['FIYAT_PERFORMANS_ORANI'] = pd.to_numeric(df['FIYAT_PERFORMANS_ORANI'], errors='coerce').fillna(df['FIYAT'] / 150.0)
df['URUN_YASI_GUN'] = pd.to_numeric(df['URUN_YASI_GUN'], errors='coerce').fillna(365)

# Veri seti özeti
print(f"\n📈 Veri Seti Özeti:")
print(f"📅 Tarih aralığı: {df['TARIH'].min().strftime('%d.%m.%Y')} - {df['TARIH'].max().strftime('%d.%m.%Y')}")
print(f"💰 Fiyat aralığı: {df['FIYAT'].min():,.0f} - {df['FIYAT'].max():,.0f} TL")
print(f"🔢 Ortalama fiyat: {df['FIYAT'].mean():,.0f} TL")
print(f"📊 Standart sapma: ±{df['FIYAT'].std():,.0f} TL")

# Model bazında özet
print(f"\n📱 Model Bazında Özet:")
model_ozet = df.groupby('MODEL').agg({
    'FIYAT': ['count', 'mean', 'std'],
    'PERFORMANS_SKORU': 'mean',
    'FIYAT_PERFORMANS_ORANI': 'mean'
}).round(2)
print(model_ozet)

# 1. VERİ TEMİZLEME VE ÖN İŞLEME
print(f"\n🧹 Veri Temizleme ve Ön İşleme")
print("-" * 50)

# Eksik değerleri kontrol et
eksik_degerler = df.isnull().sum()
if eksik_degerler.sum() > 0:
    print(f"⚠️ Eksik değerler tespit edildi:")
    print(eksik_degerler[eksik_degerler > 0])
else:
    print("✅ Eksik değer bulunamadı")

# Outlier tespiti (Z-score yöntemi)
def z_score_outliers(data, threshold=3):
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold

outliers = z_score_outliers(df['FIYAT'])
print(f"🎯 Outlier tespiti: {outliers.sum()} adet outlier bulundu (%{outliers.sum()/len(df)*100:.1f})")

# 2. ANOMALI TESPİTİ (KAMPANYA DÖNEMLERİ)
print(f"\n🔍 Anomali Tespiti - Kampanya Dönemleri")
print("-" * 50)

# Model bazında anomali tespiti
anomali_sonuclari = {}

for model in df['MODEL'].unique():
    model_data = df[df['MODEL'] == model].copy()
    model_data = model_data.sort_values('TARIH')
    
    # Isolation Forest ile anomali tespiti
    isolation_forest = IsolationForest(contamination=0.1, random_state=42)
    
    # Özellik matrisi hazırla
    features = ['FIYAT', 'PERFORMANS_SKORU', 'FIYAT_PERFORMANS_ORANI', 'URUN_YASI_GUN']
    X = model_data[features].fillna(model_data[features].mean())
    
    # Normalizasyon
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Anomali tespiti
    anomalies = isolation_forest.fit_predict(X_scaled)
    model_data['ANOMALI'] = anomalies
    
    # Anomali sonuçlarını kaydet
    anomali_verileri = model_data[model_data['ANOMALI'] == -1]
    anomali_sonuclari[model] = {
        'toplam_anomali': len(anomali_verileri),
        'anomali_orani': len(anomali_verileri) / len(model_data) * 100,
        'ortalama_indirim': ((model_data['FIYAT'].mean() - anomali_verileri['FIYAT'].mean()) / model_data['FIYAT'].mean() * 100) if len(anomali_verileri) > 0 else 0
    }
    
    print(f"📱 {model}:")
    print(f"  🎯 Anomali sayısı: {anomali_sonuclari[model]['toplam_anomali']}")
    print(f"  📊 Anomali oranı: %{anomali_sonuclari[model]['anomali_orani']:.1f}")
    print(f"  💰 Ortalama indirim: %{anomali_sonuclari[model]['ortalama_indirim']:.1f}")

# 3. ZAMAN SERİSİ MODELLEMESİ
print(f"\n📈 Zaman Serisi Modelleme")
print("-" * 50)

def create_time_series_model(model_name, kapasite=None):
    """Belirli model ve kapasite için zaman serisi analizi"""
    
    # Veri filtreleme
    if kapasite:
        model_data = df[(df['MODEL'] == model_name) & (df['KAPASITE'] == kapasite)].copy()
        baslik = f"{model_name} - {kapasite}"
    else:
        model_data = df[df['MODEL'] == model_name].copy()
        baslik = model_name
    
    if len(model_data) < 30:
        print(f"⚠️ {baslik} için yeterli veri yok ({len(model_data)} kayıt)")
        return None
    
    # Günlük ortalama fiyat hesapla
    daily_data = model_data.groupby('TARIH')['FIYAT'].mean().reset_index()
    daily_data = daily_data.sort_values('TARIH')
    
    # ARIMA Modeli
    print(f"\n🔮 {baslik} için ARIMA Modeli")
    
    # Durağanlık testi
    result = adfuller(daily_data['FIYAT'])
    print(f"📊 ADF Test p-değeri: {result[1]:.4f}")
    if result[1] < 0.05:
        print("✅ Seri durağan")
    else:
        print("⚠️ Seri durağan değil - differencing gerekli")
    
    try:
        # ARIMA model eğitimi
        arima_model = ARIMA(daily_data['FIYAT'], order=(1, 1, 1))
        arima_fitted = arima_model.fit()
        
        # 30 günlük tahmin
        arima_forecast = arima_fitted.forecast(steps=30)
        
        print(f"📈 ARIMA 30 günlük ortalama tahmin: {arima_forecast.mean():,.0f} TL")
        print(f"📉 Mevcut ortalama: {daily_data['FIYAT'].iloc[-10:].mean():,.0f} TL")
        
        degisim = ((arima_forecast.mean() - daily_data['FIYAT'].iloc[-10:].mean()) / daily_data['FIYAT'].iloc[-10:].mean() * 100)
        print(f"🎯 Öngörülen değişim: {degisim:+.1f}%")
        
    except Exception as e:
        print(f"❌ ARIMA modeli hatası: {e}")
        arima_forecast = None
    
    # Prophet Modeli
    print(f"\n🔮 {baslik} için Prophet Modeli")
    
    try:
        # Prophet için veri hazırlama
        prophet_data = daily_data[['TARIH', 'FIYAT']].copy()
        prophet_data.columns = ['ds', 'y']
        
        # Prophet model
        prophet_model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )
        
        # Tatil günleri ekle (Türkiye)
        prophet_model.add_country_holidays(country_name='TR')
        
        prophet_model.fit(prophet_data)
        
        # 30 günlük tahmin
        future = prophet_model.make_future_dataframe(periods=30)
        prophet_forecast = prophet_model.predict(future)
        
        gelecek_ortalama = prophet_forecast.tail(30)['yhat'].mean()
        print(f"📈 Prophet 30 günlük ortalama tahmin: {gelecek_ortalama:,.0f} TL")
        
        prophet_degisim = ((gelecek_ortalama - daily_data['FIYAT'].iloc[-10:].mean()) / daily_data['FIYAT'].iloc[-10:].mean() * 100)
        print(f"🎯 Prophet öngörülen değişim: {prophet_degisim:+.1f}%")
        
    except Exception as e:
        print(f"❌ Prophet modeli hatası: {e}")
        prophet_forecast = None
    
    return {
        'model_name': baslik,
        'data': daily_data,
        'arima_forecast': arima_forecast,
        'prophet_forecast': prophet_forecast,
        'current_avg': daily_data['FIYAT'].iloc[-10:].mean(),
        'arima_change': degisim if 'degisim' in locals() else 0,
        'prophet_change': prophet_degisim if 'prophet_degisim' in locals() else 0
    }

# Her model için analiz yap
model_tahminleri = {}
for model in ['iPhone 16', 'iPhone 15', 'iPhone 14', 'iPhone 13']:
    model_tahminleri[model] = create_time_series_model(model)

# 4. LSTM DEEP LEARNING MODELİ
print(f"\n🤖 LSTM Deep Learning Modeli")
print("-" * 50)

def create_lstm_model(model_name):
    """LSTM modeli ile fiyat tahmini"""
    
    model_data = df[df['MODEL'] == model_name].copy()
    model_data = model_data.sort_values('TARIH')
    
    if len(model_data) < 100:
        print(f"⚠️ {model_name} için LSTM'e yeterli veri yok")
        return None
    
    # Günlük ortalama fiyat
    daily_data = model_data.groupby('TARIH')['FIYAT'].mean().reset_index()
    prices = daily_data['FIYAT'].values.reshape(-1, 1)
    
    # Normalizasyon
    scaler = MinMaxScaler()
    prices_scaled = scaler.fit_transform(prices)
    
    # Sekans oluşturma (60 günlük pencere)
    def create_sequences(data, seq_length=60):
        X, y = [], []
        for i in range(seq_length, len(data)):
            X.append(data[i-seq_length:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)
    
    X, y = create_sequences(prices_scaled)
    
    if len(X) < 30:
        print(f"⚠️ {model_name} için LSTM sekansı oluşturulamadı")
        return None
    
    # Train-test split
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    # LSTM model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Model eğitimi
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    
    model.fit(
        X_train, y_train,
        batch_size=32,
        epochs=50,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping],
        verbose=0
    )
    
    # Tahmin
    last_sequence = prices_scaled[-60:].reshape((1, 60, 1))
    
    # 30 günlük tahmin
    lstm_predictions = []
    current_sequence = last_sequence.copy()
    
    for _ in range(30):
        pred = model.predict(current_sequence, verbose=0)
        lstm_predictions.append(pred[0, 0])
        # Sequence'i güncelle
        current_sequence = np.roll(current_sequence, -1, axis=1)
        current_sequence[0, -1, 0] = pred[0, 0]
    
    # Denormalizasyon
    lstm_predictions = scaler.inverse_transform(np.array(lstm_predictions).reshape(-1, 1))
    
    lstm_ortalama = lstm_predictions.mean()
    mevcut_ortalama = daily_data['FIYAT'].iloc[-10:].mean()
    lstm_degisim = ((lstm_ortalama - mevcut_ortalama) / mevcut_ortalama * 100)
    
    print(f"🤖 {model_name} LSTM tahmini:")
    print(f"  📈 30 günlük ortalama: {lstm_ortalama:,.0f} TL")
    print(f"  🎯 Öngörülen değişim: {lstm_degisim:+.1f}%")
    
    # Model performansı
    test_pred = model.predict(X_test, verbose=0)
    test_pred = scaler.inverse_transform(test_pred)
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    mae = mean_absolute_error(y_test_actual, test_pred)
    print(f"  📊 Test MAE: {mae:.2f} TL")
    
    return {
        'model_name': model_name,
        'predictions': lstm_predictions.flatten(),
        'avg_prediction': lstm_ortalama,
        'change_percent': lstm_degisim,
        'mae': mae
    }

# LSTM modelleri eğit
lstm_sonuclari = {}
for model in ['iPhone 16', 'iPhone 15']:  # En popüler modeller için
    try:
        lstm_sonuclari[model] = create_lstm_model(model)
    except Exception as e:
        print(f"❌ {model} LSTM hatası: {e}")

# 5. ÜRÜN BAZLI RAPOR ÜRETİMİ
print(f"\n📋 Ürün Bazlı Tahmin Raporu")
print("=" * 80)

def generate_product_report(model_name):
    """Ürün bazlı detaylı rapor"""
    
    print(f"\n📱 {model_name} Detaylı Analiz Raporu")
    print("-" * 60)
    
    model_data = df[df['MODEL'] == model_name]
    if len(model_data) == 0:
        print(f"❌ {model_name} için veri bulunamadı")
        return
    
    # Mevcut durum
    son_fiyat = model_data.sort_values('TARIH')['FIYAT'].iloc[-1]
    ortalama_fiyat = model_data['FIYAT'].mean()
    volatilite = model_data['FIYAT'].std()
    
    print(f"💰 Mevcut Durum:")
    print(f"  Son fiyat: {son_fiyat:,.0f} TL")
    print(f"  Ortalama fiyat: {ortalama_fiyat:,.0f} TL")
    print(f"  Volatilite: ±{volatilite:,.0f} TL")
    
    # Teknik özellikler
    ozellikler = model_data.iloc[0]
    print(f"\n🔧 Teknik Özellikler:")
    print(f"  RAM: {ozellikler['RAM_GB']} GB")
    print(f"  Batarya: {ozellikler['BATARYA_MAH']} mAh")
    print(f"  Kamera: {ozellikler['KAMERA_MP']} MP")
    print(f"  Chipset: {ozellikler['CHIPSET']}")
    print(f"  DxOMark Puanı: {ozellikler['DXOMARK_PUAN']}")
    
    # Performans metrikleri
    perf_skoru = model_data['PERFORMANS_SKORU'].mean()
    fp_orani = model_data['FIYAT_PERFORMANS_ORANI'].mean()
    
    print(f"\n📊 Performans Metrikleri:")
    print(f"  Performans Skoru: {perf_skoru:.1f}")
    print(f"  Fiyat/Performans Oranı: {fp_orani:.1f}")
    
    # Pazar analizi
    kampanya_dagılım = model_data['KAMPANYA_DURUMU'].value_counts()
    print(f"\n🛍️ Pazar Analizi:")
    for durum, adet in kampanya_dagılım.head(3).items():
        print(f"  {durum}: {adet} kayıt (%{adet/len(model_data)*100:.1f})")
    
    # Tahmin özeti
    if model_name in model_tahminleri and model_tahminleri[model_name]:
        tahmin = model_tahminleri[model_name]
        print(f"\n🔮 Fiyat Tahminleri (30 gün):")
        if tahmin['arima_change'] != 0:
            print(f"  ARIMA: {tahmin['arima_change']:+.1f}% değişim")
        if tahmin['prophet_change'] != 0:
            print(f"  Prophet: {tahmin['prophet_change']:+.1f}% değişim")
    
    if model_name in lstm_sonuclari and lstm_sonuclari[model_name]:
        lstm = lstm_sonuclari[model_name]
        print(f"  LSTM: {lstm['change_percent']:+.1f}% değişim")
    
    # Öneri
    if model_name in model_tahminleri and model_tahminleri[model_name]:
        tahmin = model_tahminleri[model_name]
        ortalama_degisim = (tahmin.get('arima_change', 0) + tahmin.get('prophet_change', 0)) / 2
        
        print(f"\n💡 Öneriler:")
        if ortalama_degisim < -5:
            print(f"  🔴 Bu ürünün fiyatı önümüzdeki 1 ay içinde %{abs(ortalama_degisim):.1f} düşebilir")
            print(f"  💰 Satın alma için uygun dönem yaklaşıyor")
        elif ortalama_degisim > 5:
            print(f"  🔴 Bu ürünün fiyatı önümüzdeki 1 ay içinde %{ortalama_degisim:.1f} yükselebilir")
            print(f"  ⚡ Hemen satın alınması tavsiye edilir")
        else:
            print(f"  🟡 Fiyat değişimi minimal (%{ortalama_degisim:+.1f})")
            print(f"  📊 Stabil fiyat bekleniyor")

# Tüm modeller için rapor üret
for model in df['MODEL'].unique():
    generate_product_report(model)

# 6. VİZÜALİZASYON
print(f"\n📊 Görselleştirmeler oluşturuluyor...")

# İnteraktif Plotly grafikleri
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Fiyat Trendi', 'Anomali Tespiti', 'Performans vs Fiyat', 'Kampanya Analizi'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# 1. Fiyat trendi
for model in df['MODEL'].unique():
    model_data = df[df['MODEL'] == model].sort_values('TARIH')
    fig.add_trace(
        go.Scatter(x=model_data['TARIH'], y=model_data['FIYAT'], 
                  name=model, mode='lines'),
        row=1, col=1
    )

# Grafikleri kaydet
fig.write_html('profesyonel_telefon_analizi.html')

print(f"✅ Analiz tamamlandı!")
print(f"📊 İnteraktif grafik: profesyonel_telefon_analizi.html")
print(f"🔬 Tüm modeller için fiyat tahminleri oluşturuldu")
print(f"📋 Detaylı raporlar yazdırıldı")
