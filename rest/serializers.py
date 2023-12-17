from rest_framework.serializers import ModelSerializer
from rest.models import Document, Comment, Signature, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'department', 'job_title']
        read_only_fields = ['creator']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']

class CreateDocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'file','need_sign', 'recipient']

class DocumentSerializer(ModelSerializer):
    creator = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Document
        fields = [
					'id', 'name', 'file', 'created_at', 'updated_at', 
					'status', 'need_sign','comments', 'creator', 'recipient',
                    'signatures'
                ]
        read_only_fields = ['creator', 'signatures', 'status']
        
class AwaitFixesSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']

class UploadDocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'updated_at', 'name']

class SignaturesSerializer(ModelSerializer):
    class Meta:
        model = Signature
        fields = ['id', 'created_at', 'file', 'creator', 'document']

        read_only_fields = ['creator']