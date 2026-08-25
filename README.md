# HERRAMIENTA TECNOLÓGICA PARA EL CONTROL DE MANTENIMIENTO LÓGICO, SEGURIDAD DE DATOS Y GESTIÓN DOCUMENTAL EN LA U.E.A.M. “EL LIBERTADOR”

**Universidad Politécnica Territorial del Estado Aragua "Federico Brito Figueroa"**
*Extensión de Maracay*
**Proyecto Sociotecnológico - Trayecto II**  
*PNF en Informática — Sección 02*

---

## 📌 Contextualización del Proyecto

El proyecto surge de la necesidad de optimizar y resguardar la infraestructura tecnológica de la **Unidad Educativa Autónoma Militar “El Libertador”**, la cual cuenta con un laboratorio de computación y una red local gestionada por Windows Server. 

Actualmente, la administración de las estaciones de trabajo y el control de directivas de seguridad se realizan manualmente, lo que genera cuellos de botella operativos, vulnerabilidades en la privacidad de los datos institucionales y una pérdida de eficiencia en las actividades académicas.

---

## 🛠️ Funciones del Software (Alcance Técnico)

### 1. Módulo de Diagnóstico de Mantenimiento Lógico
* **Descripción:** Módulo automatizado que evalúa el estado técnico y nivel de optimización de la PC local.
* **Proceso Interno:** Captura interactivamente variables del SO (RAM, espacio en disco, procesos en segundo plano) y las procesa mediante un algoritmo de evaluación de umbrales basado en reglas lógicas predefinidas.
* **Salida / Resultado:** 
  * Panel visual con alertas dinámicas por colores en pantalla.
  * Reporte técnico histórico guardado automáticamente en un archivo local de texto plano.

### 2. Módulo de Seguridad de Datos
* **Descripción:** Mecanismo para el resguardo y verificación de la integridad de los documentos institucionales.
* **Proceso Interno:** El usuario selecciona un archivo e introduce una clave secreta. El software calcula la huella digital única (Hash) mediante algoritmos criptográficos y aplica cifrado simétrico sobre los bytes del documento.
* **Salida / Resultado:** 
  * Generación de un archivo protegido con extensión propia para almacenamiento externo en una carpeta segura.
  * Barra de progreso y despliegue del código hash en pantalla.
  * Registro automático de la operación en una bitácora digital en formato `.json`.

### 3. Módulo de Gestión Documental
* **Descripción:** Sistema de flujo, indexación y recuperación en tiempo real de archivos institucionales.
* **Proceso Interno:** Carga de documentos con metadatos (departamento, palabras clave). Incluye un algoritmo de detección de duplicados que renombrará versiones e incrementará automáticamente el contador de versión (ej. de `V1.0` a `V2.0`) en un archivo maestro local.
* **Salida / Resultado:** 
  * Catálogo visual dinámico con búsquedas secuenciales en tiempo real.
  * Recuperación y previsualización de documentos vigentes e históricos.

---

## 💻 Stack Tecnológico

| Componente | Tecnología / Librería | Descripción |
| :--- | :--- | :--- |
| **Backend** | Python + FastAPI | Lógica del sistema, procesamiento criptográfico y API interna |
| **Frontend** | HTML5, CSS3, JavaScript | Interfaz gráfica ejecutable desde el navegador web |
| **Embebido / Desktop** | `Eel` / `Ksgl` | Empaquetado nativo para ejecutar el sistema como aplicativo `.exe` |
| **Base de Datos / Logs** | JSON | Almacenamiento local, metadatos y bitácora de seguridad |
| **Generador de Reportes** | ReportLab / FPDF2 | Exportación de reportes PDF formateados (márgenes, tablas, logos) |

---

## 👥 Equipo de Trabajo y Asignación de Roles

| Integrante | C.I. | Correo Electrónico | Rol en el Proyecto |
| :--- | :--- | :--- | :--- |
| **Abraham Silva** *(Encargado de Logística & Backend/ Dev)* | 32.139.810 | abrahamjesussilvafereira221@gmail.com | **Backend & Criptografía:** Coordinación, integración FastAPI + Eel, algoritmo de cifrado/Hash e integración con el SO. |
| **José Villegas** *(Encargado de UI/UX & Frontend/ Dev)* | 32.597.348 | JooceVillegas@gmail.com | **Frontend UI/UX & Mantenimiento:** Maquetación HTML/CSS/JS, panel visual de alertas y lectura de datos de hardware. |
| **Yender Santamaría** *(Encargado de Control Documental & IT Support/ Dev)* | 33.269.853 | Yendersm2020@gmail.com | **Gestión Documental & PDF:** Algoritmo de versionado (V1.0 a V2.0), almacenamiento JSON y generación de reportes con FPDF2/ReportLab. |

* **Asesor Académico:** Prof. Luis Eduardo Aponte Izaguirre (C.I. 13.780.965)

---

## 📍 Datos de la Comunidad Beneficiada

* **Institución:** Unidad Educativa Autónoma Militar “El Libertador” (U.E.A.M.)
* **Ubicación:** Estado Aragua, Maracay, Municipio Girardot, Parroquia Madre María de San José.
* **Teléfono de Contacto:** 0426-7346203

---

## 🚀 Instrucciones Rápidas para Desarrolladores

1. **Clonar repositorio:**
   ```bash
   git clone [https://github.com/Abrahamsilvabussiness209/ueam_herramienta.git](https://github.com/Abrahamsilvabussiness209/ueam_herramienta.git)
