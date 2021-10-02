# MyRLike
> *Jesus Abraham Haros Madrid*

> *A01252642*

> *A01252642@itesm.mx*

El proyecto MYRLike consiste en desarrollar un compilador para un lenguaje orientado a jóvenes que buscan aprender los fundamentos de la programación, a través del manejo y manipulación de conjuntos de datos simples para realizar análisis estadístico básico.

## Avance 1

Para este primer avance se desarrollaron los diagramas de sintaxis, tokens y gramáticas para MYRLike, especificamente en este repositorio se entrega la implementación en python utilizando PLY para construir un analizador léxico y un analizador sintáctico.

Para probar el codigo es necesario proveer un archivo de texto como parámetro al momento de hacer la ejecución.

*Ejemplo*

    python3 MyRLike_parse.py testValid.txt
Donde ***testValid.txt*** es la ruta del archivo a analizar.