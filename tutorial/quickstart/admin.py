from django.contrib import admin
from .models import Card, Carrera, Materia, Alumno, Inscripcion

admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Alumno)
admin.site.register(Inscripcion)
admin.site.register(Card)

# Register your models here.
