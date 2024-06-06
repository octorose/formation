# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import SuperviseurSerializer, PersonnelSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .models import Agent, RH, ResponsableFormation, ResponsableEcoleFormation, Formateur, Superviseur, Personnel, Ligne
from django.contrib.auth.hashers import make_password

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            role = data.get('role')

            agent_data = data.get('agent')
            username = agent_data.get('username')
            email = agent_data.get('email')
            password = agent_data.get('password')
            prenom = agent_data.get('prenom')
            nom = agent_data.get('nom')
            date_naissance = agent_data.get('date_naissance')
            addresse = agent_data.get('addresse')
            cin = agent_data.get('cin')
            numerotel = agent_data.get('numerotel')

            # Create the agent
            agent = Agent.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                prenom=prenom,
                nom=nom,
                date_naissance=date_naissance,
                addresse=addresse,
                cin=cin,
                numerotel=numerotel,
                role=role
            )

            # Create role-specific instance
            if role == 'Superviseur':
                ligne_id = data.get('ligne_id')
                ligne = Ligne.objects.get(id=ligne_id)
                Superviseur.objects.create(agent=agent, ligne=ligne)
            elif role == 'RH':
                department = data.get('department')
                RH.objects.create(agent=agent, department=department)
            elif role == 'ResponsableFormation':
                domain = data.get('domain')
                ResponsableFormation.objects.create(agent=agent, domain=domain)
            elif role == 'ResponsableEcoleFormation':
                school_name = data.get('school_name')
                ResponsableEcoleFormation.objects.create(agent=agent, school_name=school_name)
            elif role == 'Formateur':
                isAffecteur = data.get('isAffecteur', False)
                Formateur.objects.create(agent=agent, isAffecteur=isAffecteur)
            elif role == 'Personnel':
                etat = data.get('etat', 'Candidate')
                Personnel.objects.create(agent=agent, etat=etat)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid role specified'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': 'success',
                'message': f'{role} created successfully',
                'user_id': agent.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  
class CreateSupervisorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SuperviseurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Supervisor created successfully',
                'supervisor_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class CreatePersonnelView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Personnel created successfully',
                'personnel_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)