from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User

from django.http import HttpResponse
import socket

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        pod_hostname = socket.gethostname()
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response_data = {
            'pod_hostname': pod_hostname,
            'users': serializer.data
        }
        return Response(response_data)

    def retrieve(self, request, pk):
        pod_hostname = socket.gethostname()
        serializer = self.get_serializer(self.get_object())
        response_data = {
            'pod_hostname': pod_hostname,
            'data': serializer.data
        }
        return Response(response_data)

    def create(self, request):
        data = request.data

        if self.get_queryset().filter(dni=data.get('dni', '')).exists():
            return Response({'detail': 'User already exists'}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        pod_hostname = socket.gethostname()
        response_data = {
            'pod_hostname': pod_hostname,
            'data': serializer.data
        }
        return Response(response_data, status=201)