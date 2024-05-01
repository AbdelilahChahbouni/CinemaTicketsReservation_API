
from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from tickets.api import *

router = DefaultRouter()
router.register('guests' , ViewsetsGuest)
router.register('movies' , ViewsetsMovie)
router.register('reservations' , ViewsetsReservation)



urlpatterns = [
    path('admin/', admin.site.urls),
    #1 Response no rest no model
    path('django/api/response_no_rest_no_model/', no_rest_no_models),
    #2 Response from model no rest
    path('django/api/response_from_model_no_rest/' , no_rest_from_model),
    #3 Functions Based Views
    #3.1 GET , POST , @api_view
    path('rest/fbv/list_post',fbv_list_post),
    #3.2 GET PUT DELETE , pk
    path('rest/fbv/<int:pk>', fbv_pk),
    #4 Class Based Views APIView
    #4.1 GET POST , APIView
    path('rest/cbv/list_post' , Cbv_List_Post.as_view()),
    #4.2 GET , PUT , DELETE , pk , APIView
    path('rest/cbv/<int:pk>', Cbv_pk.as_view()),
    #5 Class Based Views Mixins
    #4.1 GET POST , Mixins
    path('rest/mixins/list_post' , MixinsListCreate.as_view()),
    #4.2 GET , PUT , DELETE , pk , Mixins
    path('rest/mixins/<int:pk>', MixinsPk.as_view()),
    #6 Class Based Views Generics
    #6.1 GET POST , Generics
    path('rest/generics/list_post' , GenericsListCreate.as_view()),
    #6.2 GET , PUT , DELETE , pk , Generics
    path('rest/generics/<int:pk>', GenericsPk.as_view()),
    #7 Viewsets
    path('rest/viewsets/', include(router.urls)),
    #8 find movie
    path('rest/find_movie', find_movie),
    #9 new Reservation
    path('rest/new_reservation' , make_reservation)




]
