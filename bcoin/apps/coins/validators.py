from rest_framework import serializers


def is_greater_than_0(value):
    if value >= 0:
        return
    else:
        raise serializers.ValidationError(f"Value must be greater than 0: {value}")
