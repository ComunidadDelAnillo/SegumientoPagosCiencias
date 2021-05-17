import numpy as np
import pandas as pd

####
####EJEMPLO

# NECESITAMOS DEL FORMULARIO
#año, 
#semestre
#cursos impartidos: horas y nombramiento
#PEPASIG
#antigüedad
#impartió curso el semestre anterior?

semestre_anio = 2021
semestre_periodo = 1
tiene_pepasig = False
antiguedad = 4
entidad = 'Ciencias'
impartio_anterior = True
lista_cursos = [(1,3)] #lista de tuplas (nombramiento, horas)


## TABLAS:
nombramiento = {
    0: 'Ninguno',
    1: 'Profesor de Asignatura A',
    2: 'Profesor de Asignatura B',
    3: 'Ayudante de Profesor A',
    4: 'Ayudante de Profesor B'
}

sueldo = {
    2020: {
        1: 400.24, # 
        2: 455.04,
        3: 304.08,
        4: 338.88
    },
    2021: { # ???
        1: 420.06,
        2: 477.56,
        3: 319.14,
        4: 355.66
    }
    # Futuro: 2022, 2023, etc... :-p
}

## Vale despensa mensual (quincenas pares)
vale_despensa = {
    2020: 1255.0,
    2021: 1443.0
}


tab_mat_didactico  = {2020: 
                          {3: 9.7, #ayudanteA
                          4: 10.8, #ayudanteB
                          1: 13.6, #profesorA
                          2:14.6  #profesorB
                          },
                      2021: 
                          {3: 9.7, #ayudanteA
                          4: 10.8, #ayudanteB
                          1: 13.6, #profesorA
                          2:14.6  #profesorB
                          } 
                     }

tab_vale_libros = {
    2020:{
        'mayor': 1090,
        'menor': 545
    },
    2021:{
        'mayor': 1155,
        'menor': 578
    }
}

tab_rec_pers_acad  = {2020: 
                          {
                          3: 46.29, #ayudanteA
                          4: 51.53, #ayudanteB
                          1: 64.39, #profesorA
                          2: 73.21  #profesorB
                          },
                      2021: 
                          {
                          3: 47.87, #ayudanteA
                          4: 53.59, #ayudanteB
                          1: 66.58, #profesorA
                          2: 75.70  #profesorB
                          } 
                     }

apoyo_superacion_acad ={
                        2020: {
                            'bajo': 2435.59,
                            'medio': 2918.46,
                            'alto': 4248.43
                        },
                        2021: {
                            'bajo': 2435.59,
                            'medio': 3017.68,
                            'alto': 4392.88
                        }
                    }

tab_pepasig = {2020:
              {1: {'A': 619, 'B': 636, 'C': 777, 'D': 947},
               2: {'A': 1235, 'B': 1267, 'C': 1553, 'D': 1903},
               3: {'A': 1974, 'B': 2027 , 'C': 2485 , 'D': 3041},
               4: {'A': 2802, 'B': 2867, 'C': 3503, 'D': 4277},
               5: {'A': 3502, 'B': 3567, 'C': 4346, 'D': 5368},
               6: {'A': 3911, 'B': 3993, 'C': 4877, 'D': 6013},
               7: {'A': 4323, 'B': 4405, 'C': 5368, 'D': 6629},
               8: {'A': 4732, 'B': 4822, 'C': 5874, 'D': 7243},
               9: {'A': 5147, 'B': 5242, 'C': 6383, 'D': 7887},
               10: {'A': 5561, 'B': 5562, 'C': 6896, 'D': 8502}},
              2021:
              {1: {'A': 619, 'B': 636, 'C': 777, 'D': 947},
               2: {'A': 1235, 'B': 1267, 'C': 1553, 'D': 1903},
               3: {'A': 1974, 'B': 2027 , 'C': 2485 , 'D': 3041},
               4: {'A': 2802, 'B': 2867, 'C': 3503, 'D': 4277},
               5: {'A': 3502, 'B': 3567, 'C': 4346, 'D': 5368},
               6: {'A': 3911, 'B': 3993, 'C': 4877, 'D': 6013},
               7: {'A': 4323, 'B': 4405, 'C': 5368, 'D': 6629},
               8: {'A': 4732, 'B': 4822, 'C': 5874, 'D': 7243},
               9: {'A': 5147, 'B': 5242, 'C': 6383, 'D': 7887},
               10: {'A': 5561, 'B': 5562, 'C': 6896, 'D': 8502}}}



# DEFINE CLASES: CURSO Y ACADEMICO

"""
Datos de cada curso que da acdémico. Nesesario dado que un acdémico puede
tener 2 nombramientos. 
"""
class Curso():
    #nombramiento = 1
    #horas = 4
    #anio = 2021
    #periodo = 2

    def __init__(self,n,h,sa,sp):
        self.nombramiento = n
        self.horas_contrato = h
        self.semestre_anio = sa
        self.semestre_periodo = sp


"""
Datos de académico UNAM, útiles para calcular su sueldo.
"""
class Academico():
    cursos = []
    nombramientos = []
    horas_semana = 0
    

    def __init__(self,ads,ant,sem_ant = False, asist = False, pepasig = False, grado = None):
        self.adscripcion = ads
        self.antiguedad = ant
        self.sem_ant = sem_ant
        self.asist = asist
        self.grado = grado
        self.pepasig = pepasig
    
    def AgregarCurso(self, curso):
        self.cursos.append(curso)
        self.nombramientos.append(curso.nombramiento)
        self.horas_semana += curso.horas_contrato
        


#FUNCIONES

## Compensación antigüedad
"""
(2020) Por cada año de servicio cumplido, el 2% del salario tabular entre el
quinto y el vigésimo año, y  2.5 % a partir del vigésimo primero.
"""
def antiguedadQuincenal(acad):### revisar lo de la multiplicacion
    if (acad.antiguedad >= 5) & (acad.antiguedad <= 20): # >= 5 o > 5???
        return acad.antiguedad*0.02# * sueldoQuincenal(acad)
    elif(acad.antiguedad > 20):
        return acad.antiguedad*0.025# * sueldoQuincenal(acad)
    return 0.0

"""
Calcula el sueldo quincenal.
"""
def sueldoQuincenal(acad, anio):
    s = 0.0
    for c in acad.cursos:
        s += sueldo[anio][c.nombramiento] * c.horas_contrato / 2
    
    s *= (1+antiguedadQuincenal(acad))###########################################
    return s



## Ayuda material didáctico (quincenal)
"""
(2020) Importe por categoria, pago quincenal:  Por hora/semana/mes de $13.60 a $14.60;
por Medio Tiempo de $138.00 a $429.00; por Tiempo Completo de $276.00 a $858.00
y Profesor Enseñanza Media Superior de $474.00 a $530.00
"""

def MatDidactico(acad, anio):
    s = 0
    for curso in acad.cursos:
        s += tab_mat_didactico[anio][curso.nombramiento]*curso.horas_contrato/2
    return s

    
## Vale libros
"""
(2020) Académico contratado por menos de 20 hrs. $545.00 anual
y con 20 horas o más $1,090.00 anual.
"""

def ValeLibros(acad, anio):
    if acad.horas_semana*4 < 20:
        status = 'menor'
    else:
        status = 'mayor'
        
    return tab_vale_libros[anio][status]
    

## Vale día del maestro
"""
(2020) 995.00 anual.
"""
vale_d_maestro = {
    2020: 995,
    2021: 1044
}

## Días de ajuste
"""
(2020) 5 días al año (6 días en caso de año bisiesto).
"""
def DiasAjuste(acad, anio):
    if semestre_anio % 4 == 0: #bisiesto
        num_dias = 6
    else:
        num_dias = 5
    
    return sueldoQuincenal(acad, anio)/15*num_dias

## Prima vacacional
"""
(2020) 60% del salario, correspondiente a las vacaciones respectivas.
"""
def PrimaVacacional(acad, anio):
    return sueldoQuincenal(acad, anio)/15*20*0.6

    
## Aguinaldo
"""
(2020) 40 días, que se pagan en dos exhibiciones de 20 días.
"""
def MedioAguinaldo(acad, anio):
    return sueldoQuincenal(acad, anio)/15*20


## Complemento profesores de asignatura
complemento_asignatura = {
    2020: 7.7,
    2021: 9.3 # ???
}
"""
(2020) A partir de 10 horas/semana/mes o más, recibirán un complemento de
$7.70 por cada hora/semana/mes que impartan, pago quincenal.
"""

def complementoAsignaturaQuincenal(acad, anio):
    horas_asignatura = 0
    for curso in acad.cursos:
        if curso.nombramiento in [1,2]:
            horas_asignatura += curso.horas_contrato
        
    if horas_asignatura >= 10:
        return horas_asignatura*complemento_asignatura[anio]
    else:
        return 0


# Estímulos

## Reconocimiento de Profesores de Asignatura
"""
Reconocimiento al Trabajo del Personal Académico Asignatura,
cuota por hora/semana/mes contratada;  pago trimestral;
Prof. Asig. "A": $64.39,  Prof Asig. "B": $73.21,
Ayte. Prof. "A": $46.29, Ayte. Prof. "B": $51.53
"""

def ReconocimientoProfAsig(acad, anio):
    s = 0
    for curso in acad.cursos:
        s += tab_rec_pers_acad[anio][curso.nombramiento]*curso.horas_contrato*3

    return s


## Superación académica
"""
Apoyo para la Superación Académica, cuota por horas contratadas,
pago semestral.; de 0.5 a 19.5 hras $2,435.59,
de 20 a 39.5 hras $2,918.46, de 40 hras $4,248.43
"""
1,044.

def SuperacionAcademica(acad, anio):
    if acad.horas_semana >= 20 & acad.horas_semana < 40 : # >= 5 o > 5???
        return apoyo_superacion_acad[anio]['medio']
    elif(acad.horas_semana > 40):
        return apoyo_superacion_acad[anio]['alto']
    
    return apoyo_superacion_acad[anio]['bajo']


## Asistencia
"""
Estímulo de Asistencia: Con un mínimo de 90% de asistencia,
15 dias salario íntegro al año.
"""
def estimuloAsistenciaSemestral(acad, anio):
    if acad.asist == True:
        return sueldoQuincenal(acad, anio)/2
    else:
        return 0
    
## PEPASIG
"""
Programa de Estímulos a la Productividad y al Rendimiento del Personal
Académico de Asignatura, por horas contratadas y grado académico; pago mensual.
"""

def Pepasig(acad, anio):
    horas_asignatura = 0
    for curso in acad.cursos:
        if curso.nombramiento in [1,2]:
            horas_asignatura += curso.horas_contrato
    
    if acad.pepasig:
        if horas_asignatura >= 30:
            return tab_pepasig[anio][10][acad.grado]
        elif (horas_asignatura>=3)&(horas_asignatura <30):
            return tab_pepasig[anio][acad.antiguedad//3][acad.grado]
        else:
            return 0
    else:
        return 0


def ModificarMatriz(matriz, acad):
    """
    Si es semestre 1 (agosto-enero) y no trabajó el semestre anterior
    no hay segunda entrega de aguinaldo en enero
    """
    matriz = matriz.copy()
    if (semestre_periodo == 1)&(acad.sem_ant):
        return matriz
    else:
        matriz[7,22] = 0
        return matriz
    
#CON TODAS LAS FUNCIONES ANTERIORES, GENERA EL VECTOR DE MONTOS DEL ACADEMICO  
def Montos(acad, anio):
    montos = np.zeros(15)
    #anio = semestre_anio 
    montos[0]  = sueldoQuincenal(acad,anio)
    montos[1]  = MatDidactico(acad, anio)
    montos[2]  = complementoAsignaturaQuincenal(acad, anio)
    montos[3]  = vale_despensa[anio]
    montos[4]  = ReconocimientoProfAsig(acad, anio)
    montos[5]  = SuperacionAcademica(acad, anio)
    montos[6]  = PrimaVacacional(acad, anio)
    montos[7]  = MedioAguinaldo(acad, anio)
    montos[8]  = ValeLibros(acad, anio)
    montos[9]  = vale_d_maestro[anio]
    montos[10] = DiasAjuste(acad, anio)
    montos[11] = sueldoQuincenal(acad, anio)/15
    montos[12] = vale_despensa[anio]
    montos[13] = estimuloAsistenciaSemestral(acad, anio)
    montos[14] = Pepasig(acad, anio)
    
    return montos

# GENERA LA MATRIZ DE SEMESTRES (INFORMACION DEL TRIPTICO)
#matriz 2020-2021
matriz = np.zeros((15,36))
matriz[0] = np.ones(36) #sueldo base
matriz[1] = np.ones(36) #material didactico
matriz[2] = np.ones(36) #complemento prof asignatura
matriz[3] = 18*[0,1] #ayuda despensa
matriz[4] = np.roll(6*[0,0,0,0,0,1], 4) #reconocimiento al personal academico
matriz[5,1] = matriz[5,15] = matriz[5,25] = 1 #apoyo superacion academica
matriz[6,10] = matriz[6,21] = matriz[6,34] = 1 # Prima vacacional
matriz[7, 20] = matriz[7,22] = 1 # Aguinaldo
matriz[8, 2] = matriz[8, 26] =1 #ayuda adq. libros
matriz[9,6] = matriz[9,30] = 1  #Ayuda libros dia del maestro
matriz[10, 10] = matriz[10, 34] = 1 #dias de ajuste
matriz[11,6] = matriz[11, 18] = matriz[11, 20] = 1 #Pago clausula 60
matriz[11, 30] = 2
matriz[12,1] = matriz[12,25] = 1 #despensa extraordinaria
matriz[13,11] = matriz[13, 23] = 1 #bono asistencia
matriz[14] = 18*[0,1]# PEPASIG


conceptos = ['Sueldo base',
             'Material didáctico',
             'Complemento prof. asignatura',
             'Ayuda despensa',
             'Reconocimiento al personal académico',
             'Apoyo para la superación acad.',
             'Prima vacacional',
             '(medio) Aguinaldo',
             'Ayuda adq. libros',
             'Ayuda libros dia del maestro',
             'Dias de ajuste',
             'Pago clausula 60',
             'Despensa extraordinaria',
             'Bono asistencia',
             'PEPASIG']
conceptos = np.array(conceptos)

def Semestre_consulta(semestre_anio, semestre_periodo):
    if semestre_anio == 2020 and semestre_periodo == 2:
        quincenas_consulta = np.concatenate([np.ones(15),np.zeros(21)])
    elif semestre_anio == 2021 and semestre_periodo == 1:
        quincenas_consulta = np.concatenate([np.zeros(15),np.ones(11), np.zeros(10)])
    elif semestre_anio == 2021 and semestre_periodo == 2:
        quincenas_consulta = np.concatenate([np.zeros(26),np.ones(10)])
        
    return quincenas_consulta


def Calculo_ingreso_semestral(semestre_anio, semestre_periodo, entidad, antiguedad, lista_cursos, tiene_pepasig,impartio_anterior):
    global matriz
    quincenas_consulta = Semestre_consulta(semestre_anio, semestre_periodo) #todo el anio. Falta hacer la funcion que genere el vector a partir del semestre solicitado


    acad = Academico(entidad, antiguedad)
    for elemento in lista_cursos:
        acad.AgregarCurso(Curso(elemento[0], elemento[1], semestre_anio, semestre_periodo))
        #curso2 = Curso(1, 3, semestre_anio, semestre_periodo) #un curso como ayudante A: nombramiento = 3

    nom_quincenas =  np.roll(range(1,25),-2)
    nom_quincenas = np.concatenate([nom_quincenas, nom_quincenas[:12]])

    matriz = ModificarMatriz(matriz,acad)
    matriz = pd.DataFrame(matriz, index=conceptos,  columns= nom_quincenas)
    matriz = matriz.iloc[:, quincenas_consulta==1]
    
    anio = semestre_anio
    if semestre_periodo == 1:
        anio -= 1
    print(anio)
    montos = Montos(acad, anio)
    montos = pd.Series(montos, index = conceptos)
    

    tabla = matriz.mul(montos, axis = 0).round(2)    
    if (semestre_anio == 2021) & (semestre_periodo == 1):#modifica los montos de los ultimos dos meses de ese semestre
        tabla.loc[:,[3,4]] = matriz.loc[:,[3,4]].mul(Montos(acad,2021), axis = 0).round(2) 
    tabla = tabla.T
    tabla = tabla.iloc[:,(tabla.cumsum().iloc[-1, :] != 0).values]
        
        
    tabla['Total quincena'] = tabla.sum(axis = 1)
    tabla['Total acumulado'] = tabla['Total quincena'].cumsum()

    return dict(tabla.apply(lambda x: x.round(2)).T.apply(dict))




Calculo_ingreso_semestral(semestre_anio, semestre_periodo, entidad, antiguedad, lista_cursos, tiene_pepasig, impartio_anterior)
