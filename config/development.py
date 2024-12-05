import os
import logging

LOG_LEVEL = logging.DEBUG
PRESERVE_CONTEXT_ON_EXCEPTION = True
DEBUG = False

SESSION_COOKIE_SAMESITE = 'strict'
SESSION_COOKIE_PATH = '/'
SESSION_KEY_PREFIX = "hello"
SESSION_COOKIE_NAME = "DSQuestSession"


ROOT_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..'))
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
TEMP_DIR = os.path.join(ROOT_DIR, 'portal')
QRDATA = os.path.join(ROOT_DIR, "qrdata")
COURSEIMAGES= os.path.join(ROOT_DIR, "course_images")

DIRECTORIES = [LOG_DIR, TEMP_DIR,QRDATA,COURSEIMAGES]
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', '7z'}
SECRET_KEY = "Gc5c3zTk'-3<&BdL:P92O{_(:-NkY+"
RECAPTCHA_SECRET_KEY = "6Lf6jocqAAAAAKSbGtve7kGAQ2vW3Sj57uf06DBR"
GOOGLECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

PROPAGATE_EXCEPTIONS = True

CORS_HEADERS = [
    'Content-Type',
    'Authorization'
]

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:5000",
    "https://127.0.0.1:5000",
    "http://127.0.0.1:4200",
    "https://127.0.0.1:4200",
    "http://localhost",
    "https://localhost",
    "http://localhost:5000",
    "https://localhost:5000",
    "http://localhost:4200",
    "https://localhost:4200",
]
