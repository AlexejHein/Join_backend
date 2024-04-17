from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Token, ReceivedData
import json


@csrf_exempt
@require_http_methods(["POST", "GET", "DELETE"])
def item(request):
    token_header = request.headers.get('Authorization', '')
    if not token_header.startswith('Bearer '):
        return JsonResponse({'status': 'error', 'message': 'Missing or malformed token'}, status=401)

    token_str = token_header[7:]  # Entfernt 'Bearer '
    try:
        token = Token.objects.get(token=token_str)
    except Token.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            key = data['key']
            value = data['value']
            # Fügen Sie hier eine Logikprüfung hinzu, um sicherzustellen, dass alle Felder korrekt sind
            data_item, created = ReceivedData.objects.update_or_create(
                key=key,
                token=token,
                defaults={'value': value}
            )
            return JsonResponse(
                {'status': 'success', 'data': {'key': key, 'value': value}, 'message': 'Data created or updated'},
                status=201 if created else 200)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid data or malformed JSON: ' + str(e)}, status=400)

    elif request.method == 'GET':
        key = request.GET.get('key')
        if not key:
            return JsonResponse({'status': 'error', 'message': 'Key is required'}, status=400)
        try:
            data_item = ReceivedData.objects.get(key=key, token=token)
            return JsonResponse({'status': 'success', 'data': {'key': key, 'value': data_item.value}})
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
