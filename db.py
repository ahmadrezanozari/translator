import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.setup()

    def setup(self):
        # ایجاد جداول تنظیمات و ترجمه‌ها
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src_language TEXT NOT NULL,
            dest_language TEXT NOT NULL,
            original_text TEXT NOT NULL,
            translated_text TEXT NOT NULL
        )
        ''')
        self.connection.commit()

    def save_setting(self, key, value):
        # ذخیره یا به‌روزرسانی تنظیمات
        self.cursor.execute('''
        INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
        self.connection.commit()

    def get_setting(self, key):
        # بازیابی تنظیمات
        self.cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_translation(self, src_language, dest_language, original_text, translated_text):
        # ذخیره ترجمه‌ها در دیتابیس
        self.cursor.execute('''
        INSERT INTO translations (src_language, dest_language, original_text, translated_text)
        VALUES (?, ?, ?, ?)
        ''', (src_language, dest_language, original_text, translated_text))
        self.connection.commit()

    def close(self):
        # بستن اتصال به دیتابیس
        self.connection.close()
