# TFGVisualizacionBlender
Generación de escenarios urbanos fotorrealistas en Blender usando código Python, contribuyendo a una mejora en la visualización del proyecto de la mesa interactiva creado en 2020 por Ignacio de Rodrigo Tobías, y mejorado en 2022 por David Egea Hernández.

Se lleva a cabo la representación completa en Blender de un caso de uso para un escenario real de movilidad. Esta información procede de un proyecto anterior a este. El entorno urbano seleccionado fue un sector del proyecto Madrid Nuevo Norte, un plan de remodelación urbana para el distrito de Castellana Norte, en la ciudad de Madrid, España. Para ello, se parte de los datos recogidos en los módulos de detección – realizado a partir de la cámara – y simulación – efectuado con el software de simulación de tráfico Aimsun –. Estos resultado fueron reunidos en: tres ficheros con formato JSON para las carreteras, intersecciones y edificios; y un fichero con formato XML para recrear la simulación del tráfico. 

Durante este trabajo se ha utilizado el lenguaje de programación Python, gracias a la importación de la librería “bpy” utilizada para interactuar con el software de modelado 3D Blender. 

Para generar los escenarios urbanos se siguen los siguientes pasos:
- Construcción de calles a partir de la información procedente del módulo de detección de la mesa interactiva. Es necesaria la conversión – mediante el uso del algoritmo de Bézier – de las varias coordenadas que definen inicialmente las carreteras, en cuatro puntos a partir de los cuales se puede obtener una curva en Blender. Para generar el volumen de las calles, a partir de las trayectorias de las curvas de Bézier, se usa la herramienta de los modificadores que posee Blender. Por último, para definir la apariencia deseada de las calles, se prepara un material personalizado mediante la configuración de un árbol de nodos de geometría en Blender.
- Construcción de las intersecciones mediante el uso de modificadores para generar la forma redondeada. Además, se usan los nodos de geometría para crear un material apropiado que se ajuste perfectamente a las intersecciones y a su función de unión entre calles.
- Construcción de los edificios a partir de la biblioteca que ofrece el addon BlenderKit. Se eligen 20 tipos de modelos distintos de edificios creados por la comunidad de usuarios de Blender y por artistas profesionales. Cada modelo se exporta a un archivo en formato OBJ, de manera que esté accesible cuando sea necesario. 
-	Construcción del terreno partiendo de una malla de tipo plano. Para la creación de la forma del terreno se hace uso de la herramienta de sistemas de partículas que ofrece Blender. Por último, se genera un material customizado mediante los nodos de geometría buscando una apariencia realista. 
-	Visualización de la simulación del tráfico mediante la inserción de fotogramas clave en Blender. También ha sido necesaria la creación de una función general que se encargue de calcular el ángulo de giro de los vehículos. Por otro lado, para definir el modelo de los vehículos se ha utilizado el addon BlenderKit.
-	También se añade el fichero ExecuteBlenderOut.py, usado para ejecutar un fichero Python en Blender desde fuera.
-	Por último, mencionar que no se ha podido subir la carpeta que almacena todos los modelos de edificios en formato OBJ debido a que la mayoría son muy pesados.

Finalmente, algunos ejemplos de los resultados obtenido en Blender:
![image](https://github.com/TatianaLB/TFGVisualizacionBlender/assets/98090265/c5c7b1ef-e303-4706-a31d-0929869ec21b)

![image](https://github.com/TatianaLB/TFGVisualizacionBlender/assets/98090265/7f3a0f1f-c922-4055-841c-5a86bb3c8714)

![image](https://github.com/TatianaLB/TFGVisualizacionBlender/assets/98090265/4f0bb53a-3ef7-4592-8d1c-6f115776e90c)
