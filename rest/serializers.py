from rest_framework.serializers import ModelSerializer
from rest.models import Document

class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'file', 'created_at', 'updated_at', 
                  'status', 'need_sign', 'creator', 'recipient'
                ]