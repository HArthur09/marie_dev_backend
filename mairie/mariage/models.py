from django.db import models
import uuid

# Create your models here.

class Marriage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_dossier = models.ForeignKey('DocumentMariage', on_delete=models.CASCADE)
    date_celebration = models.DateField()
    heure_celebration = models.TimeField()
    lieu_celebration = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[
        ('en_attente', 'En attente'),
        ('terminé', 'terminé'),
        ('annule', 'Annulé'),
    ], default='en_attente')
    nom_maire = models.CharField(max_length=100)
    infos_homme = models.ForeignKey('Hommes', on_delete=models.CASCADE, related_name='marié', default=None)
    infos_femme = models.ForeignKey('Femmes', on_delete=models.CASCADE, related_name='mariée', default=None)
    fait_à = models.CharField(max_length=100)
    fait_le = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'Mariage {self.date_celebration} - {self.status}'
    
class DocumentMariage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photocopie_CNI = models.BooleanField(default=False)
    photocopie_acte_naissance = models.BooleanField(default=False)
    certificat_celibat_mairie = models.BooleanField(default=False)
    certificat_celibat_autorité = models.BooleanField(default=False)
    acte_décès_précédent_conjoint = models.BooleanField(default=False, null=True, blank=True)
    photocopie_ancien_acte_mariage = models.BooleanField(default=False, null=True, blank=True)
    attestation_divorce = models.BooleanField(default=False, null=True, blank=True)
    acte_mariages_polygames = models.BooleanField(default=False, null=True, blank=True)
    certificat_capacité_mariage_francais = models.BooleanField(default=False, null=True, blank=True)
    autorisation_mariage_militaire = models.BooleanField(default=False, null=True, blank=True)
    dix_démi_photos_têtes_collées = models.BooleanField(default=False)
    acte_naissance_enfants_couple = models.BooleanField(default=False, null=True, blank=True)
    contrat_mariage = models.BooleanField(default=False, null=True, blank=True)
    cni_chef_famille = models.BooleanField(default=False)
    cni_temoins = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Documents pour le mariage {self.id}'
    

class Hommes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    age = models.IntegerField()
    sexe = models.CharField(max_length=10, choices=[
        ('masculin', 'Masculin'),
        ('féminin', 'Féminin'),
    ])
    lieu_naissance = models.CharField(max_length=255)
    Arrondoissement_naissance = models.CharField(max_length=100)
    Departement_naissance = models.CharField(max_length=100)
    nationalité = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    domicile = models.CharField(max_length=255)
    nom_père = models.CharField(max_length=100)
    nom_mère = models.CharField(max_length=100)
    chef_famille_marié = models.CharField(max_length=100)
    nom_temoin_epoux = models.CharField(max_length=100)
    telephone_epoux = models.CharField(max_length=15)
    
class Femmes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    age = models.IntegerField()
    sexe = models.CharField(max_length=10, choices=[
        ('masculin', 'Masculin'),
        ('féminin', 'Féminin'),
    ])
    lieu_naissance = models.CharField(max_length=255)
    Arrondoissement_naissance = models.CharField(max_length=100)
    Departement_naissance = models.CharField(max_length=100)
    nationalité = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    domicile = models.CharField(max_length=255)
    nom_père = models.CharField(max_length=100)
    nom_mère = models.CharField(max_length=100)
    chef_famille_mariée = models.CharField(max_length=100)
    nom_temoin_epouse = models.CharField(max_length=100)
    telephone_epouse = models.CharField(max_length=15)
    
    def __str__(self):
        return f'{self.prenom} {self.nom}'

class WhatsappNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Marriage, on_delete=models.CASCADE)
    nom_destinataire = models.CharField(max_length=15)
    telephone = models.CharField(max_length=15)
    status = models.CharField(max_length=50, choices=[
        ('envoyé', 'Envoyé'),
        ('échoué', 'Échoué'),
        ('en_attente', 'En attente'),
    ], default='en_attente')
    date_envoi = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Notification to {self.destinataire} - {self.status}'
    
    

    
    