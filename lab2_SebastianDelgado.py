nodos = ["E", "C", "J", "R", "T", "S"]

espacios = {
    "E": "Entrada",
    "C": "Exposición de ciencias",
    "J": "Zona de juegos",
    "R": "Robótica",
    "T": "Talleres",
    "S": "Salida"
}

mapa = {
    "E": ["C", "J"],
    "C": ["E", "R", "T"],
    "J": ["E", "S"],
    "R": ["C", "S"],
    "T": ["C", "S"],
    "S": ["J", "R", "T"]
}


def construir_matriz(mapa, nodos):
    matriz = []

    for origen in nodos:
        fila = []

        for destino in nodos:
            if destino in mapa[origen]:
                fila.append(1)
            else:
                fila.append(0)

        matriz.append(fila)

    return matriz


def dfs_recursivo(mapa, inicio):
    recorrido = []
    visitados = set()

    def explorar(nodo):
        visitados.add(nodo)
        recorrido.append(nodo)

        for vecino in mapa[nodo]:
            if vecino not in visitados:
                explorar(vecino)

    explorar(inicio)

    return recorrido


def dfs_iterativo(mapa, inicio):
    recorrido = []
    visitados = set()
    pila = [inicio]

    while pila:
        nodo = pila.pop()

        if nodo in visitados:
            continue

        visitados.add(nodo)
        recorrido.append(nodo)

        for vecino in reversed(mapa[nodo]):
            if vecino not in visitados:
                pila.append(vecino)

    return recorrido


def solicitar_nodo(mensaje):
    nodo = input(mensaje).strip().upper()

    if nodo in mapa:
        return nodo

    print("Ese espacio no existe en el mapa.")
    return None


def ver_conexiones():
    nodo = solicitar_nodo("Espacio: ")

    if nodo is None:
        return

    vecinos = ", ".join(mapa[nodo])
    print(f"{nodo} · {espacios[nodo]} se conecta con: {vecinos}")


def ver_matriz():
    matriz = construir_matriz(mapa, nodos)

    print()
    print("  " + " ".join(nodos))

    for i in range(len(nodos)):
        print(nodos[i], " ".join(map(str, matriz[i])))


def ver_dfs_recursivo():
    inicio = solicitar_nodo("Nodo inicial: ")

    if inicio is None:
        return

    recorrido = dfs_recursivo(mapa, inicio)
    print("DFS recursivo:", " -> ".join(recorrido))


def ver_dfs_iterativo():
    inicio = solicitar_nodo("Nodo inicial: ")

    if inicio is None:
        return

    recorrido = dfs_iterativo(mapa, inicio)
    print("DFS iterativo:", " -> ".join(recorrido))


def consultar_pasillo():
    origen = solicitar_nodo("Origen: ")

    if origen is None:
        return

    destino = solicitar_nodo("Destino: ")

    if destino is None:
        return

    matriz = construir_matriz(mapa, nodos)

    fila_origen = nodos.index(origen)
    columna_destino = nodos.index(destino)

    if matriz[fila_origen][columna_destino] == 1:
        print(f"Sí existe un pasillo directo entre {origen} y {destino}.")
    else:
        print(f"No existe un pasillo directo entre {origen} y {destino}.")


def menu():
    while True:
        print()
        print("=== MAPA DE LA FERIA CIENTÍFICA ===")
        print("1. Ver conexiones de un espacio")
        print("2. Ver matriz de adyacencia")
        print("3. Recorrer con DFS recursivo")
        print("4. Recorrer con DFS iterativo")
        print("5. Consultar si hay un pasillo directo")
        print("6. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            ver_conexiones()
        elif opcion == "2":
            ver_matriz()
        elif opcion == "3":
            ver_dfs_recursivo()
        elif opcion == "4":
            ver_dfs_iterativo()
        elif opcion == "5":
            consultar_pasillo()
        elif opcion == "6":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
