from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from profile.models import Profile

class UserSerializer(UserDetailsSerializer):

    protein_target = serializers.CharField(source="profile.protein_target", default=-1)
    carb_target = serializers.CharField(source="profile.carb_target", default=-1)
    fat_target = serializers.CharField(source="profile.fat_target", default=-1)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('protein_target','carb_target','fat_target')
        extra_kwargs = {'username': {'required': False}}

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        protein_target = int(profile_data.get('protein_target'))
        carb_target = int(profile_data.get('carb_target'))
        fat_target = int(profile_data.get('fat_target'))

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.profile
        if profile_data and protein_target and protein_target >= 0:
            profile.protein_target = protein_target

        if profile_data and carb_target and carb_target >= 0:
            profile.carb_target = carb_target

        if profile_data and fat_target and fat_target >= 0:
            profile.fat_target = fat_target
        
        profile.save()
        
        return instance