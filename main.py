from googletrans import Translator
from gtts import gTTS
import os
from db import DatabaseManager  # کلاس مدیریت دیتابیس را وارد می‌کنیم

# ایجاد شیء مترجم
translator = Translator()
db = DatabaseManager("translator.db")  # اتصال به دیتابیس

# گرفتن زبان مبدا از دیتابیس یا ورودی کاربر
src_lang = db.get_setting("source_language")
if not src_lang:
    src_lang = input("زبان مبدا رو وارد کنید ('en' برای انگلیسی، 'fa' برای فارسی): ")
    db.save_setting("source_language", src_lang)

# گرفتن زبان مقصد از دیتابیس یا ورودی کاربر
dest_lang = db.get_setting("dest_language")
if not dest_lang:
    dest_lang = input("زبان مقصد رو وارد کنید ('en' برای انگلیسی، 'fa' برای فارسی): ")
    db.save_setting("dest_language", dest_lang)

# بررسی ورودی زبان‌ها
if (src_lang not in ['en', 'fa']) or (dest_lang not in ['en', 'fa']):
    print("لطفاً فقط زبان‌های 'en' یا 'fa' رو وارد کنید.")
else:
    # گرفتن متن برای ترجمه از کاربر
    word_to_translate = input("کلمه یا جمله‌ای که می‌خواهید ترجمه کنید رو وارد کنید: ")

    # ترجمه متن
    translated_word = translator.translate(word_to_translate, src=src_lang, dest=dest_lang)

    # نمایش ترجمه
    print(
        f"ترجمه '{word_to_translate}' از {'انگلیسی' if src_lang == 'en' else 'فارسی'} به {'انگلیسی' if dest_lang == 'en' else 'فارسی'}: {translated_word.text}")

    # ذخیره ترجمه در تاریخچه دیتابیس
    db.save_translation(src_lang, dest_lang, word_to_translate, translated_word.text)

    # تلفظ ترجمه
    tts = gTTS(text=translated_word.text, lang=dest_lang)
    tts.save("pronunciation.mp3")
    os.system("start pronunciation.mp3")  # برای پخش فایل صوتی در ویندوز

# بستن اتصال دیتابیس
db.close()
