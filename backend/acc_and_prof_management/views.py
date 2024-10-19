from rest_framework import viewsets, permissions, generics
from rest_framework.authtoken.models import Token
from .models import Dish
from .serializers import DishSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def create(self, request, *args, **kwargs):
        print(request.data)  # Print the incoming request data
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid Credentials"}, status=400)
    
class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            # Filter dishes based on the query (case insensitive)
            dishes = Dish.objects.filter(title_en__icontains=query)
            serializer = DishSerializer(dishes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)
        
        