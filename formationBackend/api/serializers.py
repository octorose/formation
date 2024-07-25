# serializers.py
from rest_framework import serializers, status
from rest_framework import serializers
from .models import Agent, Superviseur, Ligne, Personnel, Test, Contrat ,ResponsableEcoleFormation,Formateur ,Test, Contrat 
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Agent, Superviseur, Ligne, Personnel, RH, Module
from datetime import datetime
from django.core.files import File
from django.conf import settings
import logging


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data = super().validate(attrs)
                data.update({
                    'username': user.username,
                    'role': user.role  # Include the role in the response
                })
                return data

        raise serializers.ValidationError({'detail': 'Invalid credentials'})

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role  # Include the role in the token payload
        return token
    

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class PersonnelSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = Personnel
        fields = ['id', 'agent', 'etat']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'Personnel'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        personnel = Personnel.objects.create(agent=agent, **validated_data)
        return personnel

class SuperviseurSerializer(serializers.ModelSerializer):
     
    agent = AgentSerializer()
    ligne_id = serializers.PrimaryKeyRelatedField(queryset=Ligne.objects.all(), source='ligne')

    class Meta:
        model = Superviseur
        fields = ['id', 'agent', 'ligne_id']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'Superviseur'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        superviseur = Superviseur.objects.create(agent=agent, **validated_data)
        return superviseur

class RHSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = RH
        fields = ['id', 'agent', 'department']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'RH'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        rh = RH.objects.create(agent=agent, **validated_data)
        return rh


class PersonnelSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = Personnel
        fields = ['id', 'agent', 'etat']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'Personnel'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        personnel = Personnel.objects.create(agent=agent, **validated_data)
        return personnel
    def delete(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'Personnel'
        agent = AgentSerializer.delete(AgentSerializer(), validated_data=agent_data)
        personnel = Personnel.objects.delete(agent=agent, **validated_data)
        return personnel

class SuperviseurSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()
    ligne_id = serializers.PrimaryKeyRelatedField(queryset=Ligne.objects.all(), source='ligne')
    ligne_name = serializers.CharField(source='ligne.name', read_only=True)

    class Meta:
        model = Superviseur
        fields = ['id', 'agent', 'ligne_id', 'ligne_name']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'Superviseur'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        superviseur = Superviseur.objects.create(agent=agent, **validated_data)
        return superviseur

class DateTruncatedMonthField(serializers.ReadOnlyField):
    def to_representation(self, value):
        if isinstance(value, datetime):
            return value.date()
        return value

class PersonnelCountSerializer(serializers.Serializer):
    month = DateTruncatedMonthField()
    count = serializers.IntegerField()

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'description']
    
class ResponsableFormationEcoleSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = ResponsableEcoleFormation
        fields = ['id', 'school_name','agent']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'ResponsableEcoleFormation'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        responsable_formation_ecole = ResponsableEcoleFormation.objects.create(agent=agent, **validated_data)
        return responsable_formation_ecole


class FormateurSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = Formateur
        fields = ['id', 'isAffecteur','type', 'agent']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'Formateur'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        formateur = Formateur.objects.create(agent=agent, **validated_data)
        return formateur


class TestSerializer(serializers.ModelSerializer):
     responsables_ecole_formation = ResponsableFormationEcoleSerializer(many=True)
     formateurs = FormateurSerializer(many=True)
     personnel = PersonnelSerializer()

     class Meta:
         model = Test
         fields = ['id', 'type_test', 'date_test', 'responsables_ecole_formation', 'formateurs', 'note_test', 'personnel']

     def create(self, validated_data):
         responsables_data = validated_data.pop('responsables_ecole_formation')
         formateurs_data = validated_data.pop('formateurs')
         personnel_data = validated_data.pop('personnel')

         test = Test.objects.create(**validated_data)

         for responsable_data in responsables_data:
             responsable, created = ResponsableEcoleFormation.objects.get_or_create(**responsable_data)
             test.responsables_ecole_formation.add(responsable)

         for formateur_data in formateurs_data:
             formateur, created = Formateur.objects.get_or_create(**formateur_data)
             test.formateurs.add(formateur)

         personnel, created = Personnel.objects.get_or_create(**personnel_data)
         test.personnel = personnel
         test.save()

         return test

    

class ContratSerializer(serializers.ModelSerializer):
    #agent_id = AgentSerializer()

    class Meta:
        model = Contrat
        fields = ['id', 'agent_id', 'type_contrat', 'date_creation_contrat', 'duree_contrat']

    def create(self, validated_data):
        #agent_data = validated_data.pop('agent')

        # agent, created = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all(), source='agent', write_only=True)
        #agent_instance = Agent.objects.get(id=agent_data) 
        #validated_data['agent'] = agent_instance
        contrat = Contrat.objects.create(**validated_data)
        return contrat



