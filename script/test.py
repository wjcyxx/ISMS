import sys
import os
import django


BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISMS.settings')
django.setup()


if __name__ == "__main__":

    print(BASE_DIR)