from django.contrib import admin
from .models import Reto, Jugadores, Usuario, partidas

# Register your models here.
admin.site.register(Usuario)
admin.site.register(partidas)

admin.site.register(Reto)
admin.site.register(Jugadores)
