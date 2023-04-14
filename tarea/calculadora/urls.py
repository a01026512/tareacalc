from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reto', views.RetoViewSet)
router.register(r'jugador', views.JugadoresViewSet)
router.register(r'usuario', views.UsuarioViewSet)
router.register(r'partidas', views.PartidasViewSet)

urlpatterns = [
    path('api',include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', views.index, name='index'),
    path('procesamiento', views.procesamiento, name='procesamiento'),
    path('lista', views.lista, name='lista'),
    path('score', views.score, name='score'),

    path('suma', views.suma, name='suma'),
    path('resta', views.resta, name='resta'),
    path('multiplicacion', views.multiplicacion, name='multiplicacion'),
    path('division', views.division, name='division'),

    path('usuarios', views.usuarios, name='usuarios'),
    path('usuarios_p', views.usuarios_p, name='usuarios_p'),
    path('usuarios_d', views.usuarios_d, name='usuarios_d'),

    path('usuarios_u', views.usuarios_u, name='usuarios_u'),

    path('login', views.login, name='login'),
    path('procesologin', views.procesologin, name='procesologin'),
    path('valida_usuario', views.valida_usuario, name='valida_usuario'),

    path('grafica', views.grafica, name='grafica'),
    # path('grafica', views.grafica, name='grafica'),
    path('login2', views.login2, name='login2'),

]
