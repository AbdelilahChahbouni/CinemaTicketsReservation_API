from django.http.response import JsonResponse
from django.http import Http404
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status , filters
from rest_framework.views import APIView 
from rest_framework import mixins , generics , viewsets
from .serializers import *
from .models import *
 
#1 without rest and models
def no_rest_no_models(request):
    data_guest = [{
        'id': 1,
        'name':'ali',
        'phone': 1234
    },
    {'id': 2,
     'name':'reda',
     'phone':12345
     }
     ]
    return JsonResponse(data_guest , safe=False)

#2 data from model without rest
def no_rest_from_model(requset):
    data = Guest.objects.all()
    response = {
        'guest' : list(data.values('id', 'name','modile', 'reser_geust'))
    }
    return JsonResponse(response , safe=False)

# Notes
'''
 ---HTTP METHODES---
# List == GET
# CREATE == POST
# UPDATE == PUT , PUTCH
# REMOVE , DESTROY == DELETE
# PK QUERY == GET
'''

#3 Functions Based Views

#3.1  GET , POST
@api_view(["GET", "POST"])
def fbv_list_post(request):

    #GET 
    if request.method == "GET":
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests , many=True)
        return Response(serializer.data)
    #PSOT 
    elif request.method == "POST":
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED )
        else:
            return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)
        

#3.2 GET , PUT , DELETE :pk
@api_view(['GET','PUT','DELETE'])
def fbv_pk(request,pk):
    try :
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else: 
            return Response(serializer.error,status=status.HTTP_406_NOT_ACCEPTABLE)
        
    elif request.method == 'DELETE':
        guest.delete()
        return Response({"status":"deleted"},status=status.HTTP_204_NO_CONTENT)
    
#4 Class Based Views APIView
#4.1 GET , POST
class Cbv_List_Post(APIView):
    #GET
    def get(self , request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests , many=True)
        return Response(serializer.data)
    

    #POST 
    def post(self , request):
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data ,
                status= status.HTTP_201_CREATED            
                            )
        else:
            return Response(serializer.data , status = status.HTTP_400_BAD_REQUEST)
    
#4.2 GET , PUT , DELETE , pk
class Cbv_pk(APIView):
    # get object using pk
    def get_object(self,pk):
        try:
            guest = Guest.objects.get(pk=pk)
            return guest
        except Guest.DoesNotExist:
            raise Http404
    # GET    
    def get(self , request , pk):
        serializer = GuestSerializer(self.get_object(pk=pk))
        return Response(serializer.data)
    
    # PUT 
    def put(self , request , pk):
        serializer = GuestSerializer(self.get_object(pk=pk), data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status = status.HTTP_202_ACCEPTED)
        return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE 
    def delete(self , request , pk):
        guest = self.get_object(pk=pk)
        guest.delete()
        return Response({'status', "the object is deleted"})
    
#5 Class Based View Mixins
#5.1 GET POST
class MixinsListCreate(mixins.ListModelMixin, mixins.CreateModelMixin , generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    #GET
    def get(self , request):
        return self.list(request)
    #POST
    def post(self , request):
        return self.create(request)  

#5.2 GET , PUT , DELETE , pk
class MixinsPk(mixins.RetrieveModelMixin , mixins.UpdateModelMixin , mixins.DestroyModelMixin , generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    # GET 
    def get(self , request , pk):
        return self.retrieve(request)
    #PUT 
    def put(self , request , pk):
        return self.update(request)
    # DELETE 
    def delete(self , request , pk):
        return self.destroy(request)
    
#6 Class Based View Generics
#6.1 GET POST
class GenericsListCreate(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

#6.2 GET PUT DELETE , pk
class GenericsPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

#7 Viewsets
class ViewsetsGuest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class ViewsetsMovie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ViewsetsReservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
# find movie
@api_view(["GET"])
def find_movie(request):
    movies = Movie.objects.filter(
        movie = request.data['movie'],
        hall = request.data['hall']
    )
    serializer = MovieSerializer(movies , many=True)
    return Response(serializer.data)

@api_view(["POST"])
def make_reservation(request):
    name_guest = request.data['guest']
    mobile = request.data['mobile']
    movie = request.data['movie']
    if not Guest.objects.filter(name=name_guest).exists():
        new_guest = Guest.objects.create(
            name = name_guest,
            mobile= mobile
        )
        new_movie = Movie.objects.get(movie=movie)
        new_res = Reservation.objects.create(
            geust = new_guest,
            movie = new_movie
        )
        serializer = ReservationSerializer(new_res)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    else:
        new_movie = Movie.objects.get(movie=movie)
        new_guest = Guest.objects.get(name = name_guest )
        new_res = Reservation.objects.create(
            geust = new_guest ,
            movie = new_movie
        )
        
        serializer = ReservationSerializer(new_res)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

