from django.contrib import admin

# Register your models here.
# slowka/admin.py
from django.contrib import admin
from .models import Slowko

admin.site.register(Slowko)