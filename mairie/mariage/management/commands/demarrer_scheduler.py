# management/commands/demarrer_scheduler.py
from django.core.management.base import BaseCommand
import schedule
import time
import threading
from datetime import datetime
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Démarre le planificateur de tâches pour les notifications automatiques'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 DÉMARRAGE DU PLANIFICATEUR"))
        self.stdout.write("=" * 60)
        
        # 1. Afficher les informations de configuration
        self.afficher_configuration()
        
        # 2. Planifier les tâches
        self.planifier_taches()
        
        # 3. Démarrer le scheduler dans un thread séparé
        self.demarrer_scheduler_thread()
        
        # 4. Garder la commande active
        self.maintenir_commande_active()
    
    def afficher_configuration(self):
        """Affiche la configuration des tâches planifiées"""
        self.stdout.write("📋 TÂCHES PLANIFIÉES:")
        self.stdout.write("   └─ 📅 Envoi planning: TOUS LES LUNDIS À 8H00")
        self.stdout.write("")
        self.stdout.write("👤 DESTINATAIRE:")
        self.stdout.write(f"   └─ 👨‍💼 Maire: Monsieur DUPONT")
        self.stdout.write(f"   └─ 📞 Téléphone: 33612345678")
        self.stdout.write("")
    
    def planifier_taches(self):
        """Définit les tâches à exécuter selon un planning"""
        # Tâche principale: Envoi hebdomadaire le lundi à 8h
        schedule.every(1).monday.at("08:00").do(self.executer_envoi_planning)
        
        # Tâche de vérification: Toutes les heures (pour debug)
        schedule.every().hour.do(self.verifier_statut_systeme)
        
        # Tâche de test: Tous les jours à 9h (optionnel)
        # schedule.every().day.at("09:00").do(self.test_quotidien)
        
        self.stdout.write("✅ Tâches correctement planifiées")
        self.stdout.write("")
    
    def executer_envoi_planning(self):
        """Exécute la commande d'envoi du planning"""
        heure_actuelle = datetime.now().strftime("%H:%M:%S")
        self.stdout.write(f"[{heure_actuelle}] 📤 Déclenchement automatique: ENVOI DU PLANNING")
        
        try:
            # Appelle votre commande existante 'envoyer_planning'
            call_command('envoyer_planning')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erreur lors de l'envoi: {str(e)}"))
    
    def verifier_statut_systeme(self):
        """Vérifie que le système fonctionne (pour debug)"""
        heure_actuelle = datetime.now().strftime("%H:%M:%S")
        self.stdout.write(f"[{heure_actuelle}] ✅ Système actif - Vérification horaire")
    
    def test_quotidien(self):
        """Tâche de test quotidienne (optionnelle)"""
        heure_actuelle = datetime.now().strftime("%H:%M:%S")
        self.stdout.write(f"[{heure_actuelle}] 🧪 Exécution du test quotidien")
        # call_command('test_whatsapp')
    
    def demarrer_scheduler_thread(self):
        """Démarre le scheduler dans un thread séparé"""
        def run_scheduler():
            self.stdout.write("🔄 Démarrage du scheduler en arrière-plan...")
            self.stdout.write("   (Appuyez sur Ctrl+C pour arrêter)")
            self.stdout.write("=" * 60)
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Vérifie toutes les minutes
        
        # Crée et démarre le thread
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        self.stdout.write(self.style.SUCCESS("✅ Thread du scheduler démarré"))
    
    def maintenir_commande_active(self):
        """Garder la commande en cours d'exécution"""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n\n🛑 Arrêt du planificateur demandé"))
            self.stdout.write("👋 Fermeture en cours...")