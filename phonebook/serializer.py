from rest_framework import serializers
from .models import PhoneBook


class PhonebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneBook
        fields = ['first_name',
                  'last_name',
                  'phone_number']
