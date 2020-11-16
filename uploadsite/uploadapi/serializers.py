from rest_framework import serializers

from .models import File


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('file_uuid', 'name', 'created_at', 'uploaded_at', 'zipname', 'user_uuid')
