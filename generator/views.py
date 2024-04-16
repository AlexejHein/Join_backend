from django.http import JsonResponse
from .models import Token, ReceivedData


def generate_token(request):
    new_token = Token.objects.create()
    return JsonResponse({'token': str(new_token.token)})


def receive_data(request):
    token = request.GET.get('token')
    data = request.GET.get('data')  # Beispiel: ein einfacher Datenstring

    try:
        token_obj = Token.objects.get(token=token)
        ReceivedData.objects.create(token=token_obj, data=data)
        return JsonResponse({'status': 'success', 'data_received': data})
    except Token.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=400)
