from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import api_view, permission_classes

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from .models import Carrera, Materia, Alumno, Inscripcion, Card
from .serializers import CarreraSerializer, MateriaSerializer, AlumnoSerializer, InscripcionSerializer, CardSerializer, RegisterSerializer

from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsAdminOrReadOnly]

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [IsAdminOrReadOnly]
class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['carrera']
    search_fields = ['nombre','apellido_paterno', 'numero_control']
    ordering_fields = ['nombre', 'numero_control']


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'detail': 'User registered successfully. Log in to obtain the token.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me (request):
    user = request.user
    if request.method == 'GET':
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff
        })

    data = request.data
    if 'email' in data:
        if User.objects.filter(email__iexact=data['email']).exclude(pk=user.pk).exists():
            return Response({'error': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
    if 'username' in data:
        if User.objects.filter(username__iexact=data['username']).exclude(pk=user.pk).exists():
            return Response({'error': 'Username is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
    user.save()
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "User logged out successfully."}, status=status.HTTP_204_NO_CONTENT)

class ResetTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        # Create a new token
        token = Token.objects.create(user=request.user)
        return Response({
            'token': token.key,
            "detail":" Token reset successfully."
        }, status=status.HTTP_200_OK)