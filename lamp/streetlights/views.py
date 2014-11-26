from django.shortcuts import render,HttpResponse
from django.http import HttpRequest
from django.contrib.gis.measure import D
from djgeojson.serializers import Serializer
from models import Lampadaire
from django.contrib.gis.geos import Point
# Create your views here.
def index(request):
	return render(request,'index.html')
def geodata(request):
	try:
        	x=float(request.GET['x'])
        	y=float(request.GET['y'])
        	p=float(request.GET['p'])
        	pt= Point(x,y,srid=4326)
        	pt.transform(32628)
	except Exception:
        	pass
	geojson = Serializer().serialize(
	#Lampadaire.objects.all()[:100],
	Lampadaire.objects.filter(geom__dwithin=(pt,D(m=p) ) ) )
	return HttpResponse(
		geojson,
        	content_type="application/json"
    	)