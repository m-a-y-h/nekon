from django.shortcuts import render
from rest_framework import viewsets
from .models import Partner, Share
from .serializers import PartnerSerializer, ShareSerializer

# Create your views here.


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
