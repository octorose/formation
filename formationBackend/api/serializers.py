# serializers.py
from rest_framework import serializers
from .models import Agent, Superviseur, Ligne, Personnel,ResponsableEcoleFormation,Formateur
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Agent

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data = super().validate(attrs)
                data.update({'username': user.username})
                return data

        raise serializers.ValidationError({'detail': 'Invalid credentials'})

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

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
    
    def update(self, instance, validated_data):
        agent_data = validated_data.pop('agent')
        instance.agent.username = agent_data.get('username', instance.agent.username)
        instance.agent.email = agent_data.get('email', instance.agent.email)
        instance.agent.prenom = agent_data.get('prenom', instance.agent.prenom)
        instance.agent.nom = agent_data.get('nom', instance.agent.nom)
        instance.agent.date_naissance = agent_data.get('date_naissance', instance.agent.date_naissance)
        instance.agent.addresse = agent_data.get('addresse', instance.agent.addresse)
        instance.agent.cin = agent_data.get('cin', instance.agent.cin)
        instance.agent.numerotel = agent_data.get('numerotel', instance.agent.numerotel)
        instance.agent.save()

        instance.school_name = validated_data.get('school_name', instance.school_name)
        instance.save()
        return instance

class FormateurSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = Formateur
        fields = ['id', 'agent', 'isAffecteur']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent')
        agent_data['role'] = 'Formateur'
        agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
        formateur = Formateur.objects.create(agent=agent, **validated_data)
        return formateur
    def update(self, instance, validated_data):
        agent_data = validated_data.pop('agent')
        instance.agent.username = agent_data.get('username', instance.agent.username)
        instance.agent.email = agent_data.get('email', instance.agent.email)
        instance.agent.prenom = agent_data.get('prenom', instance.agent.prenom)
        instance.agent.nom = agent_data.get('nom', instance.agent.nom)
        instance.agent.date_naissance = agent_data.get('date_naissance', instance.agent.date_naissance)
        instance.agent.addresse = agent_data.get('addresse', instance.agent.addresse)
        instance.agent.cin = agent_data.get('cin', instance.agent.cin)
        instance.agent.numerotel = agent_data.get('numerotel', instance.agent.numerotel)
        instance.agent.save()

        instance.isAffecteur = validated_data.get('isAffecteur', instance.isAffecteur)
        instance.save()
        return instance