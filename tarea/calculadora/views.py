from django.shortcuts import render
from django.http import HttpResponse
from json import loads,dumps
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from random import randrange
import requests

from .models import Reto, Jugadores, Usuario, partidas
from .serializers import RetoSerializer, JugadorSerializer, UsuarioSerializer, PartidasSerializer
from rest_framework import viewsets


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PartidasViewSet(viewsets.ModelViewSet):
    queryset = partidas.objects.all()
    serializer_class = PartidasSerializer

class Fraccion:
    def __init__(self, num, den):
        self.num = num
        self.den = den
    def toJSON(self):
        return dumps(self, default=lambda o:o.__dict__, sort_keys=False, indent=4)

# Create your views here.
def nuvea():
    return 0

def index(request):
    return render(request, 'index.html')

def procesamiento(request):
    nombre = request.POST['nombre']
    nombre = nombre.title()
    return render(request, 'proceso.html', {'name':nombre})

def lista(request):
    jugadores = Reto.objects.all() #select * from Reto 
    return render(request, 'datos.html',{'lista_jugadores':jugadores})

def score():
    return 0

@csrf_exempt
def suma(request):
    print("Ingrese 2 fracciones para suma")
    body_unicode = request.body.decode('utf-8')
    body=loads(body_unicode)
    num1 = body['numerador1']
    den1 = body['denominador1']

    num2 = body['numerador2']
    den2 = body['denominador2']

    if(den1 == den2):
        num_r =num1+num2
        den_r =den1
    else: 
        num_r = (num1*den2)+(num2*den1)
        den_r = den1*den2
    
    resultado = Fraccion(num_r,den_r)
    resultado_json = resultado.toJSON()
    return HttpResponse(resultado_json,content_type ="text/json-comment-filtered")

@csrf_exempt
def resta(request):
    print("Ingrese 2 fracciones para resta")
    body_unicode = request.body.decode('utf-8')
    body=loads(body_unicode)
    num1 = body['numerador1']
    den1 = body['denominador1']

    num2 = body['numerador2']
    den2 = body['denominador2']

    if(den1 == den2):
        num_r =num1-num2
        den_r =den1
    else: 
        num_r = (num1*den2)-(num2*den1)
        den_r = den1*den2
    
    resultado = Fraccion(num_r,den_r)
    resultado_json = resultado.toJSON()
    return HttpResponse(resultado_json,content_type ="text/json-comment-filtered")

@csrf_exempt
def multiplicacion(request):
    print("Ingrese 2 fracciones para multi")
    body_unicode = request.body.decode('utf-8')
    body=loads(body_unicode)
    num1 = body['numerador1']
    den1 = body['denominador1']

    num2 = body['numerador2']
    den2 = body['denominador2']

    num_r =num1*num2
    den_r = den1*den2
    
    resultado = Fraccion(num_r,den_r)
    resultado_json = resultado.toJSON()
    return HttpResponse(resultado_json,content_type ="text/json-comment-filtered")

@csrf_exempt
def division(request):
    print("Ingrese 2 fracciones para div")
    body_unicode = request.body.decode('utf-8')
    body=loads(body_unicode)
    num1 = body['numerador1']
    den1 = body['denominador1']

    num2 = body['numerador2']
    den2 = body['denominador2']

    num_r =num1*den2
    den_r = num2*den1
    
    resultado = Fraccion(num_r,den_r)
    resultado_json = resultado.toJSON()
    return HttpResponse(resultado_json,content_type ="text/json-comment-filtered")

@csrf_exempt
def usuarios(request):
    if (request.method == 'GET'):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM usuarios")
        resultado = res.fetchall()
        data = []
        keys = [column[0] for column in cur.description]
        for values in resultado:
            obj = {}
            for i in range(len(keys)):
                obj[keys[i]] = values[i]
            data.append(obj)
        context = {"data": data}
        return render(request, "datos.html", context)
    elif (request.method == 'POST'):
        return (usuarios_p(request))
    elif (request.method == "DELETE"):
        return (usuarios_d(request))

@csrf_exempt
def usuarios_p(request):
    body = request.body.decode('UTF-8')
    eljson = loads(body)
    grado = eljson['grado']
    grupo = eljson['grupo']
    num_lista = eljson['num_lista']
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    res = cur.execute("INSERT INTO usuarios(grupo, grado, num_lista) VALUES (?, ?, ?)", (grupo, grado, num_lista))
    con.commit()
    return HttpResponse('Ok')

@csrf_exempt
def usuarios_d(request):
    body = request.body.decode('UTF-8')
    eljson = loads(body)
    id_usuario = eljson['id_usuario']
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    res = cur.execute("DELETE FROM usuarios WHERE id_usuario = ?", (str(id_usuario)))
    con.commit()
    return HttpResponse('Ok usuario ' + str(id_usuario) + ' borrado')

@csrf_exempt
def usuarios_u(request):
    body = request.body.decode('UTF-8')
    eljson = loads(body)
    id_usuario = eljson['id_usuario']
    grado = eljson['grado']
    grupo = eljson['grupo']
    num_lista = eljson['num_lista']
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    res = cur.execute("UPDATE usuarios SET grupo = ?, grado = ?, num_lista = ? WHERE id_usuario = ?", (grupo, grado, num_lista, str(id_usuario)))
    con.commit()
    return HttpResponse('Ok usuario ' + str(id_usuario) + ' actualizado')

#entrada: {"id_usuario": "usuario", "pass": "contrasenia"}
#salida: {"estatus": True}
@csrf_exempt
def valida_usuario(request):
    body = request.body.decode('UTF-8')
    eljson = loads(body)
    usuario = eljson['id_usuario']
    contrasenia = eljson['pass']
    print(usuario+contrasenia)
    #con = sqlite3.connect("db.sqlite3")
    #cur = con.cursor()
    #res = cur.execute("SELECT * FROM usuarios WHERE id_usuario=? AND pass=?", (str(usuario), str(contrasenia)))
    return HttpResponse({"estatus":True})

@csrf_exempt
def login(request):
    body = request.body.decode('UTF-8')
    eljson = loads(body)
    grado = eljson['grado']
    grupo = eljson['grupo']
    num_lista = eljson['num_lista']  
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()   
    cur.execute(f"SELECT grado from usuarios WHERE grado = '{grado}' AND grupo = '{grupo}' AND num_lista = '{num_lista}'")

    if not cur.fetchone():
        return HttpResponse("Usuario invalido, intentalo de nuevo")
    else:
        return HttpResponse("Bienvenid@!")

@csrf_exempt
def login2(request):
    return render (request, 'login.html')

def grafica(request):
    '''
    data = [
          ['Jugador', 'Minutos Jugados'],
          ['Ian', 1000],
          ['Héctor', 1170], 
          ['Alan', 660],
          ['Manuel', 1030]
        ]
    '''
    data = []
    data.append(['Jugador', 'Minutos Jugados'])
    resultados = Reto.objects.all() #select * from reto; #Aqui debe de ir un query 
    titulo = 'Actividad Creación de end point y gráfica'
    titulo_formato = dumps(titulo)
    subtitulo= 'Total de minutos por jugador'
    subtitulo_formato = dumps(subtitulo)
    if len(resultados)>0:
        for registro in resultados:
            nombre = registro.nombre
            minutos = registro.minutos_jugados
            data.append([nombre,minutos])
        data_formato = dumps(data) #formatear los datos en string para JSON
        elJSON = {'losDatos':data_formato,'titulo':titulo_formato,'subtitulo':subtitulo_formato}
        return render(request,'barras.html',elJSON)
    else:
        return HttpResponse("<h1>No hay registros a mostrar</h1>")


#Ejemplo de como funciona 

# def grafica(request):
#     #h_var : The title for horizontal axis
#     h_var = 'X'

#     #v_var : The title for horizontal axis
#     v_var = 'Y'

#     #data : A list of list which will ultimated be used 
#     # to populate the Google chart.
#     data = [[h_var,v_var]]
#     """
#     An example of how the data object looks like in the end: 
#         [
#           ['Age', 'Weight'],
#           [ 8,      12],
#           [ 4,      5.5],
#           [ 11,     14],
#           [ 4,      5],
#           [ 3,      3.5],
#           [ 6.5,    7]
#         ]
#     The first list will consists of the title of horizontal and vertical axis,
#     and the subsequent list will contain coordinates of the points to be plotted on
#     the google chart
#     """

#     #The below for loop is responsible for appending list of two random values  
#     # to data object
#     for i in range(0,11):
#         data.append([randrange(101),randrange(101)])

#     #h_var_JSON : JSON string corresponding to  h_var
#     #json.dumps converts Python objects to JSON strings
#     h_var_JSON = dumps(h_var)

#     #v_var_JSON : JSON string corresponding to  v_var
#     v_var_JSON = dumps(v_var)

#     #modified_data : JSON string corresponding to  data
#     modified_data = dumps(data)

#     #Finally all JSON strings are supplied to the charts.html using the 
#     # dictiory shown below so that they can be displayed on the home screen
#     return render(request,"charts.html",{'values':modified_data,\
#         'h_title':h_var_JSON,'v_title':v_var_JSON})

#Ruta para el proceso del login (invocación del servicio de verificación de usuario)

@csrf_exempt
def procesologin(request):
    usuario = request.POST['usuario']
    contrasenia = request.POST['password']
    #invoca el servicio de validación de usuario
    url = "http://127.0.0.1:8000/valida_usuario"
    header = {
    "Content-Type":"application/json"
    }
    payload = {   
    "id_usuario" :usuario,
    "pass" : contrasenia
    }
    result = requests.post(url,  data= dumps(payload), headers=header)
    if result.status_code == 200:
        return HttpResponse('Abrir página principal')
    return HttpResponse('Abrir página de credenciales inválidas')



#rest

class RetoViewSet(viewsets.ModelViewSet):
    queryset = Reto.objects.all()
    serializer_class = RetoSerializer

class JugadoresViewSet(viewsets.ModelViewSet):
    queryset = Jugadores.objects.all() #select * from Calculadora.Jugadores
    serializer_class = JugadorSerializer