from django.http import HttpResponse
from django.http import JsonResponse
from .models import Clients, Interests

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