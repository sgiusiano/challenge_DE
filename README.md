# Pipeline ETL de Eventos de Documentos

Este proyecto implementa un pipeline ETL completo para procesar logs de eventos. Extrae logs en formato JSON, los transforma y los carga en PostgreSQL para su análisis. El entorno completo está containerizado con Docker.

## Requisitos Previos
*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

## Configuración y Ejecución

1.  **Crear archivo de entorno:**
    Copia el archivo de ejemplo.
    ```bash
    cp .env.example .env
    ```
2.  **Añadir datos:**
    Asegúrate de que tus archivos de logs JSON estén en la carpeta `data/events/`.

3.  **Ejecutar el Pipeline:**
    Inicia Docker desktop
    Este comando construye las imágenes y levanta todos los servicios (Python, PostgreSQL, MongoDB, Jupyter).
    ```bash
    docker-compose up --build
    ```
## Acceso a Servicios
*   **JupyterLab**:
    *   URL: `http://localhost:8888`
    Pide un token que se puede encontrar en los logs de la terminal, donde también se encuentra una URL cn el token incluido para clickear y acceder.
    una vez en el notebook, en caso de haber cambiado  parametros de user y pass en .env deberas hacerlo en una celda, luego run > all cells.
* **PostgreSQL**
    Si dispone de la herramienta de administracion de postgreSQL puede conectar con la DB utilizando la cadena de conexión que se encuentra en la jupyterNotebook para hacer queries sobre las tablas creadas.
