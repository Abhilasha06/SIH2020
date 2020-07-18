from .serializer import AppUserSerializer, NGOUserSerializer, UserSerializer
from proj.models import AppUser, NGOUser
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FileUploadParser
from ..decorators import allowed_users
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from proj.MLModel.Detector_class.garbage_detector import GarbageDetector
from proj.models import UserContributionModel, ActiveImages, AppUser
from proj.maps_api import nearbyngo

# Token Authentication for Our Mobile App
# Session Authentication for Our Website

# These 2 Viewsets to Store User Personal Information


class MyViewSet1(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return AppUser.objects.filter(user=user)

    serializer_class = AppUserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class MyViewSet2(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        return User.objects.filter(username=user.username)

    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


# Returning List of Nearby NGO for User
class GetContributions(APIView):
    def get(self, request):

        obj = UserContributionModel.objects.get(user=self.request.user)
        print(obj.contribution)
        return Response(obj.contribution)

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class GetMyContribution(APIView):
    def get(self, request):
        print("Coming to getMyImages")
        obj = AppUser.objects.get(user=self.request.user)
        print(obj.contributionImages)
        # print(obj.name)
        return Response(obj.contributionImages)

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class getNGOList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lat = request.data['lat']
        lon = request.data['lon']
        content = nearbyngo.get_list(lat, lon)
        return Response(content)




class CheckImage(APIView):
    parser_class = (FileUploadParser, )
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if 'file' not in request.data:
            return Response("File not received")

        upfile = request.FILES['file']
        lat = request.data['lat']
        lon = request.data['lon']
        print(upfile.name)
        with open(upfile.name, 'wb+') as f1:
            for chunks in upfile.chunks():
                f1.write(chunks)

        res = GarbageDetector().detect(upfile.name)
        print(res)
        # Now Change User Contributions
        if(res == 1):
            # Now save the image in ActiveImages panel
            imgModel = ActiveImages(name=upfile.name, lat=lat, lon=lon)
            imgModel.save()
            userField = AppUser.objects.get(user=self.request.user)
            try:
                userField.contributionImages += "%"+(upfile.name)
            except:
                # print("At Except")
                userField.contributionImage += ""+upfile.name
            userField.save()
            obj = UserContributionModel.objects.get(user=self.request.user)
            obj.contribution = obj.contribution + 1
            obj.save()
            # Assuming File Name will not have "%"
            # print(userField.user)
            # print(userField.mob)
            # print(userField.contributionImages)
            # contributionImages
        # Will be getting lat and long too
        # and if already lat and long is present in databse then no contribution
        # increase orless point increase
        return Response(res)

# Some More API Views Here
