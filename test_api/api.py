from django.contrib.auth import get_user
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from register_test.settings import SECRET_KEY
from .serializer import RegisterSerializer, UserSerializer
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import json
import jwt
import datetime 
import base64
from base64 import b64decode

from register_test.settings import SECRET_KEY
from .models import Hobby, PersonalProfile, Learn, Skill
#Register API

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        request.data['password'] = make_password(request.data['password'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() 
        user.is_active = False
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
 
class ActivateAPI(APIView):
    def post(self, request):
        username = json.loads(request.body)['username']
        user = User.objects.get(username = username)
        
        if user == None:
            json_data = json.dumps({ "message": "bruh" })
            return HttpResponse(json_data, content_type="application/json", status = 400)
        user.is_active = True
        json_data = json.dumps({ "message": "OK" })
        return HttpResponse(json_data, content_type="application/json", status = 200)
        
class setProfile(APIView):
    def post(self, request):
        jsonDec = json.decoder.JSONDecoder()
        user = User.objects.get(username = request.user.username)
        json_data = json.loads(request.body)
        interest = json.dumps(json_data["interest"])
        skill = json.dumps(json_data["skill"])
        wantingToLearn = json.dumps(json_data["wantingToLearn"])
        
        for i in json_data["interest"]:  
            if not Hobby.objects.filter(LabelName=i).exists():
                Hobby.objects.create(LabelName=i)
            hobbys = Hobby.objects.get(LabelName=i) 
            hobby_list = jsonDec.decode(hobbys.InterestUser) if hobbys.InterestUser != None else []
            if not user.username in hobby_list:
                hobby_list.append(user.username)
            data = json.dumps(hobby_list)
            Hobby.objects.filter(LabelName=i).update(InterestUser=data)                                       
        for i in json_data["skill"]:
            if not Skill.objects.filter(LabelName_Skill=i).exists():
                Skill.objects.create(LabelName_Skill=i)
            skills = Skill.objects.get(LabelName_Skill=i)
            skill_list = jsonDec.decode(skills.Skill_User) if skills.Skill_User != None else []
            if not user.username in skill_list:
                skill_list.append(user.username)
            data = json.dumps(skill_list)
            Skill.objects.filter(LabelName_Skill=i).update(Skill_User=data)               
        for i in json_data["wantingToLearn"]:
            if not Learn.objects.filter(LabelName_Learn=i).exists():
                Learn.objects.create(LabelName_Learn=i) 
            wantingToLearns = Learn.objects.get(LabelName_Learn=i)         
            learn_list = jsonDec.decode(wantingToLearns.wantingToLearn_User) if wantingToLearns.wantingToLearn_User != None else []
            if not user.username in learn_list:
                learn_list.append(user.username)
            data = json.dumps(learn_list)
            Learn.objects.filter(LabelName_Learn=i).update(wantingToLearn_User=data)
        
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
        if not PersonalProfile.objects.filter(username = request.user.username).exists():
            return HttpResponse(status = 401)
        
        profile = PersonalProfile.objects.get(username = request.user.username)
        
        jsonDec = json.decoder.JSONDecoder()
        interest = jsonDec.decode(profile.interest)
        skill = jsonDec.decode(profile.skill)
        wantingToLearn = jsonDec.decode(profile.wantingToLearn)
        print(profile.name)
        
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
    
class getSuggestionsAPI(APIView):
    def get(self, request):
        jsonDec = json.decoder.JSONDecoder()
        jwts = jwt.decode(request.headers["Authorization"].split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        profile = PersonalProfile.objects.get(pk = jwts["user_id"])      
        match_list = []
        interest = jsonDec.decode(profile.interest)
        skill = jsonDec.decode(profile.skill)
        for i in interest:
            list_ = Hobby.match_hobby(Hobby, i)
            for j in list_:
                if not j in match_list:
                    match_list.append(j)
         
        for i in skill:                       
            list_ = Learn.match_learn(Learn, i)
            for j in list_:
                if not j in match_list:
                    match_list.append(j)
                    
        match_user = []
        
        for i in match_list:
            if i != request.user.username:
                match_user.append(PersonalProfile.decode(i))
        json_data = json.dumps(match_user)
        return HttpResponse(json_data, content_type="application/json", status = 200)
    