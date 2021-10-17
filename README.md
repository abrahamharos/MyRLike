# MyRLike
> *Jesus Abraham Haros Madrid*

> *A01252642*

> *A01252642@itesm.mx*

El proyecto MYRLike consiste en desarrollar un compilador para un lenguaje orientado a jóvenes que buscan aprender los fundamentos de la programación, a través del manejo y manipulación de conjuntos de datos simples para realizar análisis estadístico básico.

## Avance 1

Para este primer avance se desarrollaron los diagramas de sintaxis, tokens y gramáticas para MYRLike, especificamente en este repositorio se entrega la implementación en python utilizando PLY para construir un analizador léxico y un analizador sintáctico.

## Avance 2

Para este segundo avance se elaboró el código con el que MYRLike manejará el directorio de funciones y de variables. Se tuvieron que actualizar las reglas de sintaxis para poder guardar los valores de la variables. Adicionalmente se creó un archivo llamado cubo semantico en el que se guarda el tipo resultado de aplicar operaciones a dos variables.
Se entregan diagramas actualizados y una tabla del cubo semantico.
Por ultimo se añade un archivo de tests para preparar los unit tests del proyecto.

En esta ocasión no hay cambios visibles en la ejecución ya que todo se almacena en variables internas.

Para probar el codigo es necesario proveer un archivo de texto como parámetro al momento de hacer la ejecución.

## Avance 3
Para este tercer avance se generaró el código de expresiones aritmeticas y estatutos secuenciales para asignación, operaciones, lecturas, comparaciones, operadores booleanos, entre otros.
Tambien se generó el código para los estatutos condicionales lineales para decisiones (IF, IF/ELSE).
Para lo mencionado anteriormente se generaron los cuadruplos correspondientes y al ejecutar el programa se imprimen en pantalla los cuadruplos generados.

*Ejemplo*

    python3 MyRLike_parse.py tests/parser/testValid.txt
Donde ***testValid.txt*** es la ruta del archivo a analizar.
