from django.http.response import JsonResponse  
from rest_framework.response import Response
from django.shortcuts import render
from tickets.models import Guest,Moive,Reservation ,Post
from .serializers import GuestSerializer,MovieSerializer,ReservationSerializer , PostSerializer
from rest_framework.decorators import api_view
from rest_framework import status, filters , mixins, generics , viewsets
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.authentication import BasicAuthentication , TokenAuthentication   
from rest_framework.permissions import IsAuthenticated
from .permissions import  IsAuthorOrReadOnly

# 1- without REST and no model query FBV


def no_reset_no_model(requets):
    
    guests = [
        {
            'id':1,
            "name" : "Mohsen",
            "mobile": +201166558877,
        },
         {
            'id':2,
            "name" : "Gamal",
            "mobile": +201166558855,
        }
    ]
    return JsonResponse(guests,safe=False)


# 2- model data default django without rest 
def no_rest_from_model (request):

    data = Guest.objects.all()

    response = {
        "guests": list(data.values('name','mobile'))
    }


    return JsonResponse(response,safe=False)



# List -> GET
# Create -> POST
# pk query == GET
# Update == PUT
# Delete Destroy == DELETE 

# 3- Function based views
# 3.1 GET POST

@api_view(["GET",'POST'])
def FBV_List(request):
    """
    GET -> list all guests 
    POST -> Create new guest 
    """
    # GET
    if request.method =="GET":
        guests= Guest.objects.all()
        serializer = GuestSerializer(guests,many=True)

        return Response(serializer.data)

    elif request.method =="POST":
        serializer= GuestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return  Response({"data":serializer.data,"erros":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

# 3.1 GET PUT DELETE
@api_view(["GET","PUT","DELETE"])
def FBV_pk(request,pk):
    try: 
        guest = Guest.objects.get(pk=pk)

    except Guest.DoesNotExist:


        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":

        serializer = GuestSerializer(guest,many=False)  
        return Response(serializer.data)
        
    elif request.method == "PUT":
        serializer= GuestSerializer(guest,data=request.data,partial=True)# passing data parameter means inserting new data in the db or updating existing one 
        
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return  Response(
                {
                    "data":serializer.data,
                  "erros":serializer.errors},
                  status=status.HTTP_400_BAD_REQUEST
                )



    elif request.method == "DELETE":        
        guest.delete()
        print(guest)
        return Response({"data":"element is deleted"},status=status.HTTP_204_NO_CONTENT)


# CBV Class based views
# 4.1 List and Create == GET AND POST


  
class CBV_List(APIView):


    def get(self,request):
        try:
            guests = Guest.objects.all()
            serializer = GuestSerializer(guests,many=True)
            return Response({'data':serializer.data} , status=status.HTTP_200_OK)
        except:
            return Response({'errors':serializer.errors} , status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):

        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"data":serializer.data,"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        


# 4.2 GET PUT DELETE CBV views -- pk 
        
class CBV_PK(APIView):
    """
    GET -> Retrive single element
    PUT -> Update all data related to single element
    PATCH -> Parialy update data
    DELETE -> Delete element
    """

    # instead of every time query the db in every METHOD(GET,PUT,PATCH,DELETE) we could defined a function that will do that for us 
    # the following function
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self,request ,pk ):
        try:
            guest = Guest.objects.get(pk=pk)
            serializer = GuestSerializer(guest)
            return Response({'data':serializer.data} , status=status.HTTP_200_OK)
        except:
           # raise Http404
            return Response({"erros":"object not found"},status=status.HTTP_400_BAD_REQUEST)



    def put(self,request,pk):
        """Update all data"""
        guest = Guest.objects.get(pk=pk)
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"data":serializer.data,"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self,request,pk):
        """Partialy Update  data"""
        guest = Guest.objects.get(pk=pk)

        serializer = GuestSerializer(guest,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"data":serializer.data,"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)



    def delete(self,request,pk):
        """Delete element"""
        try: 
            guest = Guest.objects.get(pk=pk)
            guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Guest.DoesNotExist:
            return Response({"erros":"the object doesnot Exist Anymore"},status=status.HTTP_404_NOT_FOUND)
        
#  When to use FBV/CBV?
#   It has no riight answer but 
#   i you have a lot of bussiness logic it's prefered to use FBV



# 5 Mixins
# 5.1 mixins list
        
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin ,generics.GenericAPIView ):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    

# 5.2 mixins get put delete --pk
    
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView) :
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self,request , pk):
        return self.retrieve(request)
    
    def put(self,request , pk):
        return self.create(request)
    
    
    def delete(self,request , pk):
        return self.destroy(request)
    
# 6 Generics
# 6.1 get and post

class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes= [IsAuthenticated]


# 6.2 get put and delete
    
class generics_pk (generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes= [IsAuthenticated]


# 7 viewsets
# all in one end point
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Moive.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']


    
class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer



#8 Find movie
@api_view(['GET'])
def find_movie(request):
    try:
        movies = Moive.objects.filter(movie = request.data['movie'], hall = request.data['hall']) # it's not a search , it's matching 

    except :
         return Response({"data":request.data , "Status":"Somthing Went wrong"} ,status=status.HTTP_400_BAD_REQUEST)
    
    serializer = MovieSerializer(movies,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

    
#9 Create new reservation

@api_view(['POST'])
def new_reservation(request):
    movie = Moive.objects.get(movie = request.data['movie'], hall = request.data['hall'])

    guest = Guest() 
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation.objects.create(moive=movie,guest=guest)

    #reservation.save() -> this line is useless 

    return Response({'data':
                     
                     [
                         {
                        "guest_name":reservation.guest.name,
                        "guest_mobile": reservation.guest.mobile,
                        "movie": reservation.moive.movie,
                        "movie_hall":reservation.moive.hall,
                        "movie_date" :  reservation.moive.date
                        }
                     ]
                     
                     },
                     
                     status=status.HTTP_201_CREATED)



# @api_view(['GET','POST'])
# def manipulate_read_post(request,pk):
#     if 
#     pass

# 10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    
    queryset= Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
