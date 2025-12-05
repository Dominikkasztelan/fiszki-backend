from rest_framework import serializers
from .models import Slowko

class SlowkoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slowko
        fields = '__all__'  # To sprawia, że wszystkie pola (angielski, polski, wymowa, details) trafią do API