# serializers.py
from rest_framework import serializers
from .models import Agent, Superviseur, Ligne, Personnel
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
