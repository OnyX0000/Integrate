from rest_framework import serializers
from .models import LegalQAFinal

class LegalQAFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalQAFinal
        fields = '__all__'