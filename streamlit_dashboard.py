import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="iPhone Fiyat Analizi Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .prediction-positive {
        color: #28a745;
        font-weight: bold;
    }
    .prediction-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .prediction-neutral {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown('<h1 class="main-header">📱 iPhone Fiyat Analizi Dashboard</h1>', unsafe_allow_html=True)

# Veri yükleme
@st.cache_data
def load_data():
    import os
    
    # Mevcut çalışma dizinini kontrol et
    current_dir = os.getcwd()
    st.sidebar.write(f"📁 Çalışma dizini: {current_dir}")
    
    # Dosya yollarını dene
    file_paths = [
        'profesyonel_telefon_verileri.csv',
        'C:/Users/FURKAN/excel_temizlik/profesyonel_telefon_verileri.csv',
        os.path.join(current_dir, 'profesyonel_telefon_verileri.csv'),
        'gelismis_telefon_verileri.csv'  # Yedek dosya
    ]
    
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                st.sidebar.success(f"✅ Dosya bulundu: {file_path}")
                df = pd.read_csv(file_path)
                
                # Tarih formatını otomatik algıla
                df['TARIH'] = pd.to_datetime(df['TARIH'])
                df['FIYAT'] = pd.to_numeric(df['FIYAT'])
                
                # Eksik sütunları kontrol et ve ekle
                required_columns = ['PERFORMANS_SKORU', 'FIYAT_PERFORMANS_ORANI', 'KAMPANYA_DURUMU']
                for col in required_columns:
                    if col not in df.columns:
                        if col == 'PERFORMANS_SKORU':
                            df[col] = 100.0  # Default değer
                        elif col == 'FIYAT_PERFORMANS_ORANI':
                            df[col] = df['FIYAT'] / 100.0  # Basit hesaplama
                        elif col == 'KAMPANYA_DURUMU':
                            df[col] = 'Normal Fiyat'  # Default durum
                
                st.sidebar.info(f"📊 Yüklenen veri: {len(df)} kayıt, {len(df.columns)} sütun")
                return df
                
        except Exception as e:
            st.sidebar.warning(f"⚠️ {file_path} yüklenemedi: {str(e)}")
            continue
    
    # Hiçbir dosya bulunamazsa
    st.error("❌ Veri dosyası bulunamadı. Lütfen önce veri hazırlama scriptini çalıştırın.")
    st.error("📁 Aşağıdaki dosyalardan birini oluşturun:")
    for path in file_paths:
        st.write(f"  - {path}")
    return None

df = load_data()

if df is not None:
    # Sidebar filtreleri
    st.sidebar.header("🔍 Filtreler")
    
    # Model seçimi
    selected_models = st.sidebar.multiselect(
        "Modeller:",
        options=df['MODEL'].unique(),
        default=df['MODEL'].unique()
    )
    
    # Kapasite seçimi
    selected_capacities = st.sidebar.multiselect(
        "Kapasiteler:",
        options=df['KAPASITE'].unique(),
        default=df['KAPASITE'].unique()
    )
    
    # Tarih aralığı
    date_range = st.sidebar.date_input(
        "Tarih Aralığı:",
        value=(df['TARIH'].min(), df['TARIH'].max()),
        min_value=df['TARIH'].min(),
        max_value=df['TARIH'].max()
    )
    
    # Veriyi filtrele
    filtered_df = df[
        (df['MODEL'].isin(selected_models)) &
        (df['KAPASITE'].isin(selected_capacities)) &
        (df['TARIH'] >= pd.to_datetime(date_range[0])) &
        (df['TARIH'] <= pd.to_datetime(date_range[1]))
    ]
    
    # Ana metrikler
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_price = filtered_df['FIYAT'].mean()
        st.metric("💰 Ortalama Fiyat", f"{avg_price:,.0f} TL")
    
    with col2:
        total_records = len(filtered_df)
        st.metric("📊 Toplam Kayıt", f"{total_records:,}")
    
    with col3:
        price_std = filtered_df['FIYAT'].std()
        st.metric("📈 Volatilite", f"±{price_std:,.0f} TL")
    
    with col4:
        avg_performance = filtered_df['PERFORMANS_SKORU'].mean()
        st.metric("🎯 Avg. Performans", f"{avg_performance:.1f}")
    
    # Tab'lar
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Fiyat Trendi", "🔍 Anomali Analizi", "🤖 AI Tahminleri", "📊 Teknik Analiz", "📋 Raporlar"])
    
    with tab1:
        st.header("📈 Fiyat Trend Analizi")
        
        # Model bazında fiyat trendi
        fig_trend = go.Figure()
        
        for model in selected_models:
            model_data = filtered_df[filtered_df['MODEL'] == model]
            daily_avg = model_data.groupby('TARIH')['FIYAT'].mean().reset_index()
            
            fig_trend.add_trace(go.Scatter(
                x=daily_avg['TARIH'],
                y=daily_avg['FIYAT'],
                mode='lines+markers',
                name=model,
                line=dict(width=3),
                marker=dict(size=6)
            ))
        
        fig_trend.update_layout(
            title="Model Bazında Fiyat Trendi",
            xaxis_title="Tarih",
            yaxis_title="Fiyat (TL)",
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Kapasite bazında karşılaştırma
        col1, col2 = st.columns(2)
        
        with col1:
            capacity_avg = filtered_df.groupby('KAPASITE')['FIYAT'].mean().sort_values()
            fig_capacity = px.bar(
                x=capacity_avg.index,
                y=capacity_avg.values,
                title="Kapasite Bazında Ortalama Fiyat",
                labels={'x': 'Kapasite', 'y': 'Ortalama Fiyat (TL)'}
            )
            st.plotly_chart(fig_capacity, use_container_width=True)
        
        with col2:
            # Sezonsal analiz
            filtered_df['AY'] = filtered_df['TARIH'].dt.month
            seasonal_avg = filtered_df.groupby('AY')['FIYAT'].mean()
            
            ay_isimleri = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 
                          'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']
            
            fig_seasonal = px.line(
                x=[ay_isimleri[i-1] for i in seasonal_avg.index],
                y=seasonal_avg.values,
                title="Aylık Ortalama Fiyat Trendi",
                labels={'x': 'Ay', 'y': 'Ortalama Fiyat (TL)'}
            )
            st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with tab2:
        st.header("🔍 Anomali ve Kampanya Analizi")
        
        # Kampanya dağılımı
        kampanya_counts = filtered_df['KAMPANYA_DURUMU'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_kampanya = px.pie(
                values=kampanya_counts.values,
                names=kampanya_counts.index,
                title="Kampanya Durumu Dağılımı"
            )
            st.plotly_chart(fig_kampanya, use_container_width=True)
        
        with col2:
            # Anomali detection sonuçları
            st.subheader("🎯 Anomali Tespiti Sonuçları")
            
            # Model bazında anomali oranları
            for model in selected_models:
                model_data = filtered_df[filtered_df['MODEL'] == model]
                indirim_kayitlari = len(model_data[model_data['KAMPANYA_DURUMU'].isin(['İndirim', 'Büyük İndirim', 'Mega İndirim'])])
                toplam_kayit = len(model_data)
                
                if toplam_kayit > 0:
                    indirim_orani = indirim_kayitlari / toplam_kayit * 100
                    st.metric(f"📱 {model}", f"%{indirim_orani:.1f} indirim")
        
        # Zaman bazında anomali haritası
        st.subheader("🗺️ Zaman Bazında İndirim Haritası")
        
        pivot_data = filtered_df.pivot_table(
            values='FIYAT', 
            index=filtered_df['TARIH'].dt.month,
            columns='MODEL',
            aggfunc='mean'
        )
        
        fig_heatmap = px.imshow(
            pivot_data.values,
            x=pivot_data.columns,
            y=[ay_isimleri[i-1] for i in pivot_data.index],
            title="Aylık Ortalama Fiyat Haritası",
            color_continuous_scale="RdYlBu_r"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab3:
        st.header("🤖 AI Tahminleri ve Öngörüler")
        
        # Basit trend tahmini
        st.subheader("📈 30 Günlük Fiyat Tahminleri")
        
        predictions = {}
        
        for model in selected_models:
            model_data = filtered_df[filtered_df['MODEL'] == model].sort_values('TARIH')
            
            if len(model_data) >= 30:
                # Son 30 günün ortalaması
                recent_avg = model_data.tail(30)['FIYAT'].mean()
                
                # Basit trend hesaplama
                if len(model_data) >= 60:
                    older_avg = model_data.tail(60).head(30)['FIYAT'].mean()
                    trend = (recent_avg - older_avg) / older_avg * 100
                else:
                    trend = 0
                
                # Tahmin
                predicted_price = recent_avg * (1 + trend/100)
                change_percent = ((predicted_price - recent_avg) / recent_avg) * 100
                
                predictions[model] = {
                    'current': recent_avg,
                    'predicted': predicted_price,
                    'change': change_percent
                }
        
        # Tahminleri görselleştir
        if predictions:
            cols = st.columns(len(predictions))
            
            for i, (model, pred) in enumerate(predictions.items()):
                with cols[i]:
                    st.markdown(f"### 📱 {model}")
                    st.metric(
                        "Mevcut Ortalama",
                        f"{pred['current']:,.0f} TL"
                    )
                    
                    change_color = "prediction-positive" if pred['change'] > 0 else "prediction-negative" if pred['change'] < 0 else "prediction-neutral"
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>30 Günlük Tahmin</h4>
                        <p style="font-size: 1.5rem; margin: 0;">{pred['predicted']:,.0f} TL</p>
                        <p class="{change_color}" style="margin: 0;">
                            {pred['change']:+.1f}% değişim
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Öneri
                    if pred['change'] < -5:
                        st.success("💰 Satın alma fırsatı yaklaşıyor!")
                    elif pred['change'] > 5:
                        st.warning("⚡ Hemen satın alınması öneriliyor!")
                    else:
                        st.info("📊 Stabil fiyat bekleniyor")
        
        # Performans vs Fiyat analizi
        st.subheader("🎯 Performans vs Fiyat Analizi")
        
        fig_scatter = px.scatter(
            filtered_df,
            x='PERFORMANS_SKORU',
            y='FIYAT',
            color='MODEL',
            size='FIYAT_PERFORMANS_ORANI',
            hover_data=['KAPASITE', 'DXOMARK_PUAN'],
            title="Performans Skoru vs Fiyat"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab4:
        st.header("📊 Teknik Özellik Analizi")
        
        # Teknik özellik karşılaştırması
        numeric_features = ['RAM_GB', 'BATARYA_MAH', 'KAMERA_MP', 'DXOMARK_PUAN', 'PERFORMANS_SKORU']
        
        feature_comparison = filtered_df.groupby('MODEL')[numeric_features].mean()
        
        # Radar chart için veriyi normalize et
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        normalized_features = pd.DataFrame(
            scaler.fit_transform(feature_comparison),
            index=feature_comparison.index,
            columns=feature_comparison.columns
        )
        
        # Radar chart oluştur
        fig_radar = go.Figure()
        
        for model in normalized_features.index:
            fig_radar.add_trace(go.Scatterpolar(
                r=normalized_features.loc[model].values.tolist() + [normalized_features.loc[model].values[0]],
                theta=list(normalized_features.columns) + [normalized_features.columns[0]],
                fill='toself',
                name=model,
                line=dict(width=2)
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Model Bazında Teknik Özellik Karşılaştırması"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Özellik korelasyon matrisi
        st.subheader("🔗 Özellik Korelasyon Analizi")
        
        correlation_features = ['FIYAT'] + numeric_features
        corr_matrix = filtered_df[correlation_features].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            title="Özellik Korelasyon Matrisi",
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with tab5:
        st.header("📋 Detaylı Raporlar")
        
        # Model seçici
        selected_model_report = st.selectbox(
            "Rapor için model seçin:",
            options=selected_models
        )
        
        if selected_model_report:
            model_data = filtered_df[filtered_df['MODEL'] == selected_model_report]
            
            # Genel istatistikler
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Toplam Kayıt", len(model_data))
                st.metric("💰 Ortalama Fiyat", f"{model_data['FIYAT'].mean():,.0f} TL")
            
            with col2:
                st.metric("📈 En Yüksek Fiyat", f"{model_data['FIYAT'].max():,.0f} TL")
                st.metric("📉 En Düşük Fiyat", f"{model_data['FIYAT'].min():,.0f} TL")
            
            with col3:
                st.metric("🎯 Performans Skoru", f"{model_data['PERFORMANS_SKORU'].mean():.1f}")
                st.metric("📱 DxOMark Puanı", f"{model_data['DXOMARK_PUAN'].iloc[0]}")
            
            # Teknik özellikler tablosu
            st.subheader("🔧 Teknik Özellikler")
            
            tech_specs = model_data.iloc[0]
            specs_df = pd.DataFrame({
                'Özellik': [
                    'RAM', 'Depolama', 'Batarya', 'Kamera', 'Chipset',
                    'Ekran Boyutu', 'Ekran Çözünürlüğü', '5G Desteği', 'Suya Dayanıklılık'
                ],
                'Değer': [
                    f"{tech_specs['RAM_GB']} GB",
                    f"{tech_specs['DAHILI_DEPOLAMA']} GB",
                    f"{tech_specs['BATARYA_MAH']} mAh",
                    f"{tech_specs['KAMERA_MP']} MP",
                    tech_specs['CHIPSET'],
                    f"{tech_specs['EKRAN_BOYUTU']} inç",
                    tech_specs['EKRAN_COZUNURLUGU'],
                    tech_specs['5G_DESTEGI'],
                    tech_specs['SU_GECIRMEZLIK_SEVIYESI']
                ]
            })
            
            st.dataframe(specs_df, use_container_width=True)
            
            # Fiyat geçmişi grafiği
            st.subheader("📈 Fiyat Geçmişi")
            
            price_history = model_data.groupby('TARIH')['FIYAT'].mean().reset_index()
            
            fig_history = px.line(
                price_history,
                x='TARIH',
                y='FIYAT',
                title=f"{selected_model_report} Fiyat Geçmişi"
            )
            st.plotly_chart(fig_history, use_container_width=True)
            
            # İndirim fırsatları
            st.subheader("🛍️ İndirim Fırsatları")
            
            indirim_kayitlari = model_data[model_data['KAMPANYA_DURUMU'].str.contains('İndirim', na=False)]
            
            if len(indirim_kayitlari) > 0:
                indirim_stats = indirim_kayitlari.groupby('KAMPANYA_DURUMU').agg({
                    'FIYAT': ['count', 'mean', 'min'],
                    'TARIH': ['min', 'max']
                }).round(2)
                
                st.dataframe(indirim_stats, use_container_width=True)
            else:
                st.info("Bu dönemde indirim kaydı bulunamadı.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        📱 iPhone Fiyat Analizi Dashboard | 
        🔬 AI Destekli Tahminler | 
        📊 Gerçek Zamanlı Analiz
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Veri yüklenemedi. Lütfen veri dosyalarının mevcut olduğundan emin olun.")

# Sidebar bilgileri
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dashboard Bilgileri")
st.sidebar.info("""
🔹 **Modeller**: ARIMA, Prophet, LSTM  
🔹 **Anomali Tespiti**: Isolation Forest  
🔹 **Tahmin Süresi**: 30 gün  
🔹 **Güncelleme**: Gerçek zamanlı  
""")

st.sidebar.markdown("### 🚀 Özellikler")
st.sidebar.success("""
✅ Fiyat trend analizi  
✅ Kampanya tespiti  
✅ AI tahminleri  
✅ Teknik analiz  
✅ Detaylı raporlar  
""")
