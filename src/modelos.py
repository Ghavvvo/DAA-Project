class Articulo:
    """Representa un artículo a transportar con peso y valor."""

    def __init__(self, id_art, peso, valor):
        self.id = id_art
        self.peso = peso
        self.valor = valor

    def __repr__(self):
        return f"A{self.id}(p={self.peso}, v={self.valor})"


class Mula:
    """Representa un transportista (mula) con capacidad limitada."""

    def __init__(self, id_mula, capacidad):
        self.id = id_mula
        self.capacidad = capacidad
        self.articulos = []
        self.peso_actual = 0
        self.valor_actual = 0

    def agregar_articulo(self, articulo):
        """Intenta agregar un artículo si hay capacidad."""
        if self.peso_actual + articulo.peso <= self.capacidad:
            self.articulos.append(articulo)
            self.peso_actual += articulo.peso
            self.valor_actual += articulo.valor
            return True
        return False

    def remover_articulo(self, articulo):
        """Remueve un artículo de la mula."""
        if articulo in self.articulos:
            self.articulos.remove(articulo)
            self.peso_actual -= articulo.peso
            self.valor_actual -= articulo.valor
            return True
        return False

    def copiar(self):
        """Crea una copia profunda de la mula."""
        nueva = Mula(self.id, self.capacidad)
        for art in self.articulos:
            nueva.agregar_articulo(art)
        return nueva

