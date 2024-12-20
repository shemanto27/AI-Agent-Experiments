from rest_framework import serializers

class instruction_serializer(serializers.Serializer):
    instruction = serializers.CharField(max_length=1000)

class response_serializer(serializers.Serializer):
    response = serializers.CharField(max_length=100000)