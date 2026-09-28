from django.contrib import admin
from .models import Carrera, Materia, Alumno, Inscripcion

admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Alumno)
admin.site.register(Inscripcion)

# Register your models here.
