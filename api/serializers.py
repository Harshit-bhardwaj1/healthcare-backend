from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(write_only=True, max_length=150)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        read_only_fields = ('id',)

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    def create(self, validated_data):
        name = validated_data.pop('name')
        email = validated_data['email']
        username = email
        user = User.objects.create_user(username=username, email=email, password=validated_data['password'], first_name=name)
        return user

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email')

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'gender', 'address', 'phone', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate_age(self, value):
        if value < 0 or value > 125:
            raise serializers.ValidationError('Age must be between 0 and 125.')
        return value

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialization', 'email', 'phone', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'assigned_by', 'created_at')
        read_only_fields = ('id', 'assigned_by', 'created_at')

    def validate(self, attrs):
        request = self.context['request']
        patient = attrs.get('patient', getattr(self.instance, 'patient', None))
        doctor = attrs.get('doctor', getattr(self.instance, 'doctor', None))
        if patient and patient.created_by_id != request.user.id:
            raise serializers.ValidationError({'patient': 'You can only assign doctors to your own patients.'})
        if patient and doctor and PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError('This doctor is already assigned to this patient.')
        return attrs
