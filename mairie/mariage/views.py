from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
import threading
from django.db import connection
from django.core.management import call_command
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Marriage, DocumentMariage, Hommes, Femmes
from .serializer import MariageSerializer, DocumentMariageSerializer, HommeSerializer, FemmeSerializer, MariageReadSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta


# Create your views here.
class MariageViewSet(viewsets.ModelViewSet):
    queryset = Marriage.objects.all()
    serializer_class = MariageSerializer
    lookup_field='id'
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'date_celebration', 'nom_maire', 'infos_homme__nom', 'infos_femme__nom']
    ordering_fields = ['date_celebration', 'heure_celebration']
    
    def perform_destroy(self, instance):
        # Supprimer les documents, homme et femme associés
        homme = instance.infos_homme
        femme = instance.infos_femme
        documents = instance.id_dossier
        
        instance.delete()
        if documents:
            documents.delete()
        if homme:
            homme.delete()
        if femme:
            femme.delete()

        

class DocumentMariageViewSet(viewsets.ModelViewSet):
    queryset = DocumentMariage.objects.all()
    serializer_class = DocumentMariageSerializer
    lookup_field='id'

class HommeViewSet(viewsets.ModelViewSet):
    queryset = Hommes.objects.all()
    serializer_class = HommeSerializer
    lookup_field='id'

class FemmeViewSet(viewsets.ModelViewSet):
    queryset = Femmes.objects.all()
    serializer_class = FemmeSerializer
    lookup_field='id'
    
class test(viewsets.ModelViewSet):
    aujourd_hui = timezone.now().date()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())  # Lundi
    fin_semaine = debut_semaine + timedelta(days=6)  # Dimanche
    queryset = mariages = Marriage.objects.filter(
            date_celebration__range=[debut_semaine, fin_semaine],
            status='en_attente'
        ).select_related('id_dossier').order_by('date_celebration', 'heure_celebration')
    serializer_class = MariageSerializer
    lookup_field='id'
    
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def envoyer_planning_manuel(request):
    """
    Endpoint API pour déclencher manuellement l'envoi du planning
    """
    try:
        # Option 1: Exécuter la commande management directement
        from io import StringIO
        from django.core.management import call_command
        
        # Créer un thread pour ne pas bloquer la requête
        def executer_envoi():
            try:
                # Fermer la connexion DB du thread principal
                connection.close()
                
                # Exécuter la commande
                output = StringIO()
                call_command('envoyer_planning', stdout=output)
                result = output.getvalue()
                
                # Log le résultat
                print(f"✅ Envoi manuel déclenché: {result[:100]}...")
                
            except Exception as e:
                print(f"❌ Erreur lors de l'envoi manuel: {str(e)}")
        
        # Démarrer dans un thread séparé
        thread = threading.Thread(target=executer_envoi)
        thread.start()
        
        # Répondre immédiatement
        return Response({
            'status': 'success',
            'message': 'Envoi du planning déclenché avec succès',
            'details': 'Le planning est en cours d\'envoi au maire via WhatsApp'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Erreur lors du déclenchement de l\'envoi',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def statut_envoi(request):
    """
    Vérifie le statut du dernier envoi
    """
    try:
        # Vous pouvez ajouter une logique pour vérifier le dernier envoi
        # Pour l'instant, retourner un statut basique
        return Response({
            'status': 'ready',
            'message': 'Système prêt pour l\'envoi',
            'last_sent': None,  # À implémenter si vous stockez l'historique
            'next_scheduled': 'Lundi 08:00'  # Prochain envoi automatique
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
