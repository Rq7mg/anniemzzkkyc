# Authored By Certified Coders © 2025
import os
from typing import List
import yaml

# Dil depoları
languages = {}
languages_present = {}

def get_string(lang: str):
    # Bot her zaman 'en' istese bile biz ona Türkçe olanı vereceğiz la!
    return languages["en"]

# Sadece ana dil dosyasını (en.yml) yüklüyoruz
# Çünkü en.yml dosyasını senin için Angara şivesiyle doldurduk.
if "en" not in languages:
    try:
        languages["en"] = yaml.safe_load(
            open(r"./strings/langs/en.yml", encoding="utf8")
        )
        # Dil listesinde sadece bu görünsün
        languages_present["en"] = languages["en"]["name"]
    except Exception as e:
        print(f"La dil dosyası yüklenemedi, mevzu var: {e}")
        exit()

# Diğer dilleri döngüye sokup yüklemiyoruz, botu Türkçeye mahkum ettik!
