
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, PatientDoctorMappingViewSet, PatientMappingsView

router = DefaultRouter()
router.register('patients', PatientViewSet, basename='patient')
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('mappings', PatientDoctorMappingViewSet, basename='mapping')

urlpatterns = [
    path('', include(router.urls)),
    path('patients/<int:pk>/mappings/', PatientMappingsView.as_view(), name='patient-mappings-detail'),
]
