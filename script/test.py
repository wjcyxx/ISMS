import sys
import os
import django
import time


BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISMS.settings')
django.setup()


if __name__ == "__main__":
    i = 0
    while True:
        i += 1
        print(i)
        time.sleep(5)
        print(os.getpid())