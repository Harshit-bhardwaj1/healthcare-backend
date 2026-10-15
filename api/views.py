
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'message': 'User registered successfully.',
            'user': UserSerializer(user).data
        }, status=201)


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(
            created_by=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return Doctor.objects.all().order_by('name')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().created_by_id != self.request.user.id:
            raise PermissionDenied(
                'You can only update doctors you created.'
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by_id != self.request.user.id:
            raise PermissionDenied(
                'You can only delete doctors you created.'
            )
        instance.delete()


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer

    http_method_names = [
        'get',
        'post',
        'put',
        'patch',
        'delete',
        'head',
        'options'
    ]

    def get_queryset(self):
        queryset = PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related('patient', 'doctor')

        patient_id = self.request.query_params.get('patient_id')

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class PatientMappingsView(APIView):
    """GET uses the path ID as patient_id; DELETE uses it as mapping ID."""

    def get(self, request, pk):
        patient = Patient.objects.filter(
            pk=pk,
            created_by=request.user
        ).first()

        if patient is None:
            raise NotFound('Patient not found.')

        mappings = PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related('patient', 'doctor')

        serializer = PatientDoctorMappingSerializer(
            mappings,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = PatientDoctorMapping.objects.filter(
            pk=pk,
            patient__created_by=request.user
        ).first()

        if mapping is None:
            raise NotFound('Mapping not found.')

        mapping.delete()
        return Response(status=204)