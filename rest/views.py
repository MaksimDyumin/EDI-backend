from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from rest.models import Document
from rest.serializers import DocumentSerializer
# Create your views here.


class DocumentsViewsSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    
    serializer_class = DocumentSerializer