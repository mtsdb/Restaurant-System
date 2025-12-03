from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserSerializer, CreateUserSerializer


class CustomObtainAuthToken(ObtainAuthToken):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data, context={"request": request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		token, created = Token.objects.get_or_create(user=user)
		data = {
			"token": token.key,
			"user": UserSerializer(user).data,
		}
		return Response(data)


class CurrentUserView(APIView):
	def get(self, request):
		user = request.user
		serializer = UserSerializer(user)
		return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by("id")
	serializer_class = UserSerializer
	permission_classes = [IsAdminUser]

	def get_serializer_class(self):
		if self.action == "create":
			return CreateUserSerializer
		return UserSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		output = UserSerializer(user).data
		return Response(output, status=status.HTTP_201_CREATED)
