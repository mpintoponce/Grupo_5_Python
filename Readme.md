# 📊 Dashboard de Cumplimiento de OTs - Proyecto G5

Este proyecto desarrollado en Python y Streamlit permite visualizar de manera dinámica y gráfica el cumplimiento semanal y mensual de las Órdenes de Trabajo (OTs) de mantenimiento en minería.

---

## 🔧 Tecnologías utilizadas

- Python 3.9+
- Streamlit
- Pandas
- Plotly
- Excel (.xlsm)

---

## 📁 Estructura del proyecto

📂 Grupo_5_Python/

├── appv4.py # Código principal de la aplicación Streamlit
├── CUMPLIMIENTO_PLAN.xlsm # Archivo de datos fuente
├── requirements.txt # Dependencias necesarias
└── README.md # Este archivo


---

## ▶️ ¿Cómo ejecutar el proyecto?

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/Grupo_5_Python.git
cd Grupo_5_Python
```

2. Crear un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```
3. Instalar las dependencias
```bash
pip install -r requirements.txt
```
Si necesitas generar el archivo requirements.txt tú mismo, puedes hacerlo con:
```bash
pip freeze > requirements.txt
```
4. Ejecutar la aplicación
```bash
streamlit run appv4.py
```
Esto abrirá automáticamente tu navegador con la aplicación ejecutándose en http://localhost:8501.

## 📸 Vista previa
https://raw.githubusercontent.com/Articjm/PROYECTO_G5/main/CAMION_TR.jpg<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/8f054126-7f12-4b5c-9fe6-9f6f22d375e6" />

## 📌 Funcionalidades principales

- Visualización de cumplimiento de OTs semanal y mensual
- Análisis de OTs correctivas y programadas
- Seguimiento por tipo de componente y flota
- Métricas por flota individual
- Tendencia anual del cumplimiento

## 📂 Fuentes de datos

El archivo CUMPLIMIENTO_PLAN.xlsm contiene las siguientes hojas de cálculo:

- IW38 PLAN SEMANAL
- IW38 SEMANA CAL
- BL MENSUALOT
- CMENSUAL
- RESUMEN ANUAL

## 📞 Contacto

Proyecto elaborado por el Grupo 5 para el curso de Python Avanzado - UTEC.
