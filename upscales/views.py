from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UpscaleSerializer
from .models import Upscale


class UpscaleViewSet(viewsets.ModelViewSet):
    queryset = Upscale.objects.all()
    serializer_class = UpscaleSerializer
