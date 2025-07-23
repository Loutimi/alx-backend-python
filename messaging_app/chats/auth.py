from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class LoginView(TokenObtainPairView):
    # Inherits post method for obtaining access & refresh tokens
    pass

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Optional: requires 'rest_framework_simplejwt.token_blacklist'
            return Response({"detail": "Successfully logged out"})
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)
