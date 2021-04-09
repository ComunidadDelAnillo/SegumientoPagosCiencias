
# Notas
# todos los identificadores los dejé en español para evitar confusiones
# con las traducciones al inglés de los tecnicismos...

nombramiento = {
    0: 'Ninguno',
    1: 'Profesor de Asignatura A',
    2: 'Profesor de Asignatura B',
    3: 'Ayudante de Profesor A',
    4: 'Ayudante de Profesor B'
}


"""
Datos de contrato de acdémico. Nesesario dado que un acdémico puede
tener 2 nombramientos. El nombre de esta clase no es adecuado, pues
el contrato es único cada semestre.
"""
class ContratoNombramiento:
    nombramiento = 1
    horas = 4
    anio = 2021
    periodo = 2

    def __init(self,n,h,sa,sp)__:
        self.nombramiento = n
        self.horas_contrato = h
        self.semestre_anio = sa
        self.semestre_periodo = sp


"""
Datos de académico UNAM, útiles para calcular su sueldo.
"""
class Academico:
    ID = 'database_id' # Innecesario?
    nombre = 'Prof. X' # Innecesario?
    adscripcion = 'Facultad de Ciencias' # Innecesario?
    antiguedad = 1
    contratos = [Contrato(1,4,2021,2)]
    contratos_semestre_anterior = []

    def __init(self,i,n,ads,ant)__:
        self.id = i
        self.nombre = n
        self.adscripcion = ads
        self.antiguedad = ant


# Sueldos (hora/semana/mes) según tabulador UNAM 2020, falta 2021
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

"""
Calcula el sueldo quincenal.
"""
def sueldoQuincenal(acad):
    s = 0.0
    for c in acad.contratos:
        s += sueldo[c.anio][c.nombramiento] * c.horas / 2
    return s



# Prestaciones
# Datos del tabulador UNAM 2020.

## Compensación antigüedad
"""
(2020) Por cada año de servicio cumplido, el 2% del salario tabular entre el
quinto y el vigésimo año, y  2.5 % a partir del vigésimo primero.
"""
def antiguedadQuincenal(acad):
    if acad.antiguedad >= 5 && acad.antiguedad <= 20: # >= 5 o > 5???
        return 0.02 * sueldoQuincenal(acad)
    elif(acad.antiguedad > 20):
        return 0.025 * sueldoQuincenal(acad)
    return 0.0

## Vale despensa mensual (quincenas pares)
vale_despensa = {
    2020: 1255.0,
    2021: 1443.0
}

## Ayuda material didáctico (quincenal)
"""
(2020) Importe por categoria, pago quincenal:  Por hora/semana/mes de $13.60 a $14.60;
por Medio Tiempo de $138.00 a $429.00; por Tiempo Completo de $276.00 a $858.00
y Profesor Enseñanza Media Superior de $474.00 a $530.00
"""

## Vale libros
"""
(2020) Académico contratado por menos de 20 hrs. $545.00 anual
y con 20 horas o más $1,090.00 anual.
"""

## Vale día del maestro
"""
(2020) 995.00 anual.
"""

## Días de ajuste
"""
(2020) 5 días al año (6 días en caso de año bisiesto).
"""

## Prima vacacional
"""
(2020) 60% del salario, correspondiente a las vacaciones respectivas.
"""

## Aguinaldo
"""
(2020) 40 días, que se pagan en dos exhibiciones de 20 días.
"""
## Complemento profesores de asignatura
complemento_asignatura = {
    2020: 7.7,
    2021: 7.7 # ???
}
"""
(2020) A partir de 10 horas/semana/mes o más, recibirán un complemento de
$7.70 por cada hora/semana/mes que impartan, pago quincenal.
"""
def complementoAsignaturaQuincenal(acad):
    s = 0.0
    for c in acad.contratos:
        if c.horas >= 10
            if c.nombramiento == 1 || c.nombramiento == 2: # Ayudantes excluidos
                s += c.horas * 7.7
    return s


# Estímulos

## PEPASIG
"""
Programa de Estímulos a la Productividad y al Rendimiento del Personal
Académico de Asignatura, por horas contratadas y grado académico; pago mensual.
"""

## Reconocimiento de Profesores de Asignatura
"""
Reconocimiento al Trabajo del Personal Académico Asignatura,
cuota por hora/semana/mes contratada;  pago trimestral;
Prof. Asig. "A": $64.39,  Prof Asig. "B": $73.21,
Ayte. Prof. "A": $46.29, Ayte. Prof. "B": $51.53
"""

## Superación académica
"""
Apoyo para la Superación Académica, cuota por horas contratadas,
pago semestral.; de 0.5 a 19.5 hras $2,435.59,
de 20 a 39.5 hras $2,918.46, de 40 hras $4,248.43
"""

## Asistencia
"""
Estímulo de Asistencia: Con un mínimo de 90% de asistencia,
15 dias salario íntegro al año.
"""


# Cálculo de percepciones totales

"""
Calcula las percepciones totales en la quincena q.
"""
def percepcionesTotalesQuincena(acad, q):
    s = 0.0

    if q % 2 == 0: # si la quincena es par hay despensa
        s += vale_despensa[acad.contratos[0].anio]

    return s


"""
Calcula las percepciones totales de una quincena inicial a una final.
"""
def percepcionesTotalesSemestre(acad, qini, qfin):
    return 0.0


"""
Calcula las percepciones totales en un semestre (pago único).
"""
def percepcionesTotalesSemestre(acad):
    return 0.0
