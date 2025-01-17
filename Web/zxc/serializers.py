from rest_framework import serializers

class CourseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    categorycourse = serializers.CharField(max_length=50)
    price = serializers.DecimalField(decimal_places=2, max_digits=7)