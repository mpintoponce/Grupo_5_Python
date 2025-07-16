# Programa de Mantenimiento Semanal

## Overview

**Programa de Mantenimiento Semanal** es una herramienta interactiva desarrollada en Streamlit que permite visualizar, analizar y exportar datos relacionados con el cumplimiento de mantenimiento preventivo y correctivo. La aplicación se conecta directamente a un archivo Excel hospedado en GitHub, y permite navegar entre secciones como: cumplimiento semanal, backlogs y componentes.

Está diseñada para apoyar la toma de decisiones operativas mediante reportes visuales claros, KPIs de cumplimiento, y exportación de resultados a PDF.

---

## Folder Structure

```
PROYECTO_G5/
│
├── assets/                          # Imágenes y recursos estáticos
├── data/                            # Archivos temporales o ejemplos
├── utils/                           # Módulos auxiliares
│   ├── data_loader.py               # Carga y limpieza de datos desde Excel
│   ├── charts.py                    # Generación de gráficos
│   ├── export_pdf.py                # Exportación de reportes a PDF
│
├── pages/                           # Páginas adicionales si se usa Streamlit multipágina
│   ├── cumplimiento.py              # Cumplimiento del plan semanal
│   ├── backlogs.py                  # Visualización de backlogs
│   ├── componentes.py               # Análisis por tipo de componente
│
├── main.py                          # Página principal con navegación e imagen inicial
├── requirements.txt                 # Dependencias del proyecto
└── README.md                        # Documentación
```

---

## Features

- 📥 **Carga Automática de Excel:** Obtiene el archivo directamente desde GitHub.
- 📊 **Visualización de Cumplimiento:** Gráficos por flota y estado de órdenes (cerradas, reprogramadas, abiertas).
- 📁 **Análisis de Backlogs y Componentes:** Filtrado por tipos de orden y por flota.
- 📄 **Exportación a PDF:** Reporte multipágina con todos los gráficos generados.
- 🌙 **Interfaz oscura y moderna:** Fondo negro, sin menú lateral izquierdo, navegación desde el lado derecho.

---

## Project Structure

Este proyecto se divide en tres grandes componentes:

- **Frontend:** Interfaz en Streamlit, moderna y adaptable.
- **Backend Lógico:** Procesamiento de datos, análisis y generación de gráficos.
- **Repositorio de Datos:** Excel ubicado en [GitHub - PROYECTO_G5](https://github.com/Articjm/PROYECTO_G5)

---

## Documentación de Archivos

### Principal

- `main.py`: Página inicial con imagen de portada y botones de navegación.

### Utilidades

- `data_loader.py`: Carga y transforma los datos desde las hojas del Excel (`IW38 PLAN SEMANAL`, `IW38 SEMANA CAL`, etc.).
- `charts.py`: Crea gráficos de torta y barras por estado y flota.
- `export_pdf.py`: Exporta todos los gráficos generados a un archivo PDF multipágina.

### Páginas

- `cumplimiento.py`: Visualiza cumplimiento del mantenimiento semanal.
- `backlogs.py`: Muestra los atrasos (backlogs) mensuales.
- `componentes.py`: Analiza órdenes por componente o tipo de mantenimiento.

---

## Getting Started

### Prerequisitos

- Python 3.10 o superior
- Pip
- Streamlit (`pip install streamlit`)

### Instalación

```bash
git clone https://github.com/Articjm/PROYECTO_G5.git
cd PROYECTO_G5
pip install -r requirements.txt
streamlit run main.py
```

---

## Uso

1. **Inicio:** Se muestra una imagen con tres botones: `Cumplimiento Plan Semanal`, `Backlogs` y `Componentes`.
2. **Navegación:** Al hacer clic en cada botón, accedes a una sección distinta con sus respectivos análisis.
3. **Carga Automática de Datos:** El Excel `CUMPLIMIENTO PLAN.xlsm` se carga desde GitHub automáticamente.
4. **Exportar PDF:** En cada sección puedes generar un reporte PDF con todos los gráficos generados.

---

## Tecnologías

- **Frontend:** Streamlit
- **Análisis y Gráficos:** Pandas, Matplotlib
- **Exportación:** Matplotlib + PdfPages
- **Datos:** Excel `.xlsm` desde GitHub

---

## Ejemplo de Archivo Excel Esperado

- Nombre: `CUMPLIMIENTO PLAN.xlsm`
- Hojas requeridas:
  - `IW38 PLAN SEMANAL`
  - `IW38 SEMANA CAL`
  - `BL MENSUALOT`
  - `CMENSUAL`

---

## Autor

Desarrollado por [Articjm](https://github.com/Articjm)  
Repositorio: [https://github.com/Articjm/PROYECTO_G5](https://github.com/Articjm/PROYECTO_G5)
