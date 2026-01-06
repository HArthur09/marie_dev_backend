# management/commands/envoyer_planning.py
from django.core.management.base import BaseCommand
from django.conf import settings
from mariage.services.whatsapp_service import WhatsAppService, PlanningGenerator

class Command(BaseCommand):
    help = 'Envoie le planning hebdomadaire des mariages au maire via WhatsApp'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Envoie un message de test simple'
        )
        parser.add_argument(
            '--message',
            type=str,
            help='Message personnalisé à envoyer'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(f"📱 WhatsApp Service - Destinataire: {settings.MAIRE_NOM}")
        self.stdout.write(f"📞 Numéro: {settings.WHATSAPP_NUM}\n")
        
        if options['test']:
            # Mode test: envoi d'un message simple
            message = "🔔 *TEST NOTIFICATION*\n\nCeci est un test de l\'envoi WhatsApp depuis le système de gestion des mariages.\n\n✅ Système opérationnel!"
            self.stdout.write("🧪 Mode test activé")
            
        elif options['message']:
            # Mode message personnalisé
            message = options['message']
            self.stdout.write(f"✉️  Message personnalisé: {message[:50]}...")
            
        else:
            # Mode normal: génération du planning
            self.stdout.write("📅 Génération du planning hebdomadaire...")
            message = PlanningGenerator.generer_planning_hebdomadaire()
            
        
        # Affichage du message (preview)
        self.stdout.write("\n" + "="*50)
        self.stdout.write("📝 MESSAGE À ENVOYER:")
        self.stdout.write("="*50)
        self.stdout.write(message[:500] + ("..." if len(message) > 500 else ""))
        self.stdout.write("="*50)
        
        
        # Envoi du message
        destinataire = settings.WHATSAPP_NUM
        self.stdout.write("\n📤 Envoi en cours...")
        succes, details = WhatsAppService.envoyer_message(destinataire, message)
        
        # Résultat
        self.stdout.write("\n" + "="*50)
        if succes:
            self.stdout.write(self.style.SUCCESS("✅ MESSAGE ENVOYÉ AVEC SUCCÈS!"))
        else:
            self.stdout.write(self.style.ERROR("❌ ÉCHEC DE L'ENVOI"))
        self.stdout.write(f"📋 Détails: {details}")
        self.stdout.write("="*50)
        
        # Information pour l'automatisation
        self.stdout.write("\n💡 POUR L'AUTOMATISATION:")
        self.stdout.write(f"   Commande test: python manage.py envoyer_planning --test")
        self.stdout.write(f"   Commande force: python manage.py envoyer_planning --force")