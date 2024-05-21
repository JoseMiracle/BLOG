from rest_framework import generics, permissions, status
from blog.accounts.api.v1.serializers import (
    SignUpSerializer,
    SignInSerializer,
    ChangePasswordSerializer,
    UserSerializer,
)
from rest_framework.response import Response


class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ("post", )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class SignInAPIView(generics.GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ("post", )

  
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)
        


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ("put", )

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(
            {"Update Info": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )


class RetrieveUpdateProfileAPIView(generics.RetrieveUpdateAPIView,):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

