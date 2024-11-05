import re
import json
from itertools import product

# Letras para etiquetar proposiciones
LETRAS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

def transformar_a_formula(frase):
    # Manejo de negación usando 'no'
    frase = re.sub(r'no\s+(\w+)', r'¬\1', frase)
    
    proposiciones = re.split(r'\s+y\s+|\s+o\s+', frase)
    formula = frase.replace(" y ", " ∧ ").replace(" o ", " ∨ ")
    mapeo = {proposiciones[i]: LETRAS[i] for i in range(len(proposiciones))}
    
    for proposicion, letra in mapeo.items():
        formula = formula.replace(proposicion, letra)
    
    return formula, mapeo

def crear_tabla_verdad(formula, mapeo):
    props = list(mapeo.values())
    n = len(props)
    combinaciones = list(product([True, False], repeat=n))
    tabla = []

    for combinacion in combinaciones:
        valores = dict(zip(props, combinacion))
        
        # Evaluación lógica de la fórmula
        evaluacion = eval(
            formula.replace("∧", " and ").replace("∨", " or ").replace("¬", " not "),
            {}, valores
        )
        tabla.append((combinacion, evaluacion))
    
    return tabla

def mostrar_tabla_verdad(tabla, mapeo):
    props = list(mapeo.values())
    encabezado = " | ".join(props) + " | Resultado"
    salida = encabezado + "\n" + "-" * len(encabezado) + "\n"
    
    for fila in tabla:
        valores = ["V" if v else "F" for v in fila[0]]
        resultado = "V" if fila[1] else "F"
        salida += " | ".join(valores) + " | " + resultado + "\n"
    
    return salida

def mostrar_tabla_atomos(mapeo):
    props = list(mapeo.values())
    n = len(props)
    combinaciones = list(product([True, False], repeat=n))
    encabezado = " | ".join(props)
    salida = f"Tabla de átomos:\n{encabezado}\n" + "-" * len(encabezado) + "\n"
    
    for combinacion in combinaciones:
        valores = ["V" if v else "F" for v in combinacion]
        salida += " | ".join(valores) + "\n"
    
    return salida

def mostrar_arbol_binario(tabla, mapeo):
    props = list(mapeo.values())
    salida = "\nÁrbol de Decisión Binario:\n"
    
    def construir_nodo(nivel, combinacion, resultado):
        if nivel == len(props):
            return f"{'V' if resultado else 'F'}\n"
        
        prop = props[nivel]
        estado = "Verdadero" if combinacion[nivel] else "Falso"
        espaciado = "    " * nivel
        nodo_texto = f"{espaciado}{prop} es {estado} -> "
        
        nodo_texto += construir_nodo(nivel + 1, combinacion, resultado)
        return nodo_texto
    
    for fila in tabla:
        combinacion, resultado = fila
        salida += construir_nodo(0, combinacion, resultado)
        salida += "-" * 30 + "\n"
    
    return salida

def mostrar_clausulas_horn(tabla, mapeo):
    props = list(mapeo.values())
    salida = "\nCláusulas de Horn:\n"

    for fila in tabla:
        combinacion, resultado = fila
        antecedente = []
        
        for i, valor in enumerate(combinacion):
            if not valor:
                antecedente.append(f"¬{props[i]}")
            else:
                antecedente.append(props[i])
        
        consecuente = "Verdadero" if resultado else "Falso"
        
        if antecedente:
            salida += f"{' ∧ '.join(antecedente)} → {consecuente}\n"
        else:
            salida += f"{consecuente}\n"
    
    return salida

def guardar_clausulas_horn(reglas):
    archivo_txt = "clausulas_horn.txt"
    with open(archivo_txt, 'w', encoding='utf-8') as file:
        for idx, regla in enumerate(reglas[:20]):
            formula, mapeo = regla["formula"], regla["mapeo"]
            tabla = crear_tabla_verdad(formula, mapeo)
            clausulas = mostrar_clausulas_horn(tabla, mapeo)
            file.write(f"Regla {idx + 1}:\n{clausulas}\n")
    print(f"Cláusulas de Horn guardadas en {archivo_txt}.")

def guardar_reglas(archivo, reglas):
    with open(archivo, 'w', encoding='utf-8') as file:
        json.dump(reglas, file)
    print(f"Reglas guardadas en {archivo}.")

def cargar_reglas(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            reglas = json.load(file)
        print(f"Reglas cargadas desde {archivo}.")
        return reglas
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def preguntar_atomica(mapeo):
    respuestas = {}
    for proposicion, letra in mapeo.items():
        respuesta = input(f"¿{proposicion} es Verdadero (V) o Falso (F)? ")
        respuestas[letra] = True if respuesta.lower() == 'v' else False
    return respuestas

def cargar_oraciones_desde_txt(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            oraciones = file.readlines()
        
        reglas = []
        for oracion in oraciones:
            oracion = oracion.strip()
            if oracion:
                formula, mapeo = transformar_a_formula(oracion)
                reglas.append({"formula": formula, "mapeo": mapeo})
        
        print(f"Oraciones cargadas desde {archivo}.")
        return reglas
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def main():
    reglas = []
    archivo = "reglas.json"

    while True:
        print("\n" + "="*40)
        print(" MENU DE OPCIONES ".center(40, "="))
        print("1. Ingresar nueva regla")
        print("2. Mostrar tabla de verdad y árbol de decisión")
        print("3. Guardar reglas")
        print("4. Cargar reglas")
        print("5. Evaluar proposición atómica")
        print("6. Mostrar tabla de átomos")
        print("7. Mostrar cláusulas de Horn")
        print("8. Guardar cláusulas de Horn")
        print("9. Cargar reglas desde archivo .txt")
        print("10. Salir")
        print("="*40)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            oracion = input("Ingrese una proposición compuesta: ")
            formula, mapeo = transformar_a_formula(oracion)
            reglas.append({"formula": formula, "mapeo": mapeo})
            print("Regla añadida.")
        
        elif opcion == "2":
            for idx, regla in enumerate(reglas, start=1):
                formula = regla["formula"]
                mapeo = regla["mapeo"]
                print(f"\nRegla {idx}")
                print(f"Fórmula lógica: {formula}")
                print("Mapeo de proposiciones:", mapeo)
                tabla = crear_tabla_verdad(formula, mapeo)
                print(mostrar_tabla_verdad(tabla, mapeo))
                print(mostrar_arbol_binario(tabla, mapeo))
        
        elif opcion == "3":
            guardar_reglas(archivo, reglas)
        
        elif opcion == "4":
            reglas = cargar_reglas(archivo)
        
        elif opcion == "5":
            if reglas:
                formula, mapeo = reglas[0]["formula"], reglas[0]["mapeo"]
                respuestas = preguntar_atomica(mapeo)
                evaluacion = eval(formula.replace("∧", " and ").replace("∨", " or ").replace("¬", " not "), {}, respuestas)
                print(f"Evaluación de la proposición: {'V' if evaluacion else 'F'}")
            else:
                print("No hay reglas cargadas para evaluar.")
        
        elif opcion == "6":
            if reglas:
                for idx, regla in enumerate(reglas, 1):
                    mapeo = regla["mapeo"]
                    print(f"\nTabla de átomos para Regla {idx}:")
                    print(mostrar_tabla_atomos(mapeo))
            else:
                print("No hay reglas cargadas para mostrar la tabla de átomos.")
        
        elif opcion == "7":
            if reglas:
                for regla in reglas:
                    formula, mapeo = regla["formula"], regla["mapeo"]
                    tabla = crear_tabla_verdad(formula, mapeo)
                    print(mostrar_clausulas_horn(tabla, mapeo))
            else:
                print("No hay reglas cargadas para mostrar cláusulas de Horn.")
        
        elif opcion == "8":
            guardar_clausulas_horn(reglas)
        
        elif opcion == "9":
            archivo_txt = input("Ingrese el nombre del archivo .txt: ")
            reglas = cargar_oraciones_desde_txt(archivo_txt)
        
        elif opcion == "10":
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
