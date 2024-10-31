import re
import json
from itertools import product

def transformar_a_logica(oracion):
    elementos = re.split(r'\s+y\s+|\s+o\s+', oracion)
    expresion_logica = oracion.replace(" y ", " ∧ ").replace(" o ", " ∨ ")
    etiquetas = ['X', 'Y', 'Z', 'W', 'P', 'Q']
    correspondencia = {elementos[i]: etiquetas[i] for i in range(len(elementos))}
    
    for elemento, etiqueta in correspondencia.items():
        expresion_logica = expresion_logica.replace(elemento, etiqueta)
    
    return expresion_logica, correspondencia

def crear_tabla_verdad(expresion_logica, correspondencia):
    variables = list(correspondencia.values())
    n = len(variables)
    casos = list(product([True, False], repeat=n))
    tabla_verdad = []

    for caso in casos:
        valor_actual = dict(zip(variables, caso))
        resultado = eval(expresion_logica.replace("∧", " and ").replace("∨", " or "), {}, valor_actual)
        tabla_verdad.append((caso, resultado))
    
    return tabla_verdad

def desplegar_tabla(tabla_verdad, correspondencia):
    variables = list(correspondencia.values())
    encabezado = " | ".join(variables) + " | Resultado"
    salida = encabezado + "\n" + "-" * len(encabezado) + "\n"
    
    for fila in tabla_verdad:
        valores = ["V" if v else "F" for v in fila[0]]
        resultado = "V" if fila[1] else "F"
        salida += " | ".join(valores) + " | " + resultado + "\n"
    
    print(salida)

def almacenar_reglas(archivo, lista_reglas):
    with open(archivo, 'w', encoding='utf-8') as file:
        json.dump(lista_reglas, file)
    print(f"Reglas guardadas en {archivo}.")

def recuperar_reglas(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            lista_reglas = json.load(file)
        print(f"Reglas recuperadas desde {archivo}.")
        return lista_reglas
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def evaluar_atomica(correspondencia):
    respuestas = {}
    for elemento, etiqueta in correspondencia.items():
        respuesta = input(f"¿{elemento} es Verdadero (V) o Falso (F)? ")
        respuestas[etiqueta] = True if respuesta.lower() == 'v' else False
    return respuestas

def programa_principal():
    lista_reglas = []
    archivo_json = "reglas.json"

    while True:
        print("\n1. Crear nueva regla")
        print("2. Mostrar reglas y desplegar tabla de verdad")
        print("3. Guardar reglas")
        print("4. Cargar reglas")
        print("5. Evaluar proposición simple")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            oracion = input("Ingrese una proposición lógica: ")
            expresion_logica, correspondencia = transformar_a_logica(oracion)
            lista_reglas.append({"expresion_logica": expresion_logica, "correspondencia": correspondencia})
            print("Regla creada.")
        
        elif opcion == "2":
            for regla in lista_reglas:
                expresion_logica = regla["expresion_logica"]
                correspondencia = regla["correspondencia"]
                print(f"\nExpresión lógica: {expresion_logica}")
                print("Correspondencia de proposiciones:", correspondencia)
                tabla_verdad = crear_tabla_verdad(expresion_logica, correspondencia)
                desplegar_tabla(tabla_verdad, correspondencia)
        
        elif opcion == "3":
            almacenar_reglas(archivo_json, lista_reglas)
        
        elif opcion == "4":
            lista_reglas = recuperar_reglas(archivo_json)
        
        elif opcion == "5":
            if lista_reglas:
                expresion_logica, correspondencia = lista_reglas[0]["expresion_logica"], lista_reglas[0]["correspondencia"]
                respuestas = evaluar_atomica(correspondencia)
                evaluacion = eval(expresion_logica.replace("∧", " and ").replace("∨", " or "), {}, respuestas)
                print(f"Evaluación de la proposición: {evaluacion}")
            else:
                print("No hay reglas cargadas para evaluar.")
        
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    programa_principal()
