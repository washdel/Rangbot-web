"""
Konfigurasi MySQL untuk RangBot Web
Sesuaikan dengan kredensial MySQL Laragon Anda
"""

# Konfigurasi MySQL Laragon (default)
MYSQL_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'rangbot_db',  # Nama database
    'USER': 'root',  # Username MySQL (default Laragon: root)
    'PASSWORD': '',  # Password MySQL (default Laragon: kosong)
    'HOST': 'localhost',  # Host MySQL
    'PORT': '3306',  # Port MySQL (default: 3306)
    'OPTIONS': {
        'charset': 'utf8mb4',
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    },
}

