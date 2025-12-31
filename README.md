# Proyecto Final: Diseño y Análisis de Algoritmos

## Problema: El Negocio del Transporte Discreto (Discrete Logistics)

Este proyecto implementa y analiza experimentalmente algoritmos para resolver el problema de distribución de carga en "mulas" de transporte, minimizando la diferencia de valor entre los transportistas respetando sus capacidades de peso.

### Autores
- Adrian Alejandro Souto Morales
- Gabriel Herrera Carrazana

### Algoritmos Implementados
1. **Fuerza Bruta:** Solución exacta (línea base).
2. **Heurística Voraz (Greedy):** Solución aproximada eficiente.
3. **Metaheurística (Búsqueda Local):** Refinamiento de la solución voraz.

### Requisitos Previos
- Python 3.x
- Librerías: pandas, matplotlib, seaborn, numpy

### Instalación
1. Clona o descarga el repositorio.
2. Instala las dependencias ejecutando el siguiente comando en la terminal:
   ```
   pip install -r requirements.txt
   ```

### Uso
1. Abre el archivo `tests.ipynb` en Jupyter Notebook o JupyterLab.
2. Ejecuta las celdas en orden para ver las implementaciones de los algoritmos y los experimentos realizados.
3. Los resultados incluyen gráficos de calidad de la solución y escalabilidad en tiempo.

### Estructura del Proyecto
- `tests.ipynb`: Notebook principal con implementaciones y experimentos.
- `informe.tex` / `informe.pdf`: Informe técnico detallado.
- `requirements.txt`: Lista de dependencias del proyecto.
- `calidad_solucion.png`: Gráfico de calidad de la solución.
- `escalabilidad_tiempo.png`: Gráfico de escalabilidad en tiempo.
- `report.txt`: Archivo de reporte adicional.

### Conclusiones
De acuerdo con los análisis, se recomienda implementar el algoritmo de **Búsqueda Local** , ya que ofrece el mejor balance entre minimizar el riesgo (distribución equitativa) y tiempo de cómputo.
