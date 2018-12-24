from rest_framework import status, permissions
from rest_framework import mixins, generics
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import Note
from .serializers import NoteSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

import socket
host = socket.gethostname()  # get local machine name
port = 5432  # Make sure it's within the > 1024 $$ <65535 range
s = socket.socket()
s.connect((host, port))

class NoteList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    """
     List all notes, or create a note
    """
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    serializer_class = NoteSerializer

    def get_queryset(self, *args, **kwargs):
        return Note.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req = self.create(request, *args, **kwargs)
        request_dict = dict(request.data)
        req_str = (request_dict['name'][0].encode('utf-8') + "@*@NINO@*@".encode('utf-8') + request_dict['image'][0]._get_name().encode('utf-8') +
        "@*@NINO@*@".encode('utf-8') + str(request.user).encode('utf-8') + "@*@NINO_END@*@".encode('utf-8'))
        #s.send(request_dict['name'][0].encode('utf-8'))
        #s.send("@*@NINO@*@".encode('utf-8'))
        #s.send(request_dict['image'][0]._get_name().encode('utf-8'))
        #s.send("@*@NINO@*@".encode('utf-8'))
        #s.send(str(request.user).encode('utf-8'))
        s.send(req_str)
        return req

class NoteDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve, update or delete a note instance.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NoteSerializer

    def get_object(self, pk):
        try:
            return Note.objects.filter(owner=self.request.user).get(pk=pk)
        except Note.DoesNotExist:
            raise

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = NoteSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
