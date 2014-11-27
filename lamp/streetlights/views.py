from django.shortcuts import render,HttpResponse
from djgeojson.serializers import Serializer
from models import Lampadaire

# Create your views here.
def index(request):
    return render(request, 'index.html')

def geodata(request):
    geojson = Serializer().serialize(
        Lampadaire.objects.all()[:100],
    )

    return HttpResponse(
        geojson,
        content_type="application/json"
    )
