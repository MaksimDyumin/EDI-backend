from django.shortcuts import render
from django.http import FileResponse
from django.db.models import Q

from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from rest.models import Document, Signature, User
from rest.serializers import (DocumentSerializer, AwaitFixesSerializer, 
                              UploadDocumentSerializer, SignaturesSerializer,
                              UserSerializer, CreateDocumentSerializer)
# Create your views here.


class DocumentsViewsSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if(self.action == 'retrieve'):
            return Document.objects.filter(Q(creator=user) | Q(recipient=user))
        return Document.objects.filter(Q(status='Complete') | Q(status='Rejected')).filter(Q(creator=user) | Q(recipient=user))
    
    def get_serializer_class(self):
        if(self.action == 'await_fixes'):
            return AwaitFixesSerializer
        if(self.action == 'send_fixes'):
            return UploadDocumentSerializer
        if(self.action == 'create'):
            return CreateDocumentSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        kwargs = {}
        kwargs['status'] = Document.WAIT_PROCESSING
        if not serializer.validated_data.get('name'):
            filename = serializer.initial_data['file'].name
            kwargs['name'] = filename
        serializer.save(creator=self.request.user, **kwargs)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        return self.get_documents(request, creator=request.user)
    
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        return self.get_documents(request, recipient=request.user)
    
    def get_documents(self, request, **kwargs):
        sent_documents = Document.objects.exclude(status='Complete').exclude(status='Rejected').filter(**kwargs)

        page = self.paginate_queryset(sent_documents)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(sent_documents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk):
        try:
            # Получение документа по ID
            document = Document.objects.get(Q(recipient=request.user) | Q(creator=request.user), id=pk)
        except Document.DoesNotExist:
            # Если документ не найден, возвращаем ошибку 404
            raise NotFound("Документ не найден")

        file_path = document.file.path
        file = open(file_path, 'rb')
        return FileResponse(file, as_attachment=True, filename=document.file.name)
    
    def get_user_document(self, id, **kwargs):
        try:
            return Document.objects.get(~Q(status='Complete') & ~Q(status='Rejected'), id=id, **kwargs)
        except Document.DoesNotExist:
            raise NotFound("Документ не найден")
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk):
        document = self.get_user_document(pk, recipient=request.user)

        document.status = Document.COMPLETE
        document.save()
        return Response("EDI Complete")
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        document = self.get_user_document(pk, recipient=request.user)
        document.status = Document.REJCTCTED
        document.save()
        return Response("EDI rejected")
    
    @action(detail=True, methods=['put'])
    def await_fixes(self, request, pk):
        document = self.get_user_document(pk, recipient=request.user)
        document.status = Document.WAIT_FIX
        comment_serializer = self.get_serializer(data=request.data)
        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save(document=document)
        document.save()
        return Response("Document sent to fix")
    
    @action(detail=True, methods=['post'])
    def send_fixes(self, request, pk):
        document = self.get_user_document(pk, creator=request.user)
        document.status = Document.WAIT_PROCESSING
        comment_serializer = self.get_serializer(data=request.data)
        comment_serializer.is_valid(raise_exception=True)
        document.save()
        return Response("Document was fixed")
    
class SignaturesView(ListCreateAPIView):
    serializer_class = SignaturesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Signature.objects.filter(Q(creator=user) | (Q(document__creator=user) | Q(document__recipient=user)))
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class SignatureDownloadView(RetrieveAPIView):
    serializer_class = SignaturesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Signature.objects.filter(Q(creator=user) | (Q(document__creator=user) | Q(document__recipient=user)))

    def get(self, request, *args, pk=None, **kwargs):
        try:
            signature = self.get_queryset().get(id=pk)
        except Signature.DoesNotExist:
            raise NotFound("Документ не найден")

        file_path = signature.file.path
        file = open(file_path, 'rb')
        return FileResponse(file, as_attachment=True, filename=signature.file.name)
    
class UsersView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    


    