from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import RegisterSerializer, UserSerializer
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import json
import datetime 

from .models import PersonalProfile
#Register API


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        request.data['password'] = make_password(request.data['password'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()    
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
        
class setProfile(APIView):
    def post(self, request):
        user = User.objects.get(username = request.user.username)
        json_data = json.loads(request.body)
        interest = json.dumps(json_data["interest"])
        skill = json.dumps(json_data["skill"])
        wantingToLearn = json.dumps(json_data["wantingToLearn"])
        if PersonalProfile.objects.filter(username = user.username).exists():
            profile = PersonalProfile.objects.filter(username = user.username)
            profile.update(
                name = json_data["name"],
                gender = json_data["gender"],
                birthday = json_data["birthday"],
                job = json_data["name"],
                interest = interest,
                skill = skill,
                wantingToLearn = wantingToLearn    
            )
            print("update")
            return HttpResponse(status = 200)
        PersonalProfile.objects.create(
            username = user.username,
            name = json_data["name"],
            gender = json_data["gender"],
            birthday = json_data["birthday"],
            job = json_data["name"],
            interest = interest,
            skill = skill,
            wantingToLearn = wantingToLearn  
        )
        print("create")
        return HttpResponse(status = 200)
    
class getProfile(APIView):
    def get(self, request):
        print(request.user.username)
        if request.user.username == None:
            return HttpResponse(status = 401)
        
        profile = PersonalProfile.objects.get(username = request.user.username)
        
        jsonDec = json.decoder.JSONDecoder()
        interest = jsonDec.decode(profile.interest)
        skill = jsonDec.decode(profile.skill)
        wantingToLearn = jsonDec.decode(profile.wantingToLearn)
        
        json_data = {
            "name" : profile.name,
            "gender" : profile.gender,
            "birthday" : profile.birthday.strftime('%Y-%m-%d'),
            "job" : profile.job,
            "interest" : interest,
            "skill" : skill,
            "wantingToLearn" : wantingToLearn
        }
        json_data = json.dumps(json_data)
        return HttpResponse(json_data, content_type="application/json", status = 200)
        
        
    