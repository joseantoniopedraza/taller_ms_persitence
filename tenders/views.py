from django.shortcuts import render

# Create your views here.
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Tenders
import RedisConnect
from config import host, port

def tenders_list(request):
    tenders = Tenders.objects.all()
    data = [
        {
            'id': tender.id,
            'code': tender.code,
            'title': tender.title,
            'description': tender.description
        }
        for tender in tenders
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_tender(data):
    try:
        data = json.loads(data)

        title = data.get('payload').get('title')
        description = data.get('payload').get('description')
        code = data.get('payload').get('code')

        if not title or not description or not code:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        if Tenders.objects.filter(code=code).exists():
            return JsonResponse({'error': 'Ya existe una licitación con ese código'}, status=409)

        tender = Tenders.objects.create(title=title, description=description, code=code)

        return JsonResponse({
            'message': 'Licitación creada correctamente',
            'tender_id': tender.id
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

redis_client = RedisConnect.RedisConnect(host=host, port=port)
redis_client.listen("messages", create_tender)
 