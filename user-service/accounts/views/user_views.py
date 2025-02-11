from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from ..serializers import UserSerializer
from ..service.user_service import UserService
from ..permisions import IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    user_service = UserService()

    def get_queryset(self):
        return self.user_service.get_active_users()

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.user_service.create_user(serializer.validated_data)
            return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            user = self.user_service.update_user(pk, serializer.validated_data)
            return Response(self.get_serializer(user).data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            user = self.user_service.delete_user(pk)
            return Response(self.get_serializer(user).data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def by_role(self, request):
        role = request.query_params.get('role')
        if not role:
            return Response({'error': 'Role parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        users = self.user_service.get_users_by_role(role)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)