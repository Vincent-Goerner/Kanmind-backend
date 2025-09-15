from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'fullname': f'{saved_account.username} {saved_account.last_name}',
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            return Response({'400': 'Ungültige Anfragedaten.', 'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data)
    
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'fulname': f'{user.username} {user.last_name}',
                'email': user.email,
                'user_id': user.id
            }
        else:
            return Response({'400': 'Ungültige Anfragedaten.', 'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data)