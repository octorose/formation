# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from django.db.models import Count
from rest_framework import status, generics
from .serializers import SuperviseurSerializer, PersonnelSerializer, RHSerializer, PersonnelCountSerializer, AgentSerializer, ModuleSerializer,ResponsableFormationEcoleSerializer,FormateurSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .models import Agent, RH, ResponsableFormation, ResponsableEcoleFormation, Formateur, Superviseur, Personnel, Ligne
from django.contrib.auth.hashers import make_password
from django.db.models.functions import TruncMonth, Coalesce
from django.http import JsonResponse
from django.http.response import Http404
import random
from django.core.files import File
from rest_framework.generics import ListAPIView
from django.conf import settings
from .models import Module
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404

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
class SupervisorListView(APIView):
    def get(self, request):
        supervisors = Superviseur.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of supervisors per page
        result_page = paginator.paginate_queryset(supervisors, request)
        serializer = SuperviseurSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class SupervisorSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            superviseurs = Superviseur.objects.filter(
                Q(agent__nom__icontains=query) |
                Q(agent__prenom__icontains=query) |
                Q(agent__cin__icontains=query) |
                Q(agent__email__icontains=query) |
                Q(agent__numerotel__icontains=query) |
                Q(ligne__name__icontains=query)
            )
            serializer = SuperviseurSerializer(superviseurs, many=True)
         
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)
class SuperviseurDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk, format=None):
        try:
            superviseur = get_object_or_404(Superviseur, pk=pk)
            superviseur.delete()
            agent = superviseur.agent
            agent.delete()
            return Response({'message': 'Supervisor and associated Agent deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CreatePersonnelView(APIView):


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

class DeletePersonnelView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk, format=None):
        try:
            personnel = get_object_or_404(Personnel, pk=pk)
            agent = personnel.agent
            personnel.delete()
            agent.delete()
            return Response({'message': 'Personnel and associated Agent deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        

class UpdatePersonnelView(APIView):
    permission_classes = [AllowAny]
    print("update")
    def put(self, request, pk, format=None):
        try:
            personnel = get_object_or_404(Personnel, pk=pk)
            agent = personnel.agent

            # Extract agent data and personnel data from the request
            agent_data = request.data.get('agent', {})
            personnel_data = request.data
            personnel_data.pop('agent', None)  # Remove agent data from personnel data

            # Separate many-to-many fields from other fields
            agent_m2m_fields = {field.name: agent_data.pop(field.name, []) for field in Agent._meta.get_fields() if field.many_to_many}
            personnel_m2m_fields = {field.name: personnel_data.pop(field.name, []) for field in Personnel._meta.get_fields() if field.many_to_many}

            # Update Agent
            agent_serializer = AgentSerializer(agent, data=agent_data, partial=True)
            if agent_serializer.is_valid():
                agent_serializer.save()
                # Update many-to-many fields for Agent
                for field_name, value in agent_m2m_fields.items():
                    field = getattr(agent, field_name)
                    field.set(value)
            else:
                return Response({'agent_errors': agent_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            # Update Personnel
            personnel_serializer = PersonnelSerializer(personnel, data=personnel_data, partial=True)
            if personnel_serializer.is_valid():
                personnel_serializer.save()
                # Update many-to-many fields for Personnel
                for field_name, value in personnel_m2m_fields.items():
                    field = getattr(personnel, field_name)
                    field.set(value)
            else:
                return Response({'personnel_errors': personnel_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'personnel': personnel_serializer.data,
                'agent': agent_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class PersonnelSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            personnel = Personnel.objects.filter(
                agent__role='Personnel',
                agent__nom__icontains=query
            ) | Personnel.objects.filter(
                agent__role='Personnel',
                agent__prenom__icontains=query
            ) | Personnel.objects.filter(
                agent__role='Personnel',
                agent__cin__icontains=query
            ) | Personnel.objects.filter(
                agent__role='Personnel',
                agent__email__icontains=query
            ) | Personnel.objects.filter(
                agent__role='Personnel',
                agent__numerotel__icontains=query
            ) | Personnel.objects.filter(
                agent__role='Personnel',
                etat__icontains=query
            )
            serializer = PersonnelSerializer(personnel, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)
class CreateRHView(APIView):

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
    
class ModuleCreateView(APIView):
    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModuleListView(APIView):
    def get(self, request):
        modules = Module.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 3  # Number of modules per page
        result_page = paginator.paginate_queryset(modules, request)
        serializer = ModuleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateResponsableFormationEcoleView(APIView):
    permission_classes = [AllowAny]
   
    def post(self, request):
        serializer = ResponsableFormationEcoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'ResponsableFormation created successfully',
                'responsableformation_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# WHY IS THIS CLASS HAS GET AND DELETE METHODS SINCE IT SAYS EDIT RESPONSABLE FORMATION ECOLE VIEW?
class EditResponsableFormationEcoleView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return ResponsableEcoleFormation.objects.get(pk=pk)
        except ResponsableEcoleFormation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        responsable_formation = self.get_object(pk)
        serializer = ResponsableFormationEcoleSerializer(responsable_formation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        responsable_formation = self.get_object(pk)
        serializer = ResponsableFormationEcoleSerializer(responsable_formation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        responsable_formation = self.get_object(pk)
        responsable_formation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CreateFormateurView(APIView):
    permission_classes = [AllowAny]
   
    def post(self, request):
        serializer = FormateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Formateur created successfully',
                'formateur_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class EditFormateurView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Formateur.objects.get(pk=pk)
        except Formateur.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        formateur = self.get_object(pk)
        serializer = FormateurSerializer(formateur)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        formateur = self.get_object(pk)
        serializer = FormateurSerializer(formateur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        formateur = self.get_object(pk)
        serializer = FormateurSerializer()
        serializer.delete(formateur)
        return Response(status=status.HTTP_204_NO_CONTENT)

