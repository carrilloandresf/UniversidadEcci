# Repositorio de Talleres de la Universidad ECCI

Este repositorio contiene los talleres organizados por cursos de la universidad. Cada curso tiene su propia carpeta y dentro de cada carpeta de curso se encuentran las carpetas de los talleres. Los archivos de las tareas se encuentran dentro de las carpetas de los talleres.

## Configuración del Entorno Virtual

Para garantizar que todas las dependencias necesarias están instaladas y evitar conflictos con otras librerías de Python en tu sistema, es recomendable usar un entorno virtual. A continuación, se muestra cómo configurar un entorno virtual y instalar las librerías necesarias:

1. **Instalar `virtualenv` si no lo tienes:**

   ```bash
   pip install virtualenv
   ```

2. **Crear un entorno virtual:**
   ```bash
   virtualenv venv
   ```

3. **Activar el entorno virtual:**
    - **En Windows**
    ```bash
    venv\Scripts\activate
    ```

    - **En macOS y Linux:**
    ```bash
    source venv/bin/activate
    ```

4. **Instalar las librerías necesarias desde requirements.txt:**
    ```python
    pip install -r requirements.txt
    ```

5. **Desactivar el entorno virtual:**
    Una vez que hayas terminado de trabajar, puedes desactivar el entorno virtual con el siguiente comando:
    ```bash
    deactivate
    ```

De esta manera, los colaboradores del proyecto podrán instalar todas las dependencias necesarias de forma rápida y sencilla.



## Estructura del Repositorio

La estructura del repositorio es la siguiente:


## Cursos

### Algoritmos de Robótica

- **Taller 1 – Python (código)**
  - **A. Sin interacción de consola**
    1. `Punto1.py`: Realice un programa que sume, reste, multiplique (producto punto y producto cruz) y divida dos vectores previamente inicializados.
    2. `Punto2.py`: Realice un programa que sume, reste, multiplique (producto punto y producto cruz) y divida dos matrices previamente inicializadas.
    3. `Punto3.py`: Realice un programa que convierta coordenadas rectangulares a cilíndricas y esféricas, para lo cual deben consultar sobre el uso de funciones trigonométricas en Python.
    4. `Punto4.py`: Realice un programa para el cálculo de la resistencia de una RTD de platino (PT100) en función de la temperatura.
    5. `Punto5.py`: Realice en funciones las rotaciones en X, Y y Z, donde se tenga un parámetro de entrada (ángulo) y un parámetro de salida (matriz).
    6. `Punto6.py`: Realice un programa que calcule la fuerza de avance y retroceso de un cilindro neumático de doble efecto. Debe establecer previamente los valores de presión, así como las dimensiones físicas del cilindro para realizar el cálculo.

  - **B. Con interacción de consola (fprintf o disp) y teclado (input)**
    1. `Punto7.py`: Realice un programa que calcule la potencia que consume un circuito ingresando por teclado el valor de corriente y voltaje.
    2. `Punto8.py`: Realice un programa que calcule X números aleatorios en un rango determinado por el usuario.
    3. `Punto9.py`: Realice un programa para el cálculo de volúmenes (Prisma, Pirámide, Cono truncado, Cilindro) donde el usuario pueda seleccionar el sólido y los parámetros de cada volumen.
    4. `Punto10.py`: Realice un programa que le permita al usuario escoger entre robot Cilíndrico, Cartesiano y esférico, donde como respuesta a la selección conteste con el tipo y número de articulaciones que posee.
    5. `Punto11.py`: Escribir un programa que realice la pregunta ¿Desea continuar Si/No? y que no deje de hacerla hasta que el usuario teclee No.

  - **C. Uso de las funciones para graficar**
    1. `Punto12.py`: Realice un programa que grafique el comportamiento de un sensor PT100 desde -200°C a 200°C.
    2. `Punto13.py`: Realice un programa que le permita al usuario ingresar los coeficientes de una función de transferencia de segundo orden y graficar su comportamiento, además se debe mostrar qué tipo de sistema es: subamortiguado, críticamente amortiguado y sobreamortiguado.
    3. `Punto14.py`: Implemente la ecuación de carga y descarga para un circuito RC. El usuario ingresa por teclado el valor de voltaje (V), capacitancia (𝜇F) y resistencia (Ω). Posteriormente realice en Python la gráfica.
    4. `Punto15.py`: Consulte y elabore un sistema coordenado X, Y y Z donde se dibuje un vector con coordenadas ingresadas por el usuario.
    5. `Punto16.py`: Dibuje el nombre de cada uno de los integrantes del grupo en un plot en 2D, teniendo en cuenta líneas rectas y/o curvas.
    6. `Punto17.py`: Obtenga las coordenadas X y Y de los contornos de dos logos de automóviles (Chevrolet, Hyundai, Mazda, etc.), a través de Python.


## Contribuyentes

Este repositorio ha sido creado y es mantenido por los siguientes estudiantes:

1. [Andrés Felipe Carrillo Rodríguez](mailto:daniela.rodriguezpe@ecci.edu.co)
2. [Daniela Rodríguez Pelaez](mailto:andresf.carillor@ecci.edu.co)
3. [Jeisson Gutierrez Sanchez](mailto:jeisson.gutierrezs@ecci.edu.co)
4. [William Alejandro Fernandez Pinzon](williama.fernandezp@ecci.edu.co)

## Cómo Contribuir

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b nueva-rama`).
3. Realiza los cambios necesarios y haz commit (`git commit -m 'Añadir nueva característica'`).
4. Envía los cambios a tu fork (`git push origin nueva-rama`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
