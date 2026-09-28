from rest_framework.routers import DefaultRouter
from .views import CarreraViewSet, MateriaViewSet, AlumnoViewSet, InscripcionViewSet, CardViewSet

router = DefaultRouter()
router.register(r'carreras', CarreraViewSet)
router.register(r'materias', MateriaViewSet)
router.register(r'alumnos', AlumnoViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'cards', CardViewSet)

urlpatterns = router.urls