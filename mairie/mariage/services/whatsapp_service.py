# services/whapi_service.py
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class WhatsAppService:
    
    def envoyer_message(destinataire, message):
        
        url = "https://gate.whapi.cloud/messages/text"
        #message = "Hello World! This is a test ✅"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {settings.WHATSAPP_API}"
        }
        
        payload = {
            "to": destinataire,
            "body": message,
            "typing_time": 0
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return True, "Message envoyé avec succès"
            else:
                error_msg = f"Erreur {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', error_msg)
                except:
                    error_msg = response.text
                return False, error_msg
                
        except requests.exceptions.ConnectionError:
            return False, "Erreur de connexion à l'API WhatsApp"
        except Exception as e:
            return False, f"Erreur inattendue: {str(e)}"
        
        

# Utilisation simple:
# service = WhatsAppService()

class PlanningGenerator:
    """Générateur de messages de planning"""
    
    @staticmethod
    def generer_planning_hebdomadaire():
        """
        Génère le planning des mariages de la semaine
        
        Returns:
            str: Message formaté pour WhatsApp
        """
        from mariage.models import Marriage  # Import ici pour éviter les imports circulaires
        
        aujourd_hui = timezone.now().date()
        debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())  # Lundi
        fin_semaine = debut_semaine + timedelta(days=6)  # Dimanche
        
        # Récupérer les mariages de la semaine
        mariages = Marriage.objects.filter(
            date_celebration__range=[debut_semaine, fin_semaine],
            status='en_attente'
        ).select_related('id_dossier').order_by('date_celebration', 'heure_celebration')
        
        # Construction du message
        lignes = [
            f"*🗓️ PLANNING HEBDOMADAIRE DES MARIAGES*",
            f"*Semaine du {debut_semaine.strftime('%d/%m')} au {fin_semaine.strftime('%d/%m/%Y')}*",
            f"",
            f"*📊 RÉCAPITULATIF : {len(mariages)} MARIAGE(S)*",
            f"",
        ]
        
        if not mariages:
            lignes.append("Aucun mariage prévu cette semaine. ✅")
        else:
            # Grouper par jour
            jours = {}
            for mariage in mariages:
                jour = mariage.date_celebration.strftime('%A %d/%m')
                if jour not in jours:
                    jours[jour] = []
                jours[jour].append(mariage)
            
            # Ajouter les mariages par jour
            for jour, mariages_jour in sorted(jours.items()):
                lignes.append(f"*📅 {jour.upper()}*")
                lignes.append("─" * 25)
                
                for i, mariage in enumerate(mariages_jour, 1):
                    lignes.extend([
                        f"*{i}. {mariage.infos_homme.nom} {mariage.infos_homme.prenom}. et .{mariage.infos_femme.nom} {mariage.infos_femme.prenom}*",
                        f"⏰ *Heure:* {mariage.heure_celebration.strftime('%H:%M')}",
                        f"📍 *Lieu:* {mariage.lieu_celebration}",
                        f"📞 *Époux:* {mariage.infos_homme.telephone_epoux}",
                        f"📞 *Épouse:* {mariage.infos_femme.telephone_epouse}",
                        f""
                    ])
        
        lignes.extend([
            "─" * 25,
            "*Bonne semaine de célébrations !* 🎉",
            f"*Envoyé le {aujourd_hui.strftime('%d/%m/%Y à %H:%M')}*"
        ])
        
        return "\n".join(lignes)