# serializers.py
from rest_framework import serializers, status
from rest_framework import serializers
from .models import Agent, Superviseur, Ligne, Personnel, Polyvalence, Test, Contrat ,ResponsableEcoleFormation,Formateur ,Test, Contrat ,Poste,ResponsableFormation
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Agent, Superviseur, Ligne, Personnel, RH, Module
from datetime import datetime
from django.core.files import File
from django.conf import settings
from .utils import validate_email



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
                    'role': user.role,
                    'user_id': user.id,
                    'role_specific_id': self.get_role_specific_id(user)  # Include the role-specific ID in the response
                })
                return data

        raise serializers.ValidationError({'detail': 'Invalid credentials'})

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        token['user_id'] = user.id
        token['role_specific_id'] = cls.get_role_specific_id(user)  # Include the role-specific ID in the token payload
        return token

    @staticmethod
    def get_role_specific_id(user):
        if user.role == 'RH':
            return RH.objects.get(agent=user).id
        elif user.role == 'ResponsableFormation':
            return ResponsableFormation.objects.get(agent=user).id
        elif user.role == 'ResponsableEcoleFormation':
            return ResponsableEcoleFormation.objects.get(agent=user).id
        elif user.role == 'Formateur':
            return Formateur.objects.get(agent=user).id
        elif user.role == 'Superviseur':
            return Superviseur.objects.get(agent=user).id
        elif user.role == 'Personnel':
            return Personnel.objects.get(agent=user).id
        return None
    

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        email = data.get('email')
        if email:
            is_valid, message = validate_email(email)
            if not is_valid:
                raise serializers.ValidationError({'email': False, 'message': message})

        return data

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
class LigneSerializer(serializers.ModelSerializer):
    superviseur_nom = serializers.CharField(source='superviseur.agent.nom', read_only=True)
    superviseur_prenom = serializers.CharField(source='superviseur.agent.prenom', read_only=True)

    class Meta:
        model = Ligne
        fields = ['id', 'name', 'superviseur_nom', 'superviseur_prenom', 'superviseur']

    def validate(self, data):
        if data.get('superviseur') is None:
            raise serializers.ValidationError("A supervisor must be assigned to the ligne.")
        return data
    
class SuperviseurSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(required=False)  # Allow partial updates without requiring password
    lignes = LigneSerializer(many=True, read_only=True)
    lignes_ids = serializers.PrimaryKeyRelatedField(queryset=Ligne.objects.all(), many=True, write_only=True)

    class Meta:
        model = Superviseur
        fields = ['id', 'agent', 'lignes', 'lignes_ids']

    def create(self, validated_data):
        agent_data = validated_data.pop('agent', None)
        lignes_ids = validated_data.pop('lignes_ids', [])

        if agent_data:
            agent_data['role'] = 'Superviseur'
            agent = AgentSerializer.create(AgentSerializer(), validated_data=agent_data)
            validated_data['agent'] = agent

        superviseur = Superviseur.objects.create(**validated_data)

        if lignes_ids:
            superviseur.lignes.set(lignes_ids)

        return superviseur
    def update(self, instance, validated_data):
        agent_data = validated_data.pop('agent', {})  # Handle optional agent data

        # Update agent instance if data provided
        if agent_data:
            agent_instance = instance.agent
            agent_serializer = AgentSerializer(agent_instance, data=agent_data, partial=True)
            if agent_serializer.is_valid():
                agent_serializer.save()
            else:
                raise serializers.ValidationError(agent_serializer.errors)

        lignes_ids = validated_data.pop('lignes_ids', [])

        # Update Superviseur instance
        instance.lignes.set(lignes_ids)  # Update many-to-many relation
        return super().update(instance, validated_data)



    def update(self, instance, validated_data):
        agent_data = validated_data.pop('agent', {})  # Handle optional agent data

        # Update agent instance if data provided
        if agent_data:
            agent_instance = instance.agent
            agent_serializer = AgentSerializer(agent_instance, data=agent_data, partial=True)
            if agent_serializer.is_valid():
                agent_serializer.save()
            else:
                raise serializers.ValidationError(agent_serializer.errors)

        lignes_ids = validated_data.pop('lignes_ids', [])

        # Update Superviseur instance
        instance.lignes.set(lignes_ids)  # Update many-to-many relation
        return super().update(instance, validated_data)


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
    
class PosteSerializer(serializers.ModelSerializer):
    lignes = LigneSerializer(many=True, read_only=True)
    lignes_ids = serializers.PrimaryKeyRelatedField(queryset=Ligne.objects.all(), many=True, write_only=True)

    class Meta:
        model = Poste
        fields = ['id', 'name', 'type', 'lignes', 'lignes_ids']

    def create(self, validated_data):
        # Pop lignes_ids from validated_data
        lignes_ids = validated_data.pop('lignes_ids', [])
        # Create the Poste instance without lignes_ids
        poste = Poste.objects.create(**validated_data)
        # Set the lignes relationship
        poste.lignes.set(lignes_ids)
        return poste

class PersonnelSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()
    poste = PosteSerializer(required=False, allow_null=True)
    polyvalence = serializers.SerializerMethodField()

    class Meta:
        model = Personnel
        fields = ['id', 'agent', 'etat', 'ligne', 'poste', 'polyvalence']

    def get_polyvalence(self, obj):
        try:
            polyvalence = Polyvalence.objects.get(personnel=obj, poste=obj.poste, ligne=obj.ligne)
            return PolyvalenceSerializer(polyvalence).data
        except Polyvalence.DoesNotExist:
            return None

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
    
class PersonnelUpdateEtatSerializer(serializers.ModelSerializer):
    ligne = serializers.PrimaryKeyRelatedField(queryset=Ligne.objects.all())
    poste = serializers.PrimaryKeyRelatedField(queryset=Poste.objects.all())

    class Meta:
        model = Personnel
        fields = ['ligne', 'poste']


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
        fields = ['id','agent']

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
        fields = ['id', 'isAffecteur','Type', 'agent']

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
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())

    class Meta:
        model = Contrat
        fields = ['id', 'agent', 'type_contrat', 'date_creation_contrat', 'duree_contrat']

    def create(self, validated_data):
        return Contrat.objects.create(**validated_data)
class ContratDisplaySerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = Contrat
        fields = ['id', 'agent', 'type_contrat', 'date_creation_contrat', 'duree_contrat']






class PolyvalenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polyvalence
        fields = '__all__'

    def validate(self, data):
        personnel = data['personnel']
        supervisor = data['supervisor']
        
        # Check if personnel is an operator
        if personnel.etat != Personnel.OPERATOR_STATE:
            raise serializers.ValidationError("Personnel must be in 'Operateur' state to be rated.")
        
        # Check if personnel belongs to the supervisor's line
        if personnel.ligne not in supervisor.lignes.all():
            raise serializers.ValidationError("Personnel must belong to the supervisor's line.")
        
        return data
class PolyvalenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polyvalence
        fields = ['score', 'comments']

