# dj_afip
Este código fue hecho para automatizar la generación de la declaración jurada mensual que se debe hacer en la AFIP para que no te aumenten el valor de la prepaga si tenés ingresos menores a un cierto monto.

## Para correrlo
Antes que nada recuerda configurar tus datos en settings.py

Si usas Chrome, deberías instalar los drivers para poder correr Selenium acordes a tu versión de navegador (versiones de chromedriver: https://chromedriver.chromium.org/downloads)

1. Crear virtualenv

        virtualenv env

2. Activar la virtualenv

        source venv/bin/activate

3. Instalar requerimientos de python

        pip install -r requirements.txt

4. Correr el script

        python generar_dj_afip.py
