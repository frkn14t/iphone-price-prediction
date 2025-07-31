#!/usr/bin/env python3
"""
iPhone Fiyat Veri Toplama Sistemi
Web Scraping ile E-ticaret Sitelerinden Otomatik Veri Çekme

Bu script çeşitli e-ticaret sitelerinden iPhone fiyat verilerini otomatik olarak çeker.
NOT: Bu kod proje kapsamında geliştirilmiş ancak etik ve yasal sebeplerden dolayı 
manuel veri toplama yöntemi tercih edilmiştir.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web_scraping.log'),
        logging.StreamHandler()
    ]
)

class iPhonePriceScraper:
    """iPhone fiyat verilerini web'den çeken ana sınıf"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # iPhone modelleri ve kapasiteleri
        self.iphone_models = {
            'iPhone 16': ['128GB', '256GB', '512GB', '1TB'],
            'iPhone 15': ['128GB', '256GB', '512GB', '1TB'], 
            'iPhone 14': ['128GB', '256GB', '512GB', '1TB'],
            'iPhone 13': ['128GB', '256GB', '512GB', '1TB']
        }
        
        # E-ticaret siteleri (örnek URL'ler - gerçek implementasyon için güncellenebilir)
        self.websites = {
            'hepsiburada': {
                'base_url': 'https://www.hepsiburada.com',
                'search_pattern': '/ara?q=iphone+{model}+{capacity}',
                'price_selector': '.price-value',
                'title_selector': '.product-title',
                'link_selector': '.product-item a'
            },
            'trendyol': {
                'base_url': 'https://www.trendyol.com',
                'search_pattern': '/sr?q=iphone+{model}+{capacity}',
                'price_selector': '.prc-box-dscntd',
                'title_selector': '.p-card-wrppr .name',
                'link_selector': '.p-card-wrppr a'
            },
            'n11': {
                'base_url': 'https://www.n11.com',
                'search_pattern': '/arama?q=iphone+{model}+{capacity}',
                'price_selector': '.productPrice .newPrice',
                'title_selector': '.productName',
                'link_selector': '.product a'
            },
            'amazon_tr': {
                'base_url': 'https://www.amazon.com.tr',
                'search_pattern': '/s?k=iphone+{model}+{capacity}',
                'price_selector': '.a-price-whole',
                'title_selector': '[data-component-type="s-search-result"] h2 a span',
                'link_selector': '[data-component-type="s-search-result"] h2 a'
            }
        }
        
        self.collected_data = []
        
    def setup_selenium_driver(self):
        """Selenium WebDriver kurulumu (JavaScript gereken siteler için)"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Tarayıcı penceresiz çalışır
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            logging.error(f"Selenium driver kurulumu başarısız: {e}")
            return None
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Bot tespitini önlemek için rastgele bekleme"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def clean_price(self, price_text):
        """Fiyat metnini temizleyip numerik değere çevirir"""
        if not price_text:
            return None
            
        # Türkçe karakterleri ve gereksiz metinleri temizle
        price_text = re.sub(r'[^\d,.]', '', price_text)
        price_text = price_text.replace(',', '.')
        
        try:
            # Fiyatı float'a çevir
            price = float(price_text)
            return price
        except (ValueError, TypeError):
            return None
    
    def scrape_hepsiburada(self, model, capacity):
        """Hepsiburada'dan iPhone fiyatlarını çeker"""
        try:
            search_query = f"iphone {model.replace('iPhone ', '')} {capacity}"
            url = f"https://www.hepsiburada.com/ara?q={search_query.replace(' ', '+')}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ürün kartlarını bul
            products = soup.find_all('div', class_='productListContent-item')
            
            for product in products[:5]:  # İlk 5 sonuç
                try:
                    # Ürün başlığı
                    title_elem = product.find('h3', class_='product-title')
                    title = title_elem.get_text(strip=True) if title_elem else "Bilinmeyen"
                    
                    # Fiyat
                    price_elem = product.find('div', class_='price-value')
                    price_text = price_elem.get_text(strip=True) if price_elem else None
                    price = self.clean_price(price_text)
                    
                    if price and model.lower() in title.lower() and capacity.lower() in title.lower():
                        self.collected_data.append({
                            'tarih': datetime.now().strftime('%d.%m.%Y'),
                            'site': 'Hepsiburada',
                            'model': model,
                            'kapasite': capacity,
                            'fiyat': price,
                            'baslik': title,
                            'url': url
                        })
                        logging.info(f"Hepsiburada'dan veri çekildi: {model} {capacity} - {price} TL")
                
                except Exception as e:
                    logging.warning(f"Hepsiburada ürün işleme hatası: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Hepsiburada scraping hatası: {e}")
    
    def scrape_trendyol(self, model, capacity):
        """Trendyol'dan iPhone fiyatlarını çeker"""
        try:
            search_query = f"iphone {model.replace('iPhone ', '')} {capacity}"
            url = f"https://www.trendyol.com/sr?q={search_query.replace(' ', '%20')}"
            
            # Trendyol için özel header'lar
            headers = self.session.headers.copy()
            headers.update({
                'Referer': 'https://www.trendyol.com/',
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ürün kartlarını bul
            products = soup.find_all('div', class_='p-card-wrppr')
            
            for product in products[:5]:  # İlk 5 sonuç
                try:
                    # Ürün başlığı
                    title_elem = product.find('span', class_='prdct-desc-cntnr-name')
                    title = title_elem.get_text(strip=True) if title_elem else "Bilinmeyen"
                    
                    # Fiyat
                    price_elem = product.find('div', class_='prc-box-dscntd')
                    if not price_elem:
                        price_elem = product.find('div', class_='prc-box-orgnl')
                    
                    price_text = price_elem.get_text(strip=True) if price_elem else None
                    price = self.clean_price(price_text)
                    
                    if price and model.lower() in title.lower() and capacity.lower() in title.lower():
                        self.collected_data.append({
                            'tarih': datetime.now().strftime('%d.%m.%Y'),
                            'site': 'Trendyol',
                            'model': model,
                            'kapasite': capacity,
                            'fiyat': price,
                            'baslik': title,
                            'url': url
                        })
                        logging.info(f"Trendyol'dan veri çekildi: {model} {capacity} - {price} TL")
                
                except Exception as e:
                    logging.warning(f"Trendyol ürün işleme hatası: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Trendyol scraping hatası: {e}")
    
    def scrape_with_selenium(self, model, capacity, site_config):
        """Selenium ile JavaScript gereken siteleri çizer"""
        driver = self.setup_selenium_driver()
        if not driver:
            return
            
        try:
            search_query = f"iphone {model.replace('iPhone ', '')} {capacity}"
            url = site_config['base_url'] + site_config['search_pattern'].format(
                model=model.replace('iPhone ', '').replace(' ', '+'),
                capacity=capacity.replace(' ', '+')
            )
            
            driver.get(url)
            self.random_delay(2, 4)
            
            # Sayfanın yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, site_config['price_selector']))
            )
            
            # Ürünleri bul
            price_elements = driver.find_elements(By.CSS_SELECTOR, site_config['price_selector'])
            title_elements = driver.find_elements(By.CSS_SELECTOR, site_config['title_selector'])
            
            for i, (price_elem, title_elem) in enumerate(zip(price_elements[:5], title_elements[:5])):
                try:
                    title = title_elem.text.strip()
                    price_text = price_elem.text.strip()
                    price = self.clean_price(price_text)
                    
                    if price and model.lower() in title.lower() and capacity.lower() in title.lower():
                        self.collected_data.append({
                            'tarih': datetime.now().strftime('%d.%m.%Y'),
                            'site': site_config['base_url'].split('//')[1].split('.')[1].title(),
                            'model': model,
                            'kapasite': capacity,
                            'fiyat': price,
                            'baslik': title,
                            'url': url
                        })
                        logging.info(f"Selenium ile veri çekildi: {model} {capacity} - {price} TL")
                
                except Exception as e:
                    logging.warning(f"Selenium ürün işleme hatası: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Selenium scraping hatası: {e}")
        finally:
            driver.quit()
    
    def scrape_all_sites(self):
        """Tüm sitelerden veri çekme işlemini koordine eder"""
        logging.info("iPhone fiyat verisi çekme işlemi başlatıldı...")
        
        total_products = sum(len(capacities) for capacities in self.iphone_models.values())
        current_progress = 0
        
        for model, capacities in self.iphone_models.items():
            for capacity in capacities:
                logging.info(f"İşleniyor: {model} {capacity}")
                
                # Hepsiburada
                self.scrape_hepsiburada(model, capacity)
                self.random_delay(2, 4)
                
                # Trendyol
                self.scrape_trendyol(model, capacity)
                self.random_delay(2, 4)
                
                # Diğer siteler için Selenium (isteğe bağlı)
                # self.scrape_with_selenium(model, capacity, self.websites['n11'])
                
                current_progress += 1
                progress_percent = (current_progress / total_products) * 100
                logging.info(f"İlerleme: %{progress_percent:.1f} tamamlandı")
        
        logging.info(f"Veri çekme işlemi tamamlandı. Toplam {len(self.collected_data)} kayıt toplandı.")
    
    def save_to_excel(self, filename='scraped_iphone_data.xlsx'):
        """Çekilen verileri Excel dosyasına kaydeder"""
        if not self.collected_data:
            logging.warning("Kaydedilecek veri bulunamadı!")
            return
        
        df = pd.DataFrame(self.collected_data)
        
        # Veri temizleme ve düzenleme
        df['tarih'] = pd.to_datetime(df['tarih'], format='%d.%m.%Y')
        df['fiyat'] = pd.to_numeric(df['fiyat'], errors='coerce')
        df = df.dropna(subset=['fiyat'])
        df = df.sort_values(['model', 'kapasite', 'fiyat'])
        
        # Excel'e kaydet
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='iPhone Fiyatları', index=False)
            
            # Özet sayfa
            summary = df.groupby(['model', 'kapasite']).agg({
                'fiyat': ['count', 'mean', 'min', 'max', 'std']
            }).round(2)
            summary.to_excel(writer, sheet_name='Özet')
        
        logging.info(f"Veriler {filename} dosyasına kaydedildi.")
        return filename
    
    def generate_historical_data(self, days_back=365):
        """Geçmiş tarihler için simüle edilmiş veri üretir"""
        logging.info(f"Son {days_back} gün için tarihsel veri simülasyonu...")
        
        base_prices = {
            'iPhone 16': {'128GB': 65000, '256GB': 70000, '512GB': 80000, '1TB': 90000},
            'iPhone 15': {'128GB': 55000, '256GB': 60000, '512GB': 70000, '1TB': 80000},
            'iPhone 14': {'128GB': 45000, '256GB': 50000, '512GB': 60000, '1TB': 70000},
            'iPhone 13': {'128GB': 35000, '256GB': 40000, '512GB': 50000, '1TB': 60000}
        }
        
        for days_ago in range(days_back):
            date = datetime.now() - timedelta(days=days_ago)
            
            # Haftanın her günü için veri üretme
            if random.random() < 0.3:  # %30 olasılıkla veri üret
                continue
                
            for model in self.iphone_models:
                for capacity in self.iphone_models[model]:
                    if random.random() < 0.15:  # %15 olasılıkla bu ürün için veri üret
                        continue
                    
                    base_price = base_prices[model][capacity]
                    
                    # Fiyat değişim simülasyonu
                    # Trend: Yeni modeller daha pahalı, eskiler zamanla düşer
                    days_since_launch = days_ago
                    if model == 'iPhone 16':
                        days_since_launch += 30  # Yeni model
                    elif model == 'iPhone 15':
                        days_since_launch += 365
                    elif model == 'iPhone 14':
                        days_since_launch += 730
                    else:  # iPhone 13
                        days_since_launch += 1095
                    
                    # Zamanla fiyat düşüş trendi
                    trend_factor = 1 - (days_since_launch * 0.00005)
                    
                    # Rastgele dalgalanma
                    random_factor = random.uniform(0.85, 1.15)
                    
                    # Kampanya dönemleri
                    campaign_factor = 1.0
                    if date.month == 11:  # Kasım (Black Friday)
                        campaign_factor = random.uniform(0.7, 0.9)
                    elif date.month == 12:  # Aralık (Yılbaşı)
                        campaign_factor = random.uniform(0.8, 0.95)
                    elif date.month in [6, 7, 8]:  # Yaz dönememi
                        campaign_factor = random.uniform(0.9, 1.1)
                    
                    final_price = base_price * trend_factor * random_factor * campaign_factor
                    final_price = round(final_price, -2)  # 100'lük yuvarla
                    
                    # Rastgele site seç
                    site = random.choice(['Hepsiburada', 'Trendyol', 'N11', 'Amazon TR'])
                    
                    self.collected_data.append({
                        'tarih': date.strftime('%d.%m.%Y'),
                        'site': site,
                        'model': model,
                        'kapasite': capacity,
                        'fiyat': final_price,
                        'baslik': f"{model} {capacity} Cep Telefonu",
                        'url': f"https://example.com/search?q={model}+{capacity}"
                    })
        
        logging.info(f"Tarihsel veri simülasyonu tamamlandı. {len(self.collected_data)} kayıt oluşturuldu.")

def main():
    """Ana çalıştırma fonksiyonu"""
    scraper = iPhonePriceScraper()
    
    print("🚀 iPhone Fiyat Veri Toplama Sistemi")
    print("=" * 50)
    print("NOT: Bu sistem etik web scraping prensipleri çerçevesinde geliştirilmiştir.")
    print("     Gerçek kullanımda site kullanım şartlarına uygun olarak kullanılmalıdır.")
    print()
    
    choice = input("Çalıştırma seçeneği:\n1. Canlı veri çekme (Gerçek siteler)\n2. Simülasyon (Test verisi)\n3. Çıkış\nSeçiminiz (1-3): ")
    
    if choice == '1':
        print("\n⚠️  UYARI: Canlı veri çekme işlemi başlatılıyor...")
        print("Bu işlem site yükünü artırabilir ve yasal sorumluluk doğurabilir.")
        confirm = input("Devam etmek istediğinizden emin misiniz? (y/N): ")
        
        if confirm.lower() == 'y':
            scraper.scrape_all_sites()
            filename = scraper.save_to_excel('canlı_iphone_verileri.xlsx')
            print(f"\n✅ Canlı veriler {filename} dosyasına kaydedildi.")
        else:
            print("❌ Canlı veri çekme işlemi iptal edildi.")
    
    elif choice == '2':
        print("\n🔄 Simülasyon verisi oluşturuluyor...")
        scraper.generate_historical_data(days_back=365)
        filename = scraper.save_to_excel('simulasyon_iphone_verileri.xlsx')
        print(f"\n✅ Simülasyon verileri {filename} dosyasına kaydedildi.")
        print(f"📊 Toplam {len(scraper.collected_data)} kayıt oluşturuldu.")
        
        # Özet istatistikler
        df = pd.DataFrame(scraper.collected_data)
        print(f"\n📈 Veri Özeti:")
        print(f"📅 Tarih aralığı: {df['tarih'].min()} - {df['tarih'].max()}")
        print(f"💰 Fiyat aralığı: {df['fiyat'].min():,.0f} - {df['fiyat'].max():,.0f} TL")
        print(f"📱 Model dağılımı:")
        for model, count in df['model'].value_counts().items():
            print(f"   {model}: {count} kayıt")
    
    elif choice == '3':
        print("👋 Çıkış yapılıyor...")
    
    else:
        print("❌ Geçersiz seçenek!")

if __name__ == "__main__":
    main()
