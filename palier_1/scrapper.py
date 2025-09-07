import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.mandelboim.com/wp-json/wc/store/v1/products"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Accept": "application/json"
} #faire genre c qqun qui appuye 

all_products = []
page = 1

while True:
    url = f"{BASE_URL}?per_page=100&page={page}"
    r = requests.get(url, headers=HEADERS)
    
    if r.status_code != 200:
        print("Stop, erreur API :", r.status_code) # pas d erreur 403 grace au headers 
        break
    
    products = r.json()
    if not products:
        break  
    
    for p in products:
        
        desc_html = p.get("short_description", "")
        desc_text = BeautifulSoup(desc_html, "html.parser").get_text(strip=True)

        
        prices = p.get("prices", {})
        price = prices.get("price") or prices.get("regular_price") or prices.get("sale_price") or "N/A"

        
        title = p.get("name", "")
        match = re.search(r"\d+\*\d+", title) #chercher la taille dans le titre
        sizes = match.group() if match else "N/A"

        
        categories = [c.get("name", "") for c in p.get("categories", [])]
        category_he = categories[0] if categories else "N/A"

        all_products.append({
            "title_he": title,
            "url": p.get("permalink", ""),
            "price": price,
            "sizes": sizes,
            "description_he": desc_text,
            "image_url": p.get("images", [{}])[0].get("src", ""),
            "category_he": category_he
        })
    
    print(f" Page {page} : {len(products)} produits récupérés")
    page += 1


df = pd.DataFrame(all_products)
df.to_csv("catalogue_complet.csv", index=False, encoding="utf-8-sig")

print(f" Catalogue complet sauvegardé avec {len(all_products)} produits")
