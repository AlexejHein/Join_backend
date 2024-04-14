from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from .models import MyModel


def create_model(request):
    if request.method == 'POST':
        # Erstellen einer Instanz und Setzen des Wertes basierend auf dem Formularinput
        instance = MyModel()
        instance.my_field = request.POST.get('my_field', '')
        instance.save()
        return redirect('success-url')  # Weiterleitung zu einer Erfolg-Seite
    return render(request, 'my_template.html')


class GenerateTokenView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('generate-token')
        else:
            # Rückmeldung geben, wenn die Anmeldung fehlschlägt
            return render(request, 'login.html', {'error': 'Ungültiger Benutzername oder Passwort'})
    return render(request, 'login.html')

