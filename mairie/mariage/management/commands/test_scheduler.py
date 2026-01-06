# management/commands/test_scheduler.py
from django.core.management.base import BaseCommand
import schedule
import time
from datetime import datetime
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Teste le scheduler avec un envoi immédiat'
    
    def handle(self, *args, **options):
        self.stdout.write("🧪 TEST DU SCHEDULER")
        self.stdout.write("=" * 50)
        
        # Planifier un test dans 10 secondes
        schedule.every(10).seconds.do(self.envoyer_test)
        
        # Planifier un test dans 1 minute
        schedule.every(1).minutes.do(self.log_test)
        
        self.stdout.write("📋 Tests planifiés:")
        self.stdout.write("   • Test WhatsApp dans 10 secondes")
        self.stdout.write("   • Log de test dans 1 minute")
        self.stdout.write("")
        self.stdout.write("⏳ En attente des exécutions...")
        self.stdout.write("   (Appuyez sur Ctrl+C pour arrêter)")
        self.stdout.write("=" * 50)
        
        compteur = 0
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                compteur += 1
                
                # Afficher un point toutes les 5 secondes
                if compteur % 5 == 0:
                    self.stdout.write(".", ending="")
                    self.stdout.flush()
                    
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n\n🛑 Test terminé"))
    
    def envoyer_test(self):
        """Envoie un message de test"""
        self.stdout.write(self.style.SUCCESS("\n\n✅ EXÉCUTION DU TEST WHATSAPP"))
        try:
            call_command('envoyer_planning', '--test')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur: {str(e)}"))
    
    def log_test(self):
        """Log un message de test"""
        heure = datetime.now().strftime("%H:%M:%S")
        self.stdout.write(self.style.NOTICE(f"\n[{heure}] 🧪 Test minute exécuté"))