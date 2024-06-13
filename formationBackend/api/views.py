# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status, generics
from .serializers import SuperviseurSerializer, PersonnelSerializer, RHSerializer, PersonnelCountSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .models import Agent, RH, ResponsableFormation, ResponsableEcoleFormation, Formateur, Superviseur, Personnel, Ligne
from django.contrib.auth.hashers import make_password
from django.db.models.functions import TruncMonth, Coalesce
from django.http import JsonResponse



class PersonnelSumByEtatView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Aggregate sum of Personnel count by etat
            queryset = Personnel.objects.values('etat').annotate(sum_personnel=Count('id'))

            # Format response data
            response_data = [{'etat': entry['etat'], 'sum_personnel': entry['sum_personnel']} for entry in queryset]

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class PersonnelCountByMonthAPIView(APIView):
 def get(self, request):
        try:
            # Annotate queryset by month and count Personnel
            queryset = Personnel.objects.annotate(
                month=TruncMonth('agent__date_joined')
            ).values(
                'month'
            ).annotate(
                count=Coalesce(Count('id'), 0)
            ).order_by('month')

            # Format month names as abbreviated (Jan, Feb, etc.)
            formatted_data = []
            for entry in queryset:
                month_name = entry['month'].strftime('%b')
                formatted_data.append({
                    'month': month_name,
                    'count': entry['count']
                })

            # Ensure all months are included with default count 0 if not present
            all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            result_data = []
            for month in all_months:
                month_data = next((item for item in formatted_data if item['month'] == month), {'month': month, 'count': 0})
                result_data.append(month_data)

            return JsonResponse(result_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
    
class CreateRHView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = RHSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'RH created successfully',
                'rh_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class PersonnelListView(generics.ListAPIView):
    # permission_classes = [AllowAny]
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer