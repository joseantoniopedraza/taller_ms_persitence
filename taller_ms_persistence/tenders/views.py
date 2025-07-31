from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Tenders

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
