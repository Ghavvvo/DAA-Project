import random
from .algorithms import Item, Mule

def generate_instance(num_items, num_mules, weight_range, value_range, mule_capacity_range=None, fixed_capacity=None, custom_capacities=None):
    """
    Generates a random instance of the problem.
    
    Args:
        num_items (int): Number of items to generate.
        num_mules (int): Number of mules to generate.
        weight_range (tuple): (min_weight, max_weight) for items.
        value_range (tuple): (min_value, max_value) for items.
        mule_capacity_range (tuple, optional): (min_cap, max_cap) for mules.
        fixed_capacity (int, optional): Fixed capacity for all mules.
        custom_capacities (list, optional): List of capacities for each mule.
        
    Returns:
        tuple: (list of Items, list of Mules)
    """
    items = []
    for i in range(num_items):
        w = random.randint(weight_range[0], weight_range[1])
        v = random.randint(value_range[0], value_range[1])
        items.append(Item(i, w, v))
        
    mules = []
    for i in range(num_mules):
        if custom_capacities and i < len(custom_capacities):
            cap = custom_capacities[i]
        elif fixed_capacity:
            cap = fixed_capacity
        elif mule_capacity_range:
            cap = random.randint(mule_capacity_range[0], mule_capacity_range[1])
        else:
            # Default capacity logic if not specified: enough to hold average items but constrained
            avg_item_weight = (weight_range[0] + weight_range[1]) / 2
            cap = int((avg_item_weight * num_items / num_mules) * 1.2) # 20% slack
            
        mules.append(Mule(i, cap))
        
    return items, mules


def generate_case1():
    """
    Caso 1: Instancia Simple Factible
    2 mulas, 4 artículos, pesos y valores balanceados
    Capacidades: Mula1=30, Mula2=30
    Artículos: (peso=10, valor=5), (15,8), (12,6), (8,4)
    """
    items = [
        Item(0, 10, 5),
        Item(1, 15, 8),
        Item(2, 12, 6),
        Item(3, 8, 4)
    ]
    mules = [
        Mule(0, 30),
        Mule(1, 30)
    ]
    return items, mules


def generate_case2():
    """
    Caso 2: No Factible por Capacidad
    2 mulas, 3 artículos
    Capacidades: Mula1=60, Mula2=60 (total=120)
    Artículos: (50,30), (50,30), (50,30) (peso total=150)
    """
    items = [
        Item(0, 50, 30),
        Item(1, 50, 30),
        Item(2, 50, 30)
    ]
    mules = [
        Mule(0, 60),
        Mule(1, 60)
    ]
    return items, mules


def generate_case3():
    """
    Caso 3: Valores Extremos
    2 mulas, 4 artículos
    Artículo 1: peso=1, valor=1000
    Artículo 2: peso=100, valor=1
    Artículos 3-4: peso=50, valor=500
    Capacidades: 100 cada mula
    """
    items = [
        Item(0, 1, 1000),
        Item(1, 100, 1),
        Item(2, 50, 500),
        Item(3, 50, 500)
    ]
    mules = [
        Mule(0, 100),
        Mule(1, 100)
    ]
    return items, mules


def generate_case4():
    """
    Caso 4: Caso Tipo PARTITION
    2 mulas, 5 artículos
    Pesos/Valores: 30, 20, 20, 15, 15 (suma total=100)
    Capacidades: 50 cada mula
    """
    items = [
        Item(0, 30, 30),
        Item(1, 20, 20),
        Item(2, 20, 20),
        Item(3, 15, 15),
        Item(4, 15, 15)
    ]
    mules = [
        Mule(0, 50),
        Mule(1, 50)
    ]
    return items, mules


def generate_case5():
    """
    Caso 5: Todas las Mulas con Capacidad Idéntica
    3 mulas, 6 artículos
    Capacidades: todas = 100
    Artículos: valores variados pero suma total divisible entre 3 (600)
    """
    items = [
        Item(0, 10, 80),
        Item(1, 10, 90),
        Item(2, 10, 100),
        Item(3, 10, 110),
        Item(4, 10, 120),
        Item(5, 10, 100)
    ]
    mules = [
        Mule(0, 100),
        Mule(1, 100),
        Mule(2, 100)
    ]
    return items, mules


def generate_case6():
    """
    Caso 6: Capacidades Muy Desiguales
    3 mulas
    Capacidades: Mula1=30, Mula2=50, Mula3=100
    6 artículos con pesos y valores variados
    """
    items = [
        Item(0, 10, 20),
        Item(1, 15, 25),
        Item(2, 20, 30),
        Item(3, 25, 35),
        Item(4, 30, 40),
        Item(5, 35, 45)
    ]
    mules = [
        Mule(0, 30),
        Mule(1, 50),
        Mule(2, 100)
    ]
    return items, mules


def generate_case7():
    """
    Caso 7: Un Solo Artículo Muy Grande
    2 mulas, 3 artículos
    Capacidades: 50 cada mula
    Artículo 1: peso=48, valor=100
    Artículos 2-3: peso=10, valor=20 cada uno
    """
    items = [
        Item(0, 48, 100),
        Item(1, 10, 20),
        Item(2, 10, 20)
    ]
    mules = [
        Mule(0, 50),
        Mule(1, 50)
    ]
    return items, mules


def generate_case8():
    """
    Caso 8: Múltiples Soluciones Óptimas
    2 mulas, 4 artículos
    Todos los artículos: peso=10, valor=10
    Capacidades: 20 cada mula
    """
    items = [
        Item(0, 10, 10),
        Item(1, 10, 10),
        Item(2, 10, 10),
        Item(3, 10, 10)
    ]
    mules = [
        Mule(0, 20),
        Mule(1, 20)
    ]
    return items, mules


def generate_case9():
    """
    Caso 9: Múltiples Mulas (M > 5)
    7 mulas, 21 artículos
    Capacidades: 50 cada mula
    Artículos: peso=10, valor=10 cada uno
    """
    items = [Item(i, 10, 10) for i in range(21)]
    mules = [Mule(i, 50) for i in range(7)]
    return items, mules


def generate_case10():
    """
    Caso 10: Relación Peso/Valor Inversa
    2 mulas, 4 artículos
    Artículo 1: peso=5, valor=100
    Artículo 2: peso=10, valor=80
    Artículo 3: peso=15, valor=60
    Artículo 4: peso=20, valor=40
    Capacidades: 50 cada mula
    """
    items = [
        Item(0, 5, 100),
        Item(1, 10, 80),
        Item(2, 15, 60),
        Item(3, 20, 40)
    ]
    mules = [
        Mule(0, 50),
        Mule(1, 50)
    ]
    return items, mules


def generate_case11():
    """
    Caso 11: Caso del Ejemplo del Informe
    2 mulas, 5 artículos (peso=valor para simplificar)
    Valores: 5, 5, 4, 4, 4
    Capacidades: 20 cada una
    """
    items = [
        Item(0, 5, 5),
        Item(1, 5, 5),
        Item(2, 4, 4),
        Item(3, 4, 4),
        Item(4, 4, 4)
    ]
    mules = [
        Mule(0, 20),
        Mule(1, 20)
    ]
    return items, mules


def generate_case12():
    """
    Caso 12: Instancia Vacía o Minimal
    Retorna una lista de subcasos: A, B, C
    """
    # Caso A: 2 mulas, 0 artículos
    items_a = []
    mules_a = [Mule(0, 50), Mule(1, 50)]

    # Caso B: 1 mula, 3 artículos
    items_b = [Item(0, 10, 20), Item(1, 15, 25), Item(2, 20, 30)]
    mules_b = [Mule(0, 100)]

    # Caso C: 3 mulas, 1 artículo
    items_c = [Item(0, 10, 20)]
    mules_c = [Mule(0, 50), Mule(1, 50), Mule(2, 50)]

    return [
        ("Caso 12A: 2 mulas, 0 artículos", items_a, mules_a),
        ("Caso 12B: 1 mula, 3 artículos", items_b, mules_b),
        ("Caso 12C: 3 mulas, 1 artículo", items_c, mules_c)
    ]
