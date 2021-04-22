import numpy as np
import pandas as pd


# Notas
# todos los identificadores los dejé en español para evitar confusiones
# con las traducciones al inglés de los tecnicismos...


## DICCIONARIOS PARA TODOS LOS TABULADORES TABLAS
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
        1: 400.24,
        2: 455.04,
        3: 304.08,
        4: 338.88
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
        'mayor': 1090,
        'menor': 545
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
                          3: 46.29, #ayudanteA
                          4: 51.53, #ayudanteB
                          1: 64.39, #profesorA
                          2: 73.21  #profesorB
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
                            'medio': 2918.46,
                            'alto': 4248.43
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
Datos de contrato de acdémico. Nesesario dado que un acdémico puede
tener 2 nombramientos. El nombre de esta clase no es adecuado, pues
el contrato es único cada semestre.
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
    ID = 'database_id' # Innecesario?
    nombre = 'Prof. X' # Innecesario?
    #adscripcion = 'Facultad de Ciencias' # Innecesario?
    #antiguedad = 1
    #contratos = [Contrato(1,4,2021,2)]
    cursos = []
    #contratos_semestre_anterior = []
    nombramientos = []
    horas_semana = 0
    

    def __init__(self,i,n,ads,ant,sem_ant = False, asist = False, pepasig = False, grado = None):
        self.id = i
        self.nombre = n
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
def sueldoQuincenal(acad):
    s = 0.0
    for c in acad.cursos:
        s += sueldo[c.semestre_anio][c.nombramiento] * c.horas_contrato / 2
    
    s *= (1+antiguedadQuincenal(acad))###########################################
    return s



## Ayuda material didáctico (quincenal)
"""
(2020) Importe por categoria, pago quincenal:  Por hora/semana/mes de $13.60 a $14.60;
por Medio Tiempo de $138.00 a $429.00; por Tiempo Completo de $276.00 a $858.00
y Profesor Enseñanza Media Superior de $474.00 a $530.00
"""


def MatDidactico(acad):
    max_nomb = min(acad.nombramientos)
    return tab_mat_didactico[semestre_anio][max_nomb] #se da el monto para el mayor nombramiento o por cada nombramiento???
    
    
## Vale libros
"""
(2020) Académico contratado por menos de 20 hrs. $545.00 anual
y con 20 horas o más $1,090.00 anual.
"""

def ValeLibros(acad):
    if acad.horas_semana*4 < 20:
        status = 'menor'
    else:
        status = 'mayor'
        
    return tab_vale_libros[semestre_anio][status]
    

## Vale día del maestro
"""
(2020) 995.00 anual.
"""
vale_d_maestro = {
    2020: 995,
    2021: 995
}

## Días de ajuste
"""
(2020) 5 días al año (6 días en caso de año bisiesto).
"""
def DiasAjuste(acad):
    if semestre_anio % 4 == 0: #bisiesto
        num_dias = 6
    else:
        num_dias = 5
    
    return sueldoQuincenal(acad)/15*num_dias

## Prima vacacional
"""
(2020) 60% del salario, correspondiente a las vacaciones respectivas.
"""
def PrimaVacacional(acad):
    return sueldoQuincenal(acad)/15*20*0.6

    
## Aguinaldo
"""
(2020) 40 días, que se pagan en dos exhibiciones de 20 días.
"""
def MedioAguinaldo(acad):
    return sueldoQuincenal(acad)/15*20


## Complemento profesores de asignatura
complemento_asignatura = {
    2020: 7.7,
    2021: 7.7 # ???
}
"""
(2020) A partir de 10 horas/semana/mes o más, recibirán un complemento de
$7.70 por cada hora/semana/mes que impartan, pago quincenal.
"""
#def complementoAsignaturaQuincenal(acad):
#    s = 0.0
#    for c in acad.contratos:
#        if c.horas >= 10
#            if c.nombramiento == 1 || c.nombramiento == 2: # Ayudantes excluidos
#                s += c.horas * 7.7
#    return s
def complementoAsignaturaQuincenal(acad):
    if (acad.horas_semana>=10)&(min(acad.nombramientos) in [1,2]):
        return acad.horas_semana*complemento_asignatura[semestre_anio]*2
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

def ReconocimientoProfAsig(acad):
    """
    Duda: si hay dos nombramientos, es horas totales por maximo nombramiento o
    horas por nombramiento por monto nombramiento"""
    return tab_rec_pers_acad[semestre_anio][min(acad.nombramientos)]*acad.horas_semana*3 

## Superación académica
"""
Apoyo para la Superación Académica, cuota por horas contratadas,
pago semestral.; de 0.5 a 19.5 hras $2,435.59,
de 20 a 39.5 hras $2,918.46, de 40 hras $4,248.43
"""


def SuperacionAcademica(acad):
    if acad.horas_semana >= 20 & acad.horas_semana < 40 : # >= 5 o > 5???
        return apoyo_superacion_acad[semestre_anio]['medio']
    elif(acad.antiguedad > 40):
        return apoyo_superacion_acad[semestre_anio]['alto']
    
    return apoyo_superacion_acad[semestre_anio]['bajo']


## Asistencia
"""
Estímulo de Asistencia: Con un mínimo de 90% de asistencia,
15 dias salario íntegro al año.
"""
def estimuloAsistenciaSemestral(acad):
    if acad.asist == True:
        return sueldoQuincenal(acad)/2
    else:
        return 0
    
## PEPASIG
"""
Programa de Estímulos a la Productividad y al Rendimiento del Personal
Académico de Asignatura, por horas contratadas y grado académico; pago mensual.
"""

def Pepasig(acad):
    if acad.pepasig:
        if acad.horas_semana >= 30:
            return tab_pepasig[semestre_anio][10][acad.grado]
        elif (acad.horas_semana>=3)&(acad.horas_semana <30):
            return tab_pepasig[semestre_anio][acad.antiguedad//3][acad.grado]
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
def Montos(acad):
    montos = np.zeros(15)
    anio = acad.cursos[0].semestre_anio #el anio; tal vez haya que extraer el anio del formulario
    montos[0]  = sueldoQuincenal(acad)
    montos[1]  = MatDidactico(acad)
    montos[2]  = complementoAsignaturaQuincenal(acad)
    montos[3]  = vale_despensa[anio]
    montos[4]  = ReconocimientoProfAsig(acad)
    montos[5]  = SuperacionAcademica(acad)
    montos[6]  = PrimaVacacional(acad)
    montos[7]  = MedioAguinaldo(acad)
    montos[8]  = ValeLibros(acad)
    montos[9]  = vale_d_maestro[anio]
    montos[10] = DiasAjuste(acad)
    montos[11] = sueldoQuincenal(acad)/15
    montos[12] = vale_despensa[anio]
    montos[13] = estimuloAsistenciaSemestral(acad)
    montos[14] = Pepasig(acad)
    
    return montos

# GENERA LA MATRIZ DE SEMESTRES (INFORMACION DEL TRIPTICO)
#requiere: año, semestre

matriz = np.zeros((15,24))
matriz[0] = np.ones(24) #sueldo base
matriz[1] = np.ones(24) #material didactico
matriz[2] = np.ones(24) #complemento prof asignatura
matriz[3] = 12*[0,1] #ayuda despensa
matriz[4] = np.roll(4*[0,0,0,0,0,1], 4) #reconocimiento al personal academico
matriz[5,1] = matriz[5,15] = 1 #apoyo superacion academica
matriz[6,10] = matriz[6,21] = 1 # Prima vacacional
matriz[7, 20] = matriz[7,22] = 1 # Aguinaldo
matriz[8, 2] = 1 #ayuda adq. libros
matriz[9,6] = 1  #Ayuda libros dia del maestro
matriz[10, 10] = 1 #dias de ajuste
matriz[11,14] = matriz[11, 18] = 1 #Pago clausula 60
matriz[12,1] = 1 #despensa extraordinaria
matriz[13,11] = matriz[13, 23] = 1 #bono asistencia
matriz[14] = 12*[0,1]# PEPASIG

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

####
####EJEMPLO

# NECESITAMOS DEL FORMULARIO
#año, 
#semestre
#quincena de consulta.
#cursos impartidos: horas y nombramiento
#PEPASIG
#antigüedad
#impartió curso el semestre anterior?

semestre_anio = 2020
semestre_periodo = 1
quincenas_consulta = np.ones(24) #todo el anio. Falta hacer la funcion que genere el vector a partir del semestre solicitado
tiene_pepasig = False
antiguedad = 3
acad_id = 5551
acad_nom = 'CFBM'
entidad = 'Ciencias'
impartio_anterior = True

#cursos: un formulario por curso
curso1 = Curso(1, 4, semestre_anio, semestre_periodo) #un curso como profe A: nombramiento = 1
curso2 = Curso(3, 3, semestre_anio, semestre_periodo) #un curso como ayudante A: nombramiento = 3


#GENERA LAS VARIABLES acad y dos cursos
acad = Academico(acad_id, acad_nom, entidad, antiguedad)


acad.AgregarCurso(curso1)
acad.AgregarCurso(curso2)

matriz = ModificarMatriz(matriz,acad)
matriz = pd.DataFrame(matriz, index=conceptos,  columns= np.roll(range(1,25),-2))


montos = Montos(acad)
montos = pd.Series(montos, index = conceptos)


tabla = matriz.mul(montos, axis = 0).round(2).T
tabla = tabla.iloc[:,(tabla.cumsum().iloc[-1, :] != 0).values]

print(tabla)