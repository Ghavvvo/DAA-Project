import itertools
from .modelos import Mula
def calcular_metrica(mulas):
    """
    Calcula la diferencia de valor entre la mula más rica y la más pobre.
    Devuelve infinito si no se puede asignar todo sin violar pesos.
    """
    if not mulas:
        return float('inf')
    valores = [m.valor_actual for m in mulas]
    return max(valores) - min(valores)


def fuerza_bruta(articulos, mulas_plantilla):
    """
    Prueba todas las formas posibles de asignar artículos a mulas.
    """
    n_mulas = len(mulas_plantilla)
    mejor_diferencia = float('inf')
    mejor_solucion = None

    for asignacion in itertools.product(range(n_mulas), repeat=len(articulos)):
        mulas_temp = [Mula(m.id, m.capacidad) for m in mulas_plantilla]
        es_valida = True

        for idx_art, idx_mula in enumerate(asignacion):
            articulo = articulos[idx_art]
            if not mulas_temp[idx_mula].agregar_articulo(articulo):
                es_valida = False
                break

        # Verificar que todas las mulas tengan al menos un artículo
        if es_valida:
            if all(len(mula.articulos) > 0 for mula in mulas_temp):
                diferencia = calcular_metrica(mulas_temp)
                if diferencia < mejor_diferencia:
                    mejor_diferencia = diferencia
                    mejor_solucion = mulas_temp

                    if mejor_diferencia == 0:
                        return mejor_solucion, mejor_diferencia

    return mejor_solucion, mejor_diferencia


def heuristica_voraz(articulos, mulas_plantilla):
    """
    Ordena los artículos por valor y los asigna a la mula que tenga menos valor y pueda llevarlo.
    """
    mulas = [Mula(m.id, m.capacidad) for m in mulas_plantilla]
    articulos_ordenados = sorted(articulos, key=lambda x: x.valor, reverse=True)

    n_mulas = len(mulas)
    n_articulos = len(articulos_ordenados)

    # Verificar que haya al menos tantos artículos como mulas
    if n_articulos < n_mulas:
        return None, float('inf')  # Imposible asignar un artículo a cada mula

    # Fase 1: Asignar al menos un artículo a cada mula (round-robin)
    articulos_asignados = set()
    for idx_mula in range(n_mulas):
        asignado = False
        for idx_art, art in enumerate(articulos_ordenados):
            if idx_art not in articulos_asignados:
                if mulas[idx_mula].agregar_articulo(art):
                    articulos_asignados.add(idx_art)
                    asignado = True
                    break

        if not asignado:
            return None, float('inf')  # No se pudo asignar a esta mula

    # Fase 2: Asignar artículos restantes con estrategia voraz
    for idx_art, art in enumerate(articulos_ordenados):
        if idx_art in articulos_asignados:
            continue  # Ya fue asignado en Fase 1

        mula_candidata = None
        menor_valor_actual = float('inf')

        for m in mulas:
            if m.peso_actual + art.peso <= m.capacidad:
                if m.valor_actual < menor_valor_actual:
                    menor_valor_actual = m.valor_actual
                    mula_candidata = m

        if mula_candidata:
            mula_candidata.agregar_articulo(art)
        else:
            return None, float('inf')  # Fallo: No cupo el artículo

    return mulas, calcular_metrica(mulas)


def busqueda_local(articulos, mulas_plantilla, max_iter=1000):
    """
    Parte de la solución voraz e intenta mejorar moviendo artículos entre mulas.
    """
    solucion_actual, dif_actual = heuristica_voraz(articulos, mulas_plantilla)

    if solucion_actual is None:
        return None, float('inf')

    mejora_encontrada = True
    iteracion = 0

    while mejora_encontrada and iteracion < max_iter:
        mejora_encontrada = False
        iteracion += 1

        mulas_ordenadas = sorted(solucion_actual, key=lambda m: m.valor_actual)
        mula_min = mulas_ordenadas[0]
        mula_max = mulas_ordenadas[-1]

        dif_actual = mula_max.valor_actual - mula_min.valor_actual

        # Intento 1: Mover artículos de mula_max a mula_min
        for art in list(mula_max.articulos):
            # Verificar que mula_max no se quede vacía
            if len(mula_max.articulos) <= 1:
                continue

            if mula_min.peso_actual + art.peso <= mula_min.capacidad:
                nuevo_val_max = mula_max.valor_actual - art.valor
                nuevo_val_min = mula_min.valor_actual + art.valor
                nueva_dif_local = abs(nuevo_val_max - nuevo_val_min)

                if nueva_dif_local < dif_actual:
                    mula_max.remover_articulo(art)
                    mula_min.agregar_articulo(art)
                    mejora_encontrada = True
                    break

        if mejora_encontrada:
            continue

        # Intento 2: Intercambio de artículos
        for art_max in list(mula_max.articulos):
            for art_min in list(mula_min.articulos):
                peso_nuevo_max = mula_max.peso_actual - art_max.peso + art_min.peso
                peso_nuevo_min = mula_min.peso_actual - art_min.peso + art_max.peso

                if (peso_nuevo_max <= mula_max.capacidad and
                        peso_nuevo_min <= mula_min.capacidad):

                    val_nuevo_max = mula_max.valor_actual - art_max.valor + art_min.valor
                    val_nuevo_min = mula_min.valor_actual - art_min.valor + art_max.valor
                    nueva_dif = abs(val_nuevo_max - val_nuevo_min)

                    if nueva_dif < dif_actual:
                        mula_max.remover_articulo(art_max)
                        mula_max.agregar_articulo(art_min)
                        mula_min.remover_articulo(art_min)
                        mula_min.agregar_articulo(art_max)
                        mejora_encontrada = True
                        break
            if mejora_encontrada:
                break

    return solucion_actual, calcular_metrica(solucion_actual)

