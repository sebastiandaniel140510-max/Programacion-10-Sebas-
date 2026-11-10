
from collections import deque

red = {
    "Santiago": ["Mercedes Sur", "Barbacoas", "Candelarita"],
    "Mercedes Sur": ["Santiago", "San Rafael"],
    "Barbacoas": ["Santiago", "Grifo Alto"],
    "San Rafael": ["Mercedes Sur", "Grifo Alto"],
    "Grifo Alto": ["Barbacoas", "San Rafael"],
    "Candelarita": ["Santiago"],
    "Desamparaditos": ["Chires"],
    "Chires": ["Desamparaditos"],
    "Zapatón": []
}

obras = {
    "Estudio": ["Permisos", "Materiales"],
    "Permisos": ["Excavación"],
    "Materiales": ["Alcantarillado", "Asfaltado"],
    "Excavación": ["Alcantarillado"],
    "Alcantarillado": ["Asfaltado"],
    "Asfaltado": ["Señalización"],
    "Señalización": []
}


def dfs_iterativo(grafo, inicio):
    pila = [inicio]
    visitados = []
    marcados = set()

    while pila:
        actual = pila.pop()

        if actual not in marcados:
            marcados.add(actual)
            visitados.append(actual)

            for vecino in reversed(grafo[actual]):
                if vecino not in marcados:
                    pila.append(vecino)

    return visitados


def ruta_mas_corta(grafo, inicio, destino):
    cola = deque([inicio])
    padres = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == destino:
            ruta = []

            while actual is not None:
                ruta.append(actual)
                actual = padres[actual]

            return ruta[::-1]

        for vecino in grafo[actual]:
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)

    return None


def contar_componentes(grafo):
    visitados = set()
    componentes = {}
    numero = 0

    for comunidad in grafo:
        if comunidad not in visitados:
            numero += 1
            pila = [comunidad]

            while pila:
                actual = pila.pop()

                if actual not in visitados:
                    visitados.add(actual)
                    componentes[actual] = numero

                    for vecino in reversed(grafo[actual]):
                        if vecino not in visitados:
                            pila.append(vecino)

    return numero, componentes


def tiene_ciclo(grafo):
    visitados = set()

    def dfs(actual, padre):
        visitados.add(actual)

        for vecino in grafo[actual]:
            if vecino not in visitados:
                if dfs(vecino, actual):
                    return True
            elif vecino != padre:
                return True

        return False

    for comunidad in grafo:
        if comunidad not in visitados:
            if dfs(comunidad, None):
                return True

    return False


def orden_topologico(grafo):
    grados = {obra: 0 for obra in grafo}

    for dependientes in grafo.values():
        for dependiente in dependientes:
            grados[dependiente] += 1

    cola = deque(
        [obra for obra in grafo if grados[obra] == 0]
    )

    orden = []

    while cola:
        actual = cola.popleft()
        orden.append(actual)

        for dependiente in grafo[actual]:
            grados[dependiente] -= 1

            if grados[dependiente] == 0:
                cola.append(dependiente)

    return orden


while True:
    print("\n=== RED VIAL DE PURISCAL ===")
    print("1. Ver la red de caminos")
    print("2. Agregar un camino")
    print("3. Comunidades alcanzables desde una comunidad")
    print("4. Ruta con menos tramos entre dos comunidades")
    print("5. Componentes conexas de la red")
    print("6. Detectar caminos circulares")
    print("7. Orden de ejecución de las obras")
    print("8. Agregar un prerrequisito entre obras")
    print("9. Salir")

    try:
        opcion = int(input("\nElija una opción: "))
    except ValueError:
        print("\nOpción inválida. Debe digitar un número del 1 al 9.")
        continue

    if opcion == 1:
        print("\nRed de caminos de Puriscal")

        total_grados = 0

        for comunidad, vecinos in red.items():
            grado = len(vecinos)
            total_grados += grado

            if vecinos:
                print(f"{comunidad} (grado {grado}): {', '.join(vecinos)}")
            else:
                print(f"{comunidad} (grado {grado}): sin caminos")

        print(f"Total de caminos: {total_grados // 2}")

    elif opcion == 2:
        origen = input("Primera comunidad: ").strip().title()
        destino = input("Segunda comunidad: ").strip().title()

        if origen not in red:
            print(f"\nNo existe la comunidad '{origen}'.")
        elif destino not in red:
            print(f"\nNo existe la comunidad '{destino}'.")
        elif origen == destino:
            print("\nUna comunidad no puede conectarse consigo misma.")
        elif destino in red[origen]:
            print(f"\nYa existe un camino entre {origen} y {destino}.")
        else:
            red[origen].append(destino)
            red[destino].append(origen)
            print(f"\nCamino agregado entre {origen} y {destino}.")

    elif opcion == 3:
        inicio = input("Comunidad de inicio: ").strip().title()

        if inicio not in red:
            print(f"\nNo existe la comunidad '{inicio}'.")
        else:
            visitados = dfs_iterativo(red, inicio)

            print(f"\nComunidades alcanzables desde {inicio}: {len(visitados)}")
            print(" -> ".join(visitados))

    elif opcion == 4:
        inicio = input("Comunidad de origen: ").strip().title()
        destino = input("Comunidad de destino: ").strip().title()

        if inicio not in red:
            print(f"\nNo existe la comunidad '{inicio}'.")
        elif destino not in red:
            print(f"\nNo existe la comunidad '{destino}'.")
        elif inicio == destino:
            print("\nEl origen y el destino no pueden ser iguales.")
        else:
            ruta = ruta_mas_corta(red, inicio, destino)

            if ruta is None:
                print(f"\nNo existe una ruta entre {inicio} y {destino}.")
            else:
                print("\nRuta con menos tramos:", " -> ".join(ruta))
                print(f"Cantidad de tramos: {len(ruta) - 1}")

    elif opcion == 5:
        cantidad, componentes = contar_componentes(red)

        grupos = {}

        for comunidad in red:
            numero = componentes[comunidad]

            if numero not in grupos:
                grupos[numero] = []

            grupos[numero].append(comunidad)

        print()

        for numero, comunidades in grupos.items():
            print(f"Componente {numero}: {', '.join(comunidades)}")

        if cantidad == 1:
            print("La red tiene 1 componente conexa y todas las comunidades están comunicadas.")
        else:
            print(f"La red tiene {cantidad} componentes conexas y no todas las comunidades están comunicadas.")

    elif opcion == 6:
        ciclo_dfs = tiene_ciclo(red)

        cantidad_componentes, componentes = contar_componentes(red)

        total_caminos = sum(len(vecinos) for vecinos in red.values()) // 2
        cantidad_comunidades = len(red)

        caminos_permitidos = cantidad_comunidades - cantidad_componentes

        ciclo_conteo = total_caminos > caminos_permitidos

        print()

        if ciclo_dfs:
            print("Búsqueda con DFS: la red tiene al menos un camino circular.")
        else:
            print("Búsqueda con DFS: la red no tiene caminos circulares.")

        if ciclo_conteo:
            print(f"Comprobación por conteo: {total_caminos} caminos frente a {caminos_permitidos} permitidos sin ciclos ({cantidad_comunidades} comunidades - {cantidad_componentes} componentes).")
        else:
            print(f"Comprobación por conteo: {total_caminos} caminos frente a {caminos_permitidos} permitidos sin ciclos ({cantidad_comunidades} comunidades - {cantidad_componentes} componentes).")

        if ciclo_dfs == ciclo_conteo:
            print("Los dos métodos coinciden.")
        else:
            print("Los dos métodos no coinciden.")

    elif opcion == 7:
        orden = orden_topologico(obras)

        print("\nOrden de ejecución de las obras:")

        if len(orden) == len(obras):
            print(" -> ".join(orden))
        else:
            bloqueadas = [
                obra for obra in obras if obra not in orden
            ]

            print("Hay un ciclo de prerrequisitos: no existe un orden válido.")
            print("Obras bloqueadas:", ", ".join(bloqueadas))

    elif opcion == 8:
        previa = input("Obra previa: ").strip().title()
        dependiente = input("Obra que depende de ella: ").strip().title()

        if previa not in obras:
            print(f"\nNo existe la obra '{previa}'.")
        elif dependiente not in obras:
            print(f"\nNo existe la obra '{dependiente}'.")
        elif previa == dependiente:
            print("\nUna obra no puede depender de sí misma.")
        elif dependiente in obras[previa]:
            print(f"\nEl prerrequisito entre {previa} y {dependiente} ya existe.")
        else:
            obras[previa].append(dependiente)
            print(f"\nPrerrequisito agregado: {previa} debe terminar antes de {dependiente}.")

    elif opcion == 9:
        print("\nGracias por utilizar el programa. ¡Hasta luego!")
        break

    else:
        print("\nOpción inválida. Debe digitar un número del 1 al 9.")
