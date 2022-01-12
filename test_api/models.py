from django.contrib.auth import default_app_config
from django.db import models
from django.db.models.base import Model
import json
from json import loads
from django.contrib.auth.hashers import make_password
import datetime
from datetime import timezone


# Create your models here.

class PersonalProfile(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=10)
    birthday = models.DateTimeField()
    job = models.CharField(max_length=32)
    interest = models.TextField(null=True)
    skill = models.TextField(null=True)
    wantingToLearn = models.TextField(null=True)
    
    
    def __str__(self):
        return "{}: {}".format(self.pk, self.username)
    
    def decode(user: str) -> str:
        if not  PersonalProfile.objects.filter(username=user).exists():
            return 
        profile = PersonalProfile.objects.get(username=user)
        jsonDec = json.decoder.JSONDecoder()
        interest = jsonDec.decode(profile.interest)
        skill = jsonDec.decode(profile.skill)
        wantingToLearn = jsonDec.decode(profile.wantingToLearn)
        name = make_password(profile.name)
        now = int(datetime.datetime.now(timezone.utc).strftime("%y"))
        birthday = int(profile.birthday.strftime("%y"))
        
        age = now - birthday
        json_data = {
            "id" : name,
            "name" : profile.name,
            "gender" : profile.gender,
            "age" : str(age),
            "job" : profile.job,
            "interest" : interest,
            "skill" : skill,
            "wantingToLearn" : wantingToLearn
        }
        return json_data
    
class Learn(models.Model):
    LabelName_Learn = models.CharField(max_length=30)
    wantingToLearn_User = models.TextField(null=True)
    
    def __str__(self):
        return self.LabelName_Learn

    def get_model_learn(self, name):
        return Learn.objects.get(LabelName_Learn = name)
    
    def match_learn(self, labels):
        label = self.get_model_learn(self, labels)
        user_list = self.decode_json(self, label)
        return user_list 
    
    def decode_json(self, model):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(model.wantingToLearn_User)   
     
    
    
    def __str__(self):
        return f"learn: {self.LabelName_Learn}"
        
    
class Skill(models.Model):
    LabelName_Skill = models.CharField(max_length=30)
    Skill_User = models.TextField(null=True) 
      
    def get_model_skill(self, name):
        return Learn.objects.get(LabelName_Skill = name)
      
    def match_skill(self, labels):
        label = self.get_model_skill(self, labels)
        user_list = self.decode_json(self, label)
        return user_list       
    
    def decode_json(self, model):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(model.Skill_User)
    
    def __str__(self) -> str:
        return f"skill: {self.LabelName_Skill}"
    
    
class Hobby(models.Model):
    LabelName = models.CharField(max_length=30)
    InterestUser = models.TextField(null=True)
       
    #LabelName存每個標籤的名字
    #InterestUser存有這個hobby的username(list)
    
    
    def match_hobby(self, labels):
        label = self.get_model_hobby(self, labels)
        user_list = self.decode_json(self, label)
        return user_list 
    

    def get_model_hobby(self, name):
        return Hobby.objects.get(LabelName = name)
    

    def decode_json(self, model):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(model.InterestUser)
    

   
    
    def __str__(self):
        return self.LabelName
    