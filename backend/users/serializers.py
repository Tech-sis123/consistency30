from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, AccountabilityPartner, UserSettings

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'timezone')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            timezone=validated_data.get('timezone', 'UTC')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account disabled')
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Must include email and password')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    settings = UserSettingsSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 
            'phone', 'timezone', 'preferred_checkin_time',
            'onboarding_completed', 'push_notifications', 
            'email_notifications', 'share_progress', 'trust_score',
            'created_at', 'updated_at', 'profile', 'settings'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'trust_score')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'phone', 'timezone',
            'preferred_checkin_time', 'push_notifications',
            'email_notifications', 'share_progress'
        )

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

class OnboardingSerializer(serializers.Serializer):
    primary_goal = serializers.CharField(required=True)
    motivation_why = serializers.CharField(required=True)
    daily_time_commitment = serializers.IntegerField(required=True, min_value=1, max_value=480)
    has_tried_before = serializers.BooleanField(required=True)
    previous_attempts = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        user = self.context['request'].user
        profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        
        # Mark user as completed onboarding
        user.onboarding_completed = True
        user.save()
        
        return profile

class AccountabilityPartnerSerializer(serializers.ModelSerializer):
    partner_email = serializers.EmailField(source='partner.email', read_only=True)
    partner_username = serializers.CharField(source='partner.username', read_only=True)
    
    class Meta:
        model = AccountabilityPartner
        fields = ('id', 'partner', 'partner_email', 'partner_username', 'created_at')
        read_only_fields = ('id', 'created_at')

class AddPartnerSerializer(serializers.Serializer):
    partner_email = serializers.EmailField(required=True)
    
    def validate_partner_email(self, value):
        try:
            partner = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        
        if partner == self.context['request'].user:
            raise serializers.ValidationError("You cannot add yourself as a partner")
        
        # Check if partnership already exists
        if AccountabilityPartner.objects.filter(
            user=self.context['request'].user, 
            partner=partner
        ).exists():
            raise serializers.ValidationError("This user is already your accountability partner")
        
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        partner = User.objects.get(email=validated_data['partner_email'])
        
        partnership = AccountabilityPartner.objects.create(
            user=user,
            partner=partner
        )
        
        return partnership