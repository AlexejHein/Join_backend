from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Token, ReceivedData
import json


@csrf_exempt
@require_http_methods(["POST", "GET", "DELETE"])
def item(request):
    token_header = request.headers.get('Authorization')
    token_str = token_header.split(' ')[1]
    token = Token.objects.get(token=token_str)

    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key')
        value = data.get('value')

        # Erhalte die höchste Version für diesen Schlüssel und Token
        latest_version = ReceivedData.objects.filter(key=key, token=token).order_by('-version').first()
        new_version = latest_version.version + 1 if latest_version else 1

        # Erstelle immer einen neuen Datensatz
        ReceivedData.objects.create(key=key, token=token, value=value, version=new_version)
        return JsonResponse({'status': 'success', 'message': 'Data saved with new version'})

    elif request.method == 'GET':
        key = request.GET.get('key')
        if key:
            try:
                data_item = ReceivedData.objects.get(key=key, token=token)
                return JsonResponse({'status': 'success', 'data': data_item.value})
            except ReceivedData.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Data not found'}, status=404)
        else:
            # Kein spezifischer Schlüssel, gib alle Daten für das Token zurück
            data_items = ReceivedData.objects.filter(token=token)
            data_list = [{'key': item.key, 'value': item.value} for item in data_items]
            return JsonResponse({'status': 'success', 'data': data_list})

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
