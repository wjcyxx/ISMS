import sys
import os
import django
from django.shortcuts import HttpResponse
import time

BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISMS.settings')
django.setup()

from common.views import *


if __name__ == "__main__":
    i = 0
    while True:
        i += 1

        jj = isVaildDate("2010-10-10")
        print(str(jj))
        time.sleep(5)
        #print(os.getpid())
