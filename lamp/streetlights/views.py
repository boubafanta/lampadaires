from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import HttpRequest
from django.contrib.gis.measure import D
from djgeojson.serializers import Serializer
from models import Lampadaire
from django.contrib.gis.geos import Point
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
# Create your views here.
def index(request):
	return render(request,'index.html')
@csrf_exempt
def geodata(request):
	if request.method=='GET':
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
	elif request.method == 'POST':
		#s=request.POST.get['statut']
		s=request.POST.get['statut']
		id_lampe=float(request.POST.get['id'])
		sama_lampe=get_object_or_404(Lampadaire, gid=id_lampe)
		sama_lampe.states=s
		sama_lampe.save()
		geojson = Serializer().serialize(Lampadaire.objects.filter(gid=id_lampe))
		return HttpResponse(
			geojson,
        		content_type="application/json"
    		)
def denthialma(request):
		#s=request.POST.get['statut']
		s=request.GET['statut']
		id_lampe=float(request.GET['id'])
		sama_lampe=get_object_or_404(Lampadaire, gid=id_lampe)
		sama_lampe.states=s
		sama_lampe.save()
		geojson = Serializer().serialize(Lampadaire.objects.filter(gid=id_lampe))
		return HttpResponse(
			geojson,
        		content_type="application/json"
    		)
def yobouma(request):
	cursor = connection.cursor()
	try:
        		x1=float(request.GET['x1'])
        		y1=float(request.GET['y1'])
        		x2=float(request.GET['x2'])
        		y2=float(request.GET['y2'])
        		p=float(request.GET['p'])
        		#pt1= Point(x1,y1,srid=4326)
        		#pt1.transform(32628)
        		#pt2= Point(x2,y2,srid=4326)
        		#pt2.transform(32628)
	except Exception:
		pass
		
	cursor.execute("""SELECT param_seq, param_cost, param_coef, param_geom
			 FROM itib(%s,%s,%s,%s,%s)""", [x1,y1,x2,y2,p])
	#geojson = simplejson.dumps(row) #Serializer().serialize(cursor.fetchall() )
	#return HttpResponse(
	#		geojson,
        #		content_type="application/json"
    	#	)
    	geojson = json.dumps(
    	{ "type": "FeatureCollection"
    		,"features": [
    			{
    			"type": "Feature", "geometry": json.loads(row[3]),
    			"properties": {
    				"id_seq" : row[0], "cost" : row[1], "coeff" : row[2]
    				}
    			} for row in cursor.fetchall()
    		]
    		}
	)
	
    	return HttpResponse(geojson,content_type="application/json")