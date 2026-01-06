# management/commands/test_whatsapp.py
from django.core.management.base import BaseCommand
from mariage.services.whatsapp_service import WhatsAppService
from django.conf import settings

class Command(BaseCommand):
    help = 'Teste la connexion à l\'API WhatsApp'
    
    def handle(self, *args, **options):
        self.stdout.write("🧪 Test de l'API WhatsApp WHAPI...")
        
        # Test 1: Message simple
        destinataire = settings.WHATSAPP_NUM
        test_message = "🔔 *TEST SYSTÈME MARIAGES*\n\nCe message confirme que le système d'envoi WhatsApp fonctionne correctement.\n\n✅ Prêt pour les envois automatiques!"
        
        self.stdout.write(f"📤 Envoi du message test...")
        succes, details = WhatsAppService.envoyer_message(destinataire, test_message)
        
        if succes:
            self.stdout.write(self.style.SUCCESS("✅ API WhatsApp fonctionnelle!"))
            self.stdout.write(f"📝 Réponse: {details}")
        else:
            self.stdout.write(self.style.ERROR("❌ Problème avec l'API WhatsApp"))
            self.stdout.write(f"🔧 Détails: {details}")
            
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Pour envoyer le planning: python manage.py envoyer_planning")
        self.stdout.write("Pour un test simple: python manage.py envoyer_planning --test")