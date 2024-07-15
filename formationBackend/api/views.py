# views.py
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Poste
from .serializers import PosteSerializer
from django.db.models import Count
from rest_framework import status, generics
from .serializers import SuperviseurSerializer,PolyvalenceUpdateSerializer, PolyvalenceSerializer,  PersonnelSerializer, RHSerializer, PersonnelCountSerializer, AgentSerializer, ModuleSerializer,ResponsableFormationEcoleSerializer,FormateurSerializer, LigneSerializer,PosteSerializer,PersonnelUpdateEtatSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .models import Agent, RH, Polyvalence, ResponsableFormation, ResponsableEcoleFormation, Superviseur, Personnel, Ligne,Formateur,Poste
from django.contrib.auth.hashers import make_password
from django.db.models.functions import TruncMonth, Coalesce
from django.http import JsonResponse
from .models import Module
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Test, Contrat
from .serializers import TestSerializer, ContratSerializer

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
            queryset = Personnel.objects.annotate(
                month=TruncMonth('agent__date_joined')
            ).values(
                'month'
            ).annotate(
                count=Coalesce(Count('id'), 0)
            ).order_by('month')
            formatted_data = []
            for entry in queryset:
                month_name = entry['month'].strftime('%b')
                formatted_data.append({
                    'month': month_name,
                    'count': entry['count']
                })
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


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Superviseur, Agent, Ligne
from .serializers import SuperviseurSerializer, AgentSerializer


class CreateSupervisorView(APIView):


    def post(self, request):
        serializer = SuperviseurSerializer(data=request.data)
        if serializer.is_valid():
            superviseur = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Supervisor created successfully',
                'supervisor_id': superviseur.id 
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        

class SupervisorLines(generics.ListAPIView):
    serializer_class = LigneSerializer

    def get_queryset(self):
        supervisor_id = self.kwargs['supervisor_id']
        return Ligne.objects.filter(superviseurs__id=supervisor_id)

class UpdateSuperviseurView(APIView):
    def put(self, request, pk, format=None):
        superviseur = get_object_or_404(Superviseur, pk=pk)
        serializer = SuperviseurSerializer(superviseur, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        data = request.data
        etat = data.get('etat')
        ligne = data.get('ligne')
        poste = data.get('poste')

        if etat not in ['En Formation', 'Candidate', 'Candidat' ,'Operateur']:
            return Response({
                'status': 'error',
                'message': 'Invalid etat value. Must be "En Formation" or "Candidate" or "Operateur".'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = PersonnelSerializer(data=data)
        if serializer.is_valid():
            if etat == 'Operateur' and  ligne is None and poste is None:
                return Response({
                    'status': 'error',
                    'message': 'Ligne and Poste is required for Operateur.'
                }, status=status.HTTP_400_BAD_REQUEST)
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


    def delete(self, request, pk, format=None):
        try:
            personnel = get_object_or_404(Personnel, pk=pk)
            agent = personnel.agent
            personnel.delete()
            agent.delete()
            return Response({'message': 'Personnel and associated Agent deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
class LineOperators(APIView):
    def get(self, request, line_id):
        line = get_object_or_404(Ligne, pk=line_id)
        operators = Personnel.objects.filter(ligne=line)
        serializer = PersonnelSerializer(operators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdatePersonnelEtatToOperatorView(APIView):
    def patch(self, request, *args, **kwargs):
        personnel_id = self.kwargs.get('id')
        try:
            personnel = Personnel.objects.get(id=personnel_id)
        except Personnel.DoesNotExist:
            return Response({'error': 'Personnel not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonnelUpdateEtatSerializer(personnel, data=request.data, partial=True)
        if serializer.is_valid():
            personnel.etat = Personnel.OPERATOR_STATE
            personnel.ligne = serializer.validated_data.get('ligne')
            personnel.poste = serializer.validated_data.get('poste')
            serializer.save()
            return Response({'message': 'Personnel updated to Operateur'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonnelView(APIView):

    
    def put(self, request, pk, format=None):
        data = request.data
        etat = data.get('etat')
        ligne = data.get('ligne')

        if etat not in ['En Formation', 'Candidate', 'Candidat', 'Operateur']:
            return Response({
                'status': 'error',
                'message': 'Invalid etat value. Must be "En Formation" or "Candidate".'
            }, status=status.HTTP_400_BAD_REQUEST)
        if etat == 'Operateur' and  ligne is None:
                return Response({
                    'status': 'error',
                    'message': 'Ligne is required for Operateur.'
                }, status=status.HTTP_400_BAD_REQUEST)
        try:
            personnel = get_object_or_404(Personnel, pk=pk)
            agent = personnel.agent

            # Extract agent data and personnel data from the request
            agent_data = request.data.get('agent', {})
            personnel_data = request.data.copy()  # Use copy to avoid mutating original request data
            personnel_data.pop('agent', None)  # Remove agent data from personnel data

            # Separate many-to-many fields from other fields for Agent
            agent_m2m_fields = {}
            for field in Agent._meta.get_fields():
                if field.many_to_many:
                    agent_m2m_fields[field.name] = agent_data.pop(field.name, [])

            # Separate many-to-many fields from other fields for Personnel
            personnel_m2m_fields = {}
            for field in Personnel._meta.get_fields():
                if field.many_to_many:
                    personnel_m2m_fields[field.name] = personnel_data.pop(field.name, [])

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
    serializer_class = PersonnelSerializer

    def get_queryset(self):
        return Personnel.objects.exclude(etat=Personnel.OPERATOR_STATE)

class PersonnelOperatorListView(generics.ListAPIView):
    serializer_class = PersonnelSerializer

    def get_queryset(self):
        return Personnel.objects.filter(etat=Personnel.OPERATOR_STATE)
    
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


#///////////////////////////////////////////////////////////////////////////////////////////:
class ResponsableFormationListView(generics.ListAPIView):
    queryset = ResponsableEcoleFormation.objects.all()
    serializer_class = ResponsableFormationEcoleSerializer
    
class CreateResponsableFormationEcoleView(APIView):
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
class DeleteResponsableFormationEcoleView(APIView):
    def delete(self, request, pk, format=None):
        try:
            responsable_formation = get_object_or_404(ResponsableEcoleFormation, pk=pk)
            agent = responsable_formation.agent
            responsable_formation.delete()
            agent.delete()
            return Response({'message': 'ResponsableFormation deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class UpdateResponsableEcoleFormationView(APIView):
    def put(self, request, pk, format=None):
        try:
            responsable_formation = get_object_or_404(ResponsableEcoleFormation, pk=pk)
            agent = responsable_formation.agent
            agent_data = request.data.get('agent', {})
            responsable_data = request.data
            responsable_data.pop('agent', None) 
            agent_m2m_fields = {field.name: agent_data.pop(field.name, []) for field in Agent._meta.get_fields() if field.many_to_many}
            responsable_m2m_fields = {field.name: responsable_data.pop(field.name, []) for field in ResponsableEcoleFormation._meta.get_fields() if field.many_to_many}

            agent_serializer = AgentSerializer(agent, data=agent_data, partial=True)
            if agent_serializer.is_valid():
                agent_serializer.save()
                for field_name, value in agent_m2m_fields.items():
                    field = getattr(agent, field_name)
                    field.set(value)
            else:
                return Response({'agent_errors': agent_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            responsable_serializer = ResponsableFormationEcoleSerializer(responsable_formation, data=responsable_data, partial=True)
            if responsable_serializer.is_valid():
                responsable_serializer.save()
                for field_name, value in responsable_m2m_fields.items():
                    field = getattr(responsable_formation, field_name)
                    field.set(value)
            else:
                return Response({'responsable_errors': responsable_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'responsable_formation': responsable_serializer.data,
                'agent': agent_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ResponsableFormationEcoleSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            responsables = ResponsableEcoleFormation.objects.filter(
                Q(agent__nom__icontains=query) |
                Q(agent__prenom__icontains=query) |
                Q(agent__email__icontains=query)
            )
            serializer = ResponsableFormationEcoleSerializer(responsables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

 #///////////////////////////////////////////////////////////////////////////////////   

class ListFormateurView(APIView):

     def get(self, request):
        formateurs = Formateur.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of supervisors per page
        result_page = paginator.paginate_queryset(formateurs, request)
        serializer = FormateurSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CreateFormateurView(APIView):

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

class SearchFormateurView(APIView):

    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            formateurs = Formateur.objects.filter(
                Q(nom__icontains=query) |
                Q(prenom__icontains=query) |
                Q(email__icontains=query)
            )
            serializer = FormateurSerializer(formateurs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

class DeleteFormateurView(APIView):

    def delete(self, request, pk, format=None):
        try:
            formateur = get_object_or_404(Formateur, pk=pk)
            agent = formateur.agent
            formateur.delete()
            agent.delete()
            return Response({'message': 'Formateur deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateFormateurView(APIView):

    def put(self, request, pk, format=None):
        try:
            formateur = get_object_or_404(Formateur, pk=pk)
            agent = formateur.agent
            agent_data = request.data.get('agent', {})
            formateur_data = request.data
            formateur_data.pop('agent', None)  # Remove agent data from formateur data

            agent_m2m_fields = {field.name: agent_data.pop(field.name, []) for field in Agent._meta.get_fields() if field.many_to_many}
            formateur_m2m_fields = {field.name: formateur_data.pop(field.name, []) for field in Formateur._meta.get_fields() if field.many_to_many}

            agent_serializer = AgentSerializer(agent, data=agent_data, partial=True)
            if agent_serializer.is_valid():
                agent_serializer.save()
                for field_name, value in agent_m2m_fields.items():
                    field = getattr(agent, field_name)
                    field.set(value)
            else:
                return Response({'agent_errors': agent_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            formateur_serializer = FormateurSerializer(formateur, data=formateur_data, partial=True)
            if formateur_serializer.is_valid():
                formateur_serializer.save()
                for field_name, value in formateur_m2m_fields.items():
                    field = getattr(formateur, field_name)
                    field.set(value)
            else:
                return Response({'formateur_errors': formateur_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'formateur': formateur_serializer.data,
                'agent': agent_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListTestView(generics.ListAPIView):

    queryset = Test.objects.all()
    serializer_class = TestSerializer

class CreateTestView(APIView):


    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Test created successfully',
                'test_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class SearchTestView(APIView):


    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            tests = Test.objects.filter(
                type_test__icontains=query
            ) | Test.objects.filter(
                date_test__icontains=query
            )
            serializer = TestSerializer(tests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

class DeleteTestView(APIView):


    def delete(self, request, pk, format=None):
        try:
            test = get_object_or_404(Test, pk=pk)
            test.delete()
            return Response({'message': 'Test deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateTestView(APIView):


    def put(self, request, pk, format=None):
        try:
            test = get_object_or_404(Test, pk=pk)
            serializer = TestSerializer(test, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Views for Contrat
class ListContratView(generics.ListAPIView):

    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer

class CreateContratView(APIView):


    def post(self, request):
        serializer = ContratSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Contrat created successfully',
                'contrat_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class SearchContratView(APIView):


    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            contrats = Contrat.objects.filter(
                type_contrat__icontains=query
            ) | Contrat.objects.filter(
                date_creation_contrat__icontains=query
            )
            serializer = ContratSerializer(contrats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

class DeleteContratView(APIView):


    def delete(self, request, pk, format=None):
        try:
            contrat = get_object_or_404(Contrat, pk=pk)
            contrat.delete()
            return Response({'message': 'Contrat deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateContratView(APIView):


    def put(self, request, pk, format=None):
        try:
            contrat = get_object_or_404(Contrat, pk=pk)
            serializer = ContratSerializer(contrat, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class LigneListView(generics.ListAPIView):
    queryset = Ligne.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 3
    serializer_class = LigneSerializer


class CreateLigneView(APIView):
    def post(self, request):
        serializer = LigneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Ligne created successfully',
                'ligne_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
class LigneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ligne.objects.all()
    serializer_class = LigneSerializer
 
#////////////////////////////////////////////////////////////////////////////   
class PosteCreateView(APIView):
    def post(self, request):
        serializer = PosteSerializer(data=request.data)
        if serializer.is_valid():
            poste = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Poste created successfully',
                'poste_id': poste.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

        
class UpdatePosteView(APIView):
    def put(self, request, pk, format=None):
        poste = get_object_or_404(Poste, pk=pk)
        serializer = PosteSerializer(poste, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PosteListView(APIView):
    def get(self, request):
        postes = Poste.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of postes per page
        result_page = paginator.paginate_queryset(postes, request)
        serializer = PosteSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class PosteSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            postes = Poste.objects.filter(
                Q(name__icontains=query)
            )
            serializer = PosteSerializer(postes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

class PosteDeleteView(APIView):
    def delete(self, request, pk, format=None):
        try:
            poste = get_object_or_404(Poste, pk=pk)
            poste.delete()
            return Response({'message': 'Poste deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#/////////////////////////////////////////////////////////////////////////:

class PolyvalenceViewSet(generics.CreateAPIView):
    queryset = Polyvalence.objects.all()
    serializer_class = PolyvalenceSerializer

class PolyvalenceUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Polyvalence.objects.all()
    serializer_class = PolyvalenceUpdateSerializer

class UnratedOperatorsByLineView(APIView):
    def get(self, request, ligne_id):
        try:
            ligne = Ligne.objects.get(id=ligne_id)
        except Ligne.DoesNotExist:
            return Response({'error': 'Ligne not found'}, status=status.HTTP_404_NOT_FOUND)
    
        operators_in_line = Personnel.objects.filter(ligne=ligne, etat=Personnel.OPERATOR_STATE)
        
        # Most important part of the view
        unrated_operators = []
        for operator in operators_in_line:
            if not Polyvalence.objects.filter(personnel=operator, poste=operator.poste, ligne=ligne).exists():
                unrated_operators.append(operator)
        ########################################

        serializer = PersonnelSerializer(unrated_operators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatedOperatorsByLineView(APIView):
    def get(self, request, ligne_id):
        try:
            ligne = Ligne.objects.get(id=ligne_id)
        except Ligne.DoesNotExist:
            return Response({'error': 'Ligne not found'}, status=status.HTTP_404_NOT_FOUND)
        
        operators_in_line = Personnel.objects.filter(ligne=ligne, etat=Personnel.OPERATOR_STATE)
        
        rated_operators = []
        for operator in operators_in_line:
            if Polyvalence.objects.filter(personnel=operator, poste=operator.poste, ligne=ligne).exists():
                rated_operators.append(operator)
        
        serializer = PersonnelSerializer(rated_operators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)