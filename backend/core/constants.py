import os

PAGE_SIZE = 6
MAX_LENGTH = 256
MAX_DISPLAY_LENGTH = 50
MAX_NAME_LENGTH = 150
MAX_EMAIL_LENGTH = 254
CHARACTERS = 'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz234567890'
URL_LENGTH = 3
DOMAIN = f'http://{os.getenv("ALLOWED_HOSTS")}/'
