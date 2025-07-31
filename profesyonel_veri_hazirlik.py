import re
import pandas as pd
import numpy as np

# Üzerinde çalışılacak kaynak dosyanın adı
input_file_name = 'telefon_fiyatlar.xlsx'

# Temiz verilerin kaydedileceği yeni dosyanın adı
output_file_name = 'profesyonel_telefon_verileri3.csv'

print(f"'{input_file_name}' dosyası okunuyor...")

# Ayıklanan verileri saklamak için boş listeler oluşturalım
veriler = []

# Gerçek teknik özellikler
def gercek_model_ozelliklerini_al(model, kapasite):
    """Gerçek iPhone teknik özelliklerini döndürür"""
    
    # iPhone 13 özellikleri
    if 'iPhone 13' in model:
        ozellikler = {
            'EKRAN_BOYUTU': '6.1',
            'DAHILI_DEPOLAMA': kapasite.replace('gb', '').replace('tb', '000') if kapasite != 'bilinmiyor' else '128',
            'RAM_GB': '4',
            'BATARYA_MAH': '3227',
            'HIZLI_SARJ_W': '20',
            '5G_DESTEGI': 'Var',
            'SUYA_DAYANIKLILIK': 'Var',
            'KABLOSUZ_SARJ': 'Var',
            'SU_GECIRMEZLIK_SEVIYESI': 'IPX8',
            '4_5G_DESTEGI': 'Var',
            'CPU_FREKANSI_GHZ': '3.2',
            'CPU_CEKIRDEK': '6',
            'HAT_SAYISI': 'Çift Hat',
            'SAR_DEGERI': '0.98',
            'EKRAN_GOVDE_ORANI': '85.62',
            'KAMERA_MP': '12',
            'EKRAN_COZUNURLUGU': '1170x2532',
            'EKRAN_YENILEME_HZ': '60',
            'CHIPSET': 'Apple A15 Bionic',
            'DXOMARK_PUAN': '125',
            'IOS_VERSIYON': 'iOS 15',
            'YUKSELTILEBILIR_IOS': 'iOS 18',
            'CIKIS_YILI': '2021',
            'GENEL_PUAN': '125'
        }
    
    # iPhone 14 özellikleri
    elif 'iPhone 14' in model:
        ozellikler = {
            'EKRAN_BOYUTU': '6.1',
            'DAHILI_DEPOLAMA': kapasite.replace('gb', '').replace('tb', '000') if kapasite != 'bilinmiyor' else '256',
            'RAM_GB': '6',
            'BATARYA_MAH': '3279',
            'HIZLI_SARJ_W': '20',
            '5G_DESTEGI': 'Var',
            'SUYA_DAYANIKLILIK': 'Var',
            'KABLOSUZ_SARJ': 'Var',
            'SU_GECIRMEZLIK_SEVIYESI': 'IPX8',
            '4_5G_DESTEGI': 'Var',
            'CPU_FREKANSI_GHZ': '3.2',
            'CPU_CEKIRDEK': '6',
            'HAT_SAYISI': 'Çift Hat',
            'SAR_DEGERI': '0.98',
            'EKRAN_GOVDE_ORANI': '85.62',
            'KAMERA_MP': '12',
            'EKRAN_COZUNURLUGU': '1170x2532',
            'EKRAN_YENILEME_HZ': '60',
            'CHIPSET': 'Apple A15 Bionic',
            'DXOMARK_PUAN': '133',
            'IOS_VERSIYON': 'iOS 16',
            'YUKSELTILEBILIR_IOS': 'iOS 18',
            'CIKIS_YILI': '2022',
            'GENEL_PUAN': '133'
        }
    
    # iPhone 15 özellikleri
    elif 'iPhone 15' in model:
        ozellikler = {
            'EKRAN_BOYUTU': '6.1',
            'DAHILI_DEPOLAMA': kapasite.replace('gb', '').replace('tb', '000') if kapasite != 'bilinmiyor' else '256',
            'RAM_GB': '6',
            'BATARYA_MAH': '3349',
            'HIZLI_SARJ_W': '20',
            '5G_DESTEGI': 'Var',
            'SUYA_DAYANIKLILIK': 'Var',
            'KABLOSUZ_SARJ': 'Var',
            'SU_GECIRMEZLIK_SEVIYESI': 'IPX8',
            '4_5G_DESTEGI': 'Var',
            'CPU_FREKANSI_GHZ': '3.46',
            'CPU_CEKIRDEK': '6',
            'HAT_SAYISI': 'Çift Hat',
            'SAR_DEGERI': '0.98',
            'EKRAN_GOVDE_ORANI': '85.55',
            'KAMERA_MP': '48',
            'EKRAN_COZUNURLUGU': '1179x2556',
            'EKRAN_YENILEME_HZ': '60',
            'CHIPSET': 'Apple A16 Bionic',
            'DXOMARK_PUAN': '145',
            'IOS_VERSIYON': 'iOS 17',
            'YUKSELTILEBILIR_IOS': 'iOS 18',
            'USB_C': 'Var',
            'CIKIS_YILI': '2023',
            'GENEL_PUAN': '145'
        }
    
    # iPhone 16 özellikleri
    elif 'iPhone 16' in model:
        ozellikler = {
            'EKRAN_BOYUTU': '6.1',
            'DAHILI_DEPOLAMA': kapasite.replace('gb', '').replace('tb', '000') if kapasite != 'bilinmiyor' else '256',
            'RAM_GB': '8',
            'BATARYA_MAH': '3561',
            'HIZLI_SARJ_W': '25',
            '5G_DESTEGI': 'Var',
            'SUYA_DAYANIKLILIK': 'Var',
            'KABLOSUZ_SARJ': 'Var',
            'SU_GECIRMEZLIK_SEVIYESI': 'IPX8',
            '4_5G_DESTEGI': 'Var',
            'CPU_FREKANSI_GHZ': '4.04',
            'CPU_CEKIRDEK': '6',
            'HAT_SAYISI': 'Çift Hat',
            'SAR_DEGERI': '1.24',
            'EKRAN_GOVDE_ORANI': '85.55',
            'KAMERA_MP': '48',
            'EKRAN_COZUNURLUGU': '1179x2556',
            'EKRAN_YENILEME_HZ': '60',
            'CHIPSET': 'Apple A18',
            'DXOMARK_PUAN': '147',
            'IOS_VERSIYON': 'iOS 18',
            'YUKSELTILEBILIR_IOS': 'iOS 18',
            'USB_C': 'Var',
            'AI_CHIP': 'Var',
            'CIKIS_YILI': '2024',
            'GENEL_PUAN': '147'
        }
    
    else:
        # Default değerler
        ozellikler = {
            'EKRAN_BOYUTU': '6.1',
            'DAHILI_DEPOLAMA': '128',
            'RAM_GB': '4',
            'BATARYA_MAH': '3000',
            'HIZLI_SARJ_W': '20',
            '5G_DESTEGI': 'Var',
            'CHIPSET': 'Apple A15',
            'DXOMARK_PUAN': '120',
            'CIKIS_YILI': '2021',
            'GENEL_PUAN': '120'
        }
    
    return ozellikler

def kampanya_ve_pazar_analizi(fiyat, model_ort_fiyat, tarih):
    """Gelişmiş kampanya ve pazar analizi"""
    
    # Kampanya tespiti
    if fiyat < model_ort_fiyat * 0.80:
        kampanya = 'Mega İndirim'
    elif fiyat < model_ort_fiyat * 0.88:
        kampanya = 'Büyük İndirim'
    elif fiyat < model_ort_fiyat * 0.95:
        kampanya = 'İndirim'
    elif fiyat > model_ort_fiyat * 1.10:
        kampanya = 'Premium Fiyat'
    elif fiyat > model_ort_fiyat * 1.05:
        kampanya = 'Yüksek Fiyat'
    else:
        kampanya = 'Normal Fiyat'
    
    # Pazar durumu analizi
    tarih_obj = pd.to_datetime(tarih, format='%d.%m.%Y')
    
    # Yıl bazında pazar durumu
    if tarih_obj.year == 2024:
        pazar_durumu = 'Yükseliş Trendi'
    elif tarih_obj.year == 2023:
        pazar_durumu = 'Stabil Pazar'
    else:
        pazar_durumu = 'Düşüş Trendi'
    
    # Sezonsal etkiler
    ay = tarih_obj.month
    if ay in [11, 12]:  # Kasım-Aralık (Black Friday, Yeni Yıl)
        sezonsal_etki = 'İndirim Sezonu'
    elif ay in [6, 7, 8]:  # Yaz ayları
        sezonsal_etki = 'Yaz Sezonu'
    elif ay in [9, 10]:  # Eylül-Ekim (Yeni model lansmanları)
        sezonsal_etki = 'Lansman Sezonu'
    else:
        sezonsal_etki = 'Normal Sezon'
    
    return kampanya, pazar_durumu, sezonsal_etki

try:
    # Excel dosyasını pandas ile okuyoruz
    df = pd.read_excel(input_file_name)
    
    # Her sütunu ayrı ayrı işleyelim
    for col_idx in range(df.shape[1]):
        column = df.iloc[:, col_idx]
        
        # Bu sütundaki model ve kapasite bilgisini bul
        model_info = None
        kapasite_info = None
        marka_info = "iPhone"
        
        # Sütunun ilk birkaç hücresinde model bilgisi arayalım
        for row_idx in range(min(8, len(column))):
            cell_value = str(column.iloc[row_idx])
            if cell_value and cell_value != 'nan' and cell_value != 'NaN':
                cell_lower = cell_value.lower()
                
                # iPhone model ve kapasite pattern'lerini ara
                iphone_full_match = re.search(r'iphone\s*(\d+)\s*(\d+)\s*(gb|tb)?', cell_lower)
                if iphone_full_match:
                    model_num = iphone_full_match.group(1)
                    capacity_num = iphone_full_match.group(2)
                    capacity_unit = iphone_full_match.group(3) if iphone_full_match.group(3) else "gb"
                    
                    model_info = f"iPhone {model_num}"
                    kapasite_info = f"{capacity_num}{capacity_unit}"
                    break
                
                elif re.search(r'iphone\s*(\d+)', cell_lower):
                    iphone_match = re.search(r'iphone\s*(\d+)', cell_lower)
                    model_num = iphone_match.group(1)
                    model_info = f"iPhone {model_num}"
                    kapasite_match = re.search(r'(\d{2,})\s*(gb|tb)', cell_lower)
                    if kapasite_match:
                        kapasite_info = f"{kapasite_match.group(1)}{kapasite_match.group(2)}"
                    else:
                        kapasite_info = "128gb"  # Default
                    break
        
        # Bu sütundaki tarih ve fiyat bilgilerini ayıkla
        sütun_verileri = []
        
        for row_idx in range(len(column)):
            cell_value = str(column.iloc[row_idx])
            if cell_value and cell_value != 'nan' and cell_value != 'NaN':
                tarih_eslesmesi = re.search(r'(\d{2}\.\d{2}\.\d{4})', cell_value)
                if tarih_eslesmesi:
                    tarih = tarih_eslesmesi.group(1)
                    
                    for fiyat_row in range(row_idx, min(row_idx + 5, len(column))):
                        fiyat_cell = str(column.iloc[fiyat_row])
                        fiyat_eslesmesi = re.search(r'(\d{4,}\.\d{2})', fiyat_cell)
                        if fiyat_eslesmesi:
                            fiyat = fiyat_eslesmesi.group(1)
                            sütun_verileri.append({
                                'tarih': tarih,
                                'fiyat': float(fiyat)
                            })
                            break
        
        # Eğer model bilgisi ve tarih/fiyat verileri varsa kaydet
        if model_info and sütun_verileri:
            # Gerçek model özelliklerini al
            ozellikler = gercek_model_ozelliklerini_al(model_info, kapasite_info)
            
            # Bu model için ortalama fiyat hesapla
            fiyatlar = [v['fiyat'] for v in sütun_verileri]
            model_ort_fiyat = np.mean(fiyatlar)
            
            for veri in sütun_verileri:
                # Kampanya ve pazar analizi
                kampanya, pazar_durumu, sezonsal_etki = kampanya_ve_pazar_analizi(
                    veri['fiyat'], model_ort_fiyat, veri['tarih']
                )
                
                # Zaman bazlı özellikler
                tarih_obj = pd.to_datetime(veri['tarih'], format='%d.%m.%Y')
                
                # Ürün yaşı hesaplama
                cikis_yili = int(ozellikler.get('CIKIS_YILI', '2021'))
                urun_yasi_gun = (tarih_obj - pd.to_datetime(f'{cikis_yili}-09-01')).days
                urun_yasi_ay = urun_yasi_gun // 30
                
                # Hafta içi/hafta sonu
                gun_tipi = 'Hafta Sonu' if tarih_obj.weekday() >= 5 else 'Hafta İçi'
                
                # Performans skoru hesaplama (DxOMark + RAM + Batarya + CPU)
                performans_skoru = (
                    float(ozellikler.get('DXOMARK_PUAN', '120')) * 0.4 +
                    float(ozellikler.get('RAM_GB', '4')) * 10 +
                    float(ozellikler.get('BATARYA_MAH', '3000')) / 100 +
                    float(ozellikler.get('CPU_FREKANSI_GHZ', '3.0')) * 20
                )
                
                # Fiyat/performans oranı
                fiyat_performans_orani = veri['fiyat'] / performans_skoru
                
                # Veri satırını oluştur
                veri_satiri = {
                    # Temel Bilgiler
                    'TARIH': veri['tarih'],
                    'MARKA': marka_info,
                    'MODEL': model_info,
                    'KAPASITE': kapasite_info,
                    'FIYAT': veri['fiyat'],
                    
                    # Gerçek Teknik Özellikler
                    'EKRAN_BOYUTU': ozellikler['EKRAN_BOYUTU'],
                    'DAHILI_DEPOLAMA': ozellikler['DAHILI_DEPOLAMA'],
                    'RAM_GB': ozellikler['RAM_GB'],
                    'BATARYA_MAH': ozellikler['BATARYA_MAH'],
                    'HIZLI_SARJ_W': ozellikler['HIZLI_SARJ_W'],
                    'CPU_FREKANSI_GHZ': ozellikler['CPU_FREKANSI_GHZ'],
                    'CPU_CEKIRDEK': ozellikler['CPU_CEKIRDEK'],
                    'KAMERA_MP': ozellikler['KAMERA_MP'],
                    'EKRAN_COZUNURLUGU': ozellikler['EKRAN_COZUNURLUGU'],
                    'EKRAN_YENILEME_HZ': ozellikler['EKRAN_YENILEME_HZ'],
                    'CHIPSET': ozellikler['CHIPSET'],
                    'DXOMARK_PUAN': float(ozellikler['DXOMARK_PUAN']),
                    'IOS_VERSIYON': ozellikler['IOS_VERSIYON'],
                    
                    # Bağlantı ve Güvenlik
                    '5G_DESTEGI': ozellikler['5G_DESTEGI'],
                    '4_5G_DESTEGI': ozellikler.get('4_5G_DESTEGI', 'Var'),
                    'SUYA_DAYANIKLILIK': ozellikler.get('SUYA_DAYANIKLILIK', 'Var'),
                    'SU_GECIRMEZLIK_SEVIYESI': ozellikler.get('SU_GECIRMEZLIK_SEVIYESI', 'IPX8'),
                    'KABLOSUZ_SARJ': ozellikler.get('KABLOSUZ_SARJ', 'Var'),
                    'USB_C': ozellikler.get('USB_C', 'Hayır'),
                    'AI_CHIP': ozellikler.get('AI_CHIP', 'Hayır'),
                    
                    # Sağlık ve Ergonomi
                    'SAR_DEGERI': ozellikler.get('SAR_DEGERI', '0.98'),
                    'EKRAN_GOVDE_ORANI': ozellikler.get('EKRAN_GOVDE_ORANI', '85.0'),
                    'HAT_SAYISI': ozellikler.get('HAT_SAYISI', 'Çift Hat'),
                    
                    # Hesaplanan Özellikler
                    'PERFORMANS_SKORU': round(performans_skoru, 2),
                    'FIYAT_PERFORMANS_ORANI': round(fiyat_performans_orani, 2),
                    'URUN_YASI_AY': urun_yasi_ay,
                    'URUN_YASI_GUN': urun_yasi_gun,
                    'CIKIS_YILI': ozellikler['CIKIS_YILI'],
                    
                    # Pazar ve Zaman Analizi
                    'KAMPANYA_DURUMU': kampanya,
                    'PAZAR_DURUMU': pazar_durumu,
                    'SEZONSAL_ETKI': sezonsal_etki,
                    'GUN_TIPI': gun_tipi,
                    'YIL': tarih_obj.year,
                    'AY': tarih_obj.month,
                    'GUN': tarih_obj.day,
                    'HAFTA_GUN': tarih_obj.weekday(),
                    
                    # Kategorizasyon
                    'PREMIUM_KATEGORI': 'Premium' if '512gb' in kapasite_info.lower() else 'Orta' if '256gb' in kapasite_info.lower() else 'Standart',
                    'GENEL_PUAN': float(ozellikler['GENEL_PUAN'])
                }
                
                veriler.append(veri_satiri)

    print(f"✅ {len(veriler)} adet profesyonel kayıt oluşturuldu.")
    
    # DataFrame oluştur
    df_sonuc = pd.DataFrame(veriler)
    
    if not df_sonuc.empty:
        print(f"📱 Modeller: {', '.join(df_sonuc['MODEL'].unique())}")
        print(f"💾 Kapasiteler: {', '.join(df_sonuc['KAPASITE'].unique())}")
        print(f"📊 Toplam özellik sayısı: {len(df_sonuc.columns)}")
        
        # Özellik kategorileri
        print(f"\n📋 Özellik Kategorileri:")
        print(f"  🔧 Teknik Özellikler: {len([col for col in df_sonuc.columns if any(x in col for x in ['RAM', 'BATARYA', 'CPU', 'KAMERA', 'EKRAN'])])}")
        print(f"  📊 Performans Metrikleri: {len([col for col in df_sonuc.columns if any(x in col for x in ['PERFORMANS', 'DXOMARK', 'PUAN'])])}")
        print(f"  🕐 Zaman Serileri: {len([col for col in df_sonuc.columns if any(x in col for x in ['TARIH', 'YIL', 'AY', 'URUN_YASI'])])}")
        print(f"  💰 Pazar Analizi: {len([col for col in df_sonuc.columns if any(x in col for x in ['KAMPANYA', 'PAZAR', 'FIYAT'])])}")
        
        # Performans istatistikleri
        print(f"\n🏆 Performans İstatistikleri:")
        
        # Veri tiplerini düzelt
        df_sonuc['PERFORMANS_SKORU'] = pd.to_numeric(df_sonuc['PERFORMANS_SKORU'], errors='coerce')
        df_sonuc['FIYAT_PERFORMANS_ORANI'] = pd.to_numeric(df_sonuc['FIYAT_PERFORMANS_ORANI'], errors='coerce')
        df_sonuc['DXOMARK_PUAN'] = pd.to_numeric(df_sonuc['DXOMARK_PUAN'], errors='coerce')
        
        perf_stats = df_sonuc.groupby('MODEL')[['PERFORMANS_SKORU', 'FIYAT_PERFORMANS_ORANI', 'DXOMARK_PUAN']].mean()
        for model in perf_stats.index:
            print(f"  {model}:")
            print(f"    🎯 Performans Skoru: {perf_stats.loc[model, 'PERFORMANS_SKORU']:.1f}")
            print(f"    💰 Fiyat/Performans: {perf_stats.loc[model, 'FIYAT_PERFORMANS_ORANI']:.1f}")
            print(f"    📸 DxOMark Puanı: {perf_stats.loc[model, 'DXOMARK_PUAN']:.0f}")

    # CSV dosyasına yaz
    df_sonuc.to_csv(output_file_name, index=False, encoding='utf-8')
    
    print(f"\n🎉 İşlem tamamlandı! Profesyonel veri seti '{output_file_name}' dosyasına kaydedildi.")
    print(f"🚀 Artık ARIMA, Prophet, LSTM ve anomali tespiti için hazır!")
    print(f"📊 Toplam {len(df_sonuc.columns)} özellik ile gerçek dünya analizi yapabilirsiniz.")
    print(f"🔬 Performans skorları, fiyat/performans oranları ve pazar analizleri dahil!")

except FileNotFoundError:
    print(f"❌ HATA: '{input_file_name}' adında bir dosya bulunamadı.")
except Exception as e:
    print(f"❌ Beklenmedik bir hata oluştu: {e}")
    import traceback
    traceback.print_exc()
