from .models import Marriage, DocumentMariage, Hommes, Femmes
from rest_framework import serializers

        
class DocumentMariageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentMariage
        fields = '__all__'
        
class HommeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hommes
        fields = '__all__'

class FemmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Femmes
        fields = '__all__'
        
class MariageReadSerializer(serializers.HyperlinkedModelSerializer):
    DocumentMariage = DocumentMariageSerializer()
    Hommes = HommeSerializer()
    Femmes = FemmeSerializer()
    
    
    class Meta:
        model = Marriage
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'mariage-detail', 'lookup_field': 'id'}
        }

""" class MariageSerializer(serializers.HyperlinkedModelSerializer):
    DocumentMariage = serializers.HyperlinkedRelatedField(
        view_name='documentmariage-detail',
        queryset=DocumentMariage.objects.all(),
        lookup_field='id'
    )
    Hommes = serializers.HyperlinkedRelatedField(
        view_name='homme-detail',
        queryset=Hommes.objects.all(),
        lookup_field='id'
    )
    Femmes = serializers.HyperlinkedRelatedField(
        view_name='homme-detail',
        queryset=Femmes.objects.all(),
        lookup_field='id'
    )
    
    class Meta:
        model = Marriage
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'mariage-detail', 'lookup_field': 'id'}
        } """
        
class MariageSerializer(serializers.ModelSerializer):
    infos_homme = HommeSerializer()
    infos_femme = FemmeSerializer()
    id_dossier = DocumentMariageSerializer()

    class Meta:
        model = Marriage
        fields = '__all__'

    def create(self, validated_data):
        # Extraire les sous-données
        homme_data = validated_data.pop('infos_homme')
        femme_data = validated_data.pop('infos_femme')
        document_data = validated_data.pop('id_dossier')

        # Créer les sous-objets
        homme = Hommes.objects.create(**homme_data)
        femme = Femmes.objects.create(**femme_data)
        document = DocumentMariage.objects.create(**document_data)

        # Créer le mariage principal
        mariage = Marriage.objects.create(
            infos_homme=homme,
            infos_femme=femme,
            id_dossier=document,
            **validated_data
        )

        return mariage
    
    def update(self, instance, validated_data):
        # Mettre à jour les sous-objets
        homme_data = validated_data.pop('infos_homme', None)
        femme_data = validated_data.pop('infos_femme', None)
        document_data = validated_data.pop('id_dossier', None)

        if homme_data:
            for attr, value in homme_data.items():
                setattr(instance.infos_homme, attr, value)
            instance.infos_homme.save()

        if femme_data:
            for attr, value in femme_data.items():
                setattr(instance.infos_femme, attr, value)
            instance.infos_femme.save()

        if document_data:
            for attr, value in document_data.items():
                setattr(instance.id_dossier, attr, value)
            instance.id_dossier.save()

        # Mettre à jour le mariage principal
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance