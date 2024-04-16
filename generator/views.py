from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Token, ReceivedData
import json


@csrf_exempt
@require_http_methods(["POST", "GET", "DELETE"])
def item(request):
    # Token aus dem Header extrahieren
    token_header = request.headers.get('Authorization')
    if not token_header or not token_header.startswith('Bearer '):
        return JsonResponse({'status': 'error', 'message': 'No token provided'}, status=401)

    token_str = token_header.split(' ')[1]
    try:
        token = Token.objects.get(token=token_str)
    except Token.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=401)

    if request.method == 'POST':
        # Daten setzen
        data = json.loads(request.body)
        key = data.get('key')
        value = data.get('value')
        ReceivedData.objects.update_or_create(key=key, token=token, defaults={'value': value})
        return JsonResponse({'status': 'success', 'message': 'Data saved'})

    elif request.method == 'GET':
        # Daten abrufen
        key = request.GET.get('key')
        try:
            data_item = ReceivedData.objects.get(key=key, token=token)
            return JsonResponse({'status': 'success', 'data': data_item.value})
        except ReceivedData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Data not found'}, status=404)

    elif request.method == 'DELETE':
        # Daten löschen
        key = request.GET.get('key')
        ReceivedData.objects.filter(key=key, token=token).delete()
        return JsonResponse({'status': 'success', 'message': 'Data deleted'})

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


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
