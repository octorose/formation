import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Agent, Superviseur, Ligne
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_supervisor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            email = data['email']
            password = data['password']
            prenom = data['prenom']
            nom = data['nom']
            date_naissance = data['date_naissance']
            addresse = data['addresse']
            cin = data['cin']
            numerotel = data['numerotel']
            ligne_id = data['ligne_id']


            agent = Agent.objects.create(
                username=username,
                email=email,
                password=password,
                prenom=prenom,
                nom=nom,
                date_naissance=date_naissance,
                addresse=addresse,
                cin=cin,
                numerotel=numerotel,
                role='Superviseur'
            )

            ligne = Ligne.objects.get(id=ligne_id)
            superviseur = Superviseur.objects.create(agent=agent, ligne=ligne)

            return JsonResponse({
                'status': 'success',
                'message': 'Supervisor created successfully',
                'supervisor_id': superviseur.id
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }, status=405)
