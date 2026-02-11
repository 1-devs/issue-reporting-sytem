from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =  ['id', 'email', 'full_name', 'phone_number', 'role']
        read_only_fields = ['role']


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
class LeadercreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'role', 'assigned_location_id', 'password']

    def validate(self, data):
        request = self.context.get('request')
        creator = request.user
        new_role = data.get('role')

        # Ensure the creator is authenticated (not a Guest)
        if creator.is_anonymous:
             # Citizens are self-registered, so they don't have a supervisor
            if new_role == 'CITIZEN':
                return data
            raise serializers.ValidationError("Only logged-in leaders can create other leaders.")

        #  Hierarchy Validation Logic
        if new_role == 'SECTOR_LEADER' and creator.role != 'DISTRICT_LEADER':
            raise serializers.ValidationError("Only District Leaders can create Sector Leaders.")
        
        if new_role == 'CELL_LEADER' and creator.role != 'SECTOR_LEADER':
            raise serializers.ValidationError("Only Sector Leaders can create Cell Leaders.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        creator = request.user

        # Automatically assign supervisor if the creator is a Leader
        if not creator.is_anonymous and creator.role in ['DISTRICT_LEADER', 'SECTOR_LEADER']:
            validated_data['supervisor'] = creator

        password = validated_data.pop('password') #
        user = CustomUser(**validated_data)
        user.set_password(password) # 
        user.save()
        return user
    

class signupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data    

    def create(self, validated_data):
        validated_data.pop('confirm_password') # Remove confirm_password from validated_data
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user    
