# Architecture Decision Records

## ADR-001: Separar el pipeline en tres capas (Ingestion, Transformation, Analysis)

**Estado:** Aceptado

**Contexto:**
Se necesita procesar event logs de un sistema de colaboración de documentos, transformarlos en un modelo analítico y permitir la exploración de métricas.

**Decisión:**
Dividir el proyecto en tres capas independientes:
- **Ingestion:** lectura de eventos crudos y almacenamiento intermedio en MongoDB.
- **Transformation:** modelado relacional en PostgreSQL con arquitectura medallion (raw → trusted → marts).
- **Analysis:** notebook Jupyter para exploración de métricas.

**Consecuencias:**
- Cada capa tiene una responsabilidad clara y puede evolucionar por separado.
- La separación facilita reemplazar componentes individuales (ej. sustituir la ingestion por un consumer de Kafka real).

---

## ADR-002: Usar MongoDB como buffer intermedio simulando un tópico de Kafka

**Estado:** Aceptado

**Contexto:**
El `LogReader` simula un consumer de Kafka leyendo eventos uno por uno desde archivos JSON. Se necesitaba un almacenamiento intermedio que desacople la lectura de archivos del procesamiento hacia PostgreSQL.

**Decisión:**
Usar MongoDB como buffer intermedio: los eventos se insertan uno a uno en una colección y luego un proceso separado los lee, valida, deduplica y escribe en PostgreSQL.

**Consecuencias:**
- Desacopla ingestion de transformation, permitiendo que cada etapa corra de forma independiente.
- La colección de MongoDB se vacía tras cada procesamiento exitoso, simulando el comportamiento de consumo de un tópico.
- Queda acoplada la validación/deduplicación al proceso de escritura a PostgreSQL; idealmente serían procesos separados.

**Mejoras futuras:**
- Montar un Kafka real con un producer que publique los eventos y un consumer que escuche el tópico y los almacene.
- Separar validación y deduplicación en un step dedicado.

---

## ADR-003: Arquitectura medallion (raw → trusted → marts) con modelado 3FN

**Estado:** Aceptado

**Contexto:**
Los eventos crudos necesitan transformarse en un modelo relacional que permita análisis eficientes sobre usuarios, documentos y sesiones.

**Decisión:**
Implementar una arquitectura medallion de tres capas en PostgreSQL:
- **Raw:** eventos aplanados tal como llegan, sin transformación.
- **Trusted:** modelado relacional en 3FN con tablas de `users`, `documents` y `events`, incluyendo métricas agregadas.
- **Marts:** vistas analíticas con lógica de negocio (ej. cálculo de sesiones con ventana de 30 minutos).

**Consecuencias:**
- El modelo relacional en trusted permite queries eficientes con integridad referencial.
- Los marts encapsulan la lógica de negocio, aislándola del modelado base.
- Las transformaciones se ejecutan mediante scripts SQL en orden secuencial.

**Mejoras futuras:**
- Migrar las transformaciones a dbt para gestionar dependencias, testing, data contracts, documentación y semantic layer.
- Evaluar una BD columnar (Redshift, Snowflake) para escala analítica.

---

## ADR-004: PostgreSQL como almacenamiento analítico

**Estado:** Aceptado

**Contexto:**
Se necesita una base de datos que soporte el modelo relacional con integridad referencial y permita queries analíticos sobre los datos transformados.

**Decisión:**
Usar PostgreSQL como base de datos analítica para almacenar las capas raw, trusted y marts.

**Consecuencias:**
- Soporte completo de SQL, schemas, foreign keys y window functions necesarias para el cálculo de sesiones.
- Adecuado para el volumen actual de datos del challenge.
- No escala horizontalmente como soluciones columnares para grandes volúmenes de datos.

**Mejoras futuras:**
- Para escala productiva, migrar a una BD columnar (Redshift, Snowflake, BigQuery) alineando el proceso de carga a las necesidades de freshness de los casos de uso (batch o streaming).

---

## ADR-005: Transformaciones SQL directas en vez de un framework de orquestación

**Estado:** Aceptado

**Contexto:**
Las transformaciones de raw a trusted y marts se implementan como scripts SQL ejecutados secuencialmente desde Python.

**Decisión:**
Ejecutar los scripts SQL directamente desde Python en orden fijo, sin usar un framework de orquestación de transformaciones.

**Consecuencias:**
- Simplicidad de implementación para el alcance del challenge.
- Difícil de mantener a medida que crecen las dependencias entre modelos.
- No hay gestión automática de dependencias, testing integrado ni documentación de linaje.

**Mejoras futuras:**
- Adoptar dbt para orquestar transformaciones, que provee: gestión de dependencias (DAG), testing, data contracts, documentación, semantic layer y versionado de modelos.
