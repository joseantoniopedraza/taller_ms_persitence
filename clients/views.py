from django.http import HttpResponse
from django.http import JsonResponse
from .models import Clients, Interests, Clients_Interests
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the client index.")

def clients_list(request):
    clients_data = []

    for client in Clients.objects.all():
        interests = client.clients_interests_set.all().select_related('interest')
        interests_names = [ci.interest.name for ci in interests]

        clients_data.append({
            'name': client.name,
            'email': client.email,
            'interests': interests_names
        })

    return JsonResponse(clients_data, safe=False)


def interests_list(request):
    interests = Interests.objects.all()
    interests_data = [{'id': i.id, 'name': i.name} for i in interests]
    return JsonResponse(interests_data, safe=False)


@csrf_exempt
def create_client_with_interests(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            interests = data.get('interests', [])  # Lista de strings

            if not name or not email:
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)

            # Crear el cliente
            client = Clients.objects.create(name=name, email=email)

            # Asociar intereses
            for interest_name in interests:
                interest, created = Interests.objects.get_or_create(name=interest_name)
                Clients_Interests.objects.create(client=client, interest=interest)

            return JsonResponse({
                'message': 'Cliente creado correctamente',
                'client_id': client.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)