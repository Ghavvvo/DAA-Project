import random
import json
class Generador:
    """Generador de instancias para Discrete Logistics"""

    def __init__(self, seed=42):
        """Inicializa el generador con una seed específica"""
        self.seed = seed
        random.seed(seed)
        self.instancias = []

    def generar_aleatorias(self):
        """Genera 100 instancias aleatorias distribuidas en categorías"""

        # Configuración de categorías: (nombre, n_min, n_max, m_min, m_max, cantidad)
        categorias = [
            ('pequena', 5, 10, 2, 3, 30),  # 30 instancias pequeñas
            ('mediana', 10, 20, 3, 5, 40),  # 40 instancias medianas
            ('grande', 20, 50, 5, 10, 20),  # 20 instancias grandes
            ('muy_grande', 50, 100, 10, 20, 10),  # 10 instancias muy grandes
        ]

        id_counter = 1

        for categoria, n_min, n_max, m_min, m_max, cantidad in categorias:
            for _ in range(cantidad):
                # Generar parámetros básicos
                n = random.randint(n_min, n_max)
                m = random.randint(m_min, m_max)
                if n < m:
                    n = m + 1  # Asegurar n >= m para problemas interesantes

                # Generar artículos
                articulos = []
                for _ in range(n):
                    # 70% correlacionados, 30% no correlacionados
                    if random.random() < 0.7:
                        peso = random.randint(1, 100)
                        valor = max(1, peso + random.randint(-20, 20))
                    else:
                        peso = random.randint(1, 100)
                        valor = random.randint(1, 100)
                    articulos.append([peso, valor])

                # Generar capacidades variables para cada mula
                peso_total = sum(p for p, _ in articulos)
                peso_max = max(p for p, _ in articulos)

                # Capacidad base promedio
                cap_base = random.randint(
                    max(peso_max, peso_total // m),
                    peso_total // m * 2
                )

                # Generar capacidades con variación (±30%)
                capacidades = []
                for _ in range(m):
                    variacion = random.uniform(0.7, 1.3)
                    cap_mula = max(peso_max, int(cap_base * variacion))
                    capacidades.append(cap_mula)

                # Crear instancia
                instancia = {
                    'id': f"rand_{id_counter:03d}",
                    'n': n,
                    'm': m,
                    'articulos': articulos,
                    'capacidades': capacidades,  # Ahora es una lista
                    'categoria': categoria
                }

                self.instancias.append(instancia)
                id_counter += 1

        return self.instancias

    def agregar_edge_cases(self):
        """Agrega 12 casos edge predefinidos"""

        edge_cases = [
            # 1. Solución perfecta balanceada
            {
                'id': 'edge_001',
                'n': 4, 'm': 2,
                'articulos': [[5, 5], [5, 5], [5, 5], [5, 5]],
                'capacidades': [10, 10],
                'categoria': 'edge',
                'descripcion': 'Solución perfecta balanceada'
            },
            # 2. Infactible por capacidad
            {
                'id': 'edge_002',
                'n': 3, 'm': 2,
                'articulos': [[10, 50], [1, 1], [1, 1]],
                'capacidades': [5, 6],
                'categoria': 'edge',
                'descripcion': 'Artículo excede capacidad individual'
            },
            # 3. Infactible por balance perfecto
            {
                'id': 'edge_003',
                'n': 2, 'm': 2,
                'articulos': [[1, 100], [1, 1]],
                'capacidades': [100, 80],
                'categoria': 'edge',
                'descripcion': 'Imposible balance perfecto con valores diferentes'
            },
            # 4. Solución única
            {
                'id': 'edge_004',
                'n': 3, 'm': 2,
                'articulos': [[4, 10], [2, 5], [2, 5]],
                'capacidades': [6, 4],
                'categoria': 'edge',
                'descripcion': 'Solución única forzada con capacidades asimétricas'
            },
            # 5. Artículo grande indivisible
            {
                'id': 'edge_005',
                'n': 3, 'm': 2,
                'articulos': [[95, 100], [10, 10], [10, 10]],
                'capacidades': [100, 25],
                'categoria': 'edge',
                'descripcion': 'Artículo ocupa casi toda la capacidad de una mula'
            },
            # 6. Más mulas que artículos
            {
                'id': 'edge_006',
                'n': 2, 'm': 4,
                'articulos': [[5, 5], [5, 5]],
                'capacidades': [10, 8, 12, 6],
                'categoria': 'edge',
                'descripcion': 'Más mulas que artículos con capacidades variadas'
            },
            # 7. Valores no correlacionados
            {
                'id': 'edge_007',
                'n': 4, 'm': 2,
                'articulos': [[10, 1], [1, 100], [5, 50], [4, 10]],
                'capacidades': [15, 12],
                'categoria': 'edge',
                'descripcion': 'Trade-off extremo peso vs valor'
            },
            # 8. Caso difícil de partición
            {
                'id': 'edge_008',
                'n': 8, 'm': 2,
                'articulos': [[7, 7], [6, 6], [5, 5], [4, 4], [4, 4], [3, 3], [2, 2], [2, 2]],
                'capacidades': [16, 17],
                'categoria': 'edge',
                'descripcion': 'Caso clásico difícil de number partitioning'
            },
            # 9. Límite estricto de capacidad
            {
                'id': 'edge_009',
                'n': 3, 'm': 2,
                'articulos': [[5, 10], [5, 9], [5, 8]],
                'capacidades': [10, 8],
                'categoria': 'edge',
                'descripcion': 'Capacidades ajustadas para balance difícil'
            },
            # 10. Simetría completa con capacidades diferentes
            {
                'id': 'edge_010',
                'n': 6, 'm': 3,
                'articulos': [[10, 10], [10, 10], [10, 10], [10, 10], [10, 10], [10, 10]],
                'capacidades': [20, 25, 18],
                'categoria': 'edge',
                'descripcion': 'Múltiples soluciones simétricas con capacidades variadas'
            },
            # 11. Capacidad exacta requerida
            {
                'id': 'edge_011',
                'n': 5, 'm': 2,
                'articulos': [[8, 15], [7, 12], [5, 8], [4, 6], [1, 2]],
                'capacidades': [13, 15],
                'categoria': 'edge',
                'descripcion': 'Uso exacto de capacidad necesario con mulas diferentes'
            },
            # 12. Artículos con valor cero
            {
                'id': 'edge_012',
                'n': 3, 'm': 2,
                'articulos': [[5, 0], [5, 0], [5, 100]],
                'capacidades': [10, 8],
                'categoria': 'edge',
                'descripcion': 'Artículos con valor cero y capacidades asimétricas'
            }
        ]

        self.instancias.extend(edge_cases)
        return self.instancias



    def generar_todas(self):
        """Genera todas las instancias (aleatorias + edge cases)"""
        self.generar_aleatorias()
        self.agregar_edge_cases()
        return self.instancias


