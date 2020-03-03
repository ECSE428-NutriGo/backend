from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from profile.models import Profile

class UserSerializer(UserDetailsSerializer):

    protein_target = serializers.IntegerField(source="profile.protein_target", default=0)
    carb_target = serializers.IntegerField(source="profile.carb_target", default=0)
    fat_target = serializers.IntegerField(source="profile.fat_target", default=0)

    current_weight = serializers.IntegerField(source="profile.current_weight", default=0)
    target_weight = serializers.IntegerField(source="profile.target_weight", default=0)
    age = serializers.IntegerField(source="profile.age", default=0)
    hours_activity = serializers.IntegerField(source="profile.hours_activity", default=0)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('protein_target','carb_target','fat_target','current_weight','target_weight','age', 'hours_activity')
        extra_kwargs = {'username': {'required': False}}

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        protein_target = profile_data.get('protein_target')
        carb_target = profile_data.get('carb_target')
        fat_target = profile_data.get('fat_target')

        current_weight = profile_data.get('current_weight')
        target_weight = profile_data.get('target_weight')
        age = profile_data.get('age')
        hours_activity = profile_data.get('hours_activity')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.profile
        if profile_data and protein_target and protein_target >= 0:
            profile.protein_target = protein_target

        if profile_data and carb_target and carb_target >= 0:
            profile.carb_target = carb_target

        if profile_data and fat_target and fat_target >= 0:
            profile.fat_target = fat_target

        if profile_data and current_weight and current_weight >= 0:
            profile.current_weight = current_weight

        if profile_data and target_weight and target_weight >= 0:
            profile.target_weight = target_weight

        if profile_data and age and age >= 0:
            profile.age = age

        if profile_data and hours_activity and hours_activity >= 0:
            profile.hours_activity = hours_activity
        
        profile.save()
        
        return instance