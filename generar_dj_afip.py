import datetime
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import settings

# set up webdriver (assuming you have installed ChromeDriver)
driver = webdriver.Chrome()
driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")

# completamos CUIT
cuil_input = driver.find_element(By.ID, "F1:username")
cuil_input.send_keys(settings.MY_CUIT)
submit_button = driver.find_element(By.ID, "F1:btnSiguiente")
submit_button.click()
time.sleep(5)

# completamos PASSWORD
password_input = driver.find_element(By.ID, "F1:password")
password_input.send_keys(settings.MY_PASSWORD)
submit_button = driver.find_element(By.ID, "F1:btnIngresar")
submit_button.click()
time.sleep(5)

# buscamos el servicio MiSSSalud y entramos
search_button = driver.find_element(By.ID, "buscadorInput")
search_button.send_keys("misssalud")
time.sleep(2)
misalud_button = driver.find_element(By.ID, "rbt-menu-item-0")
misalud_button.click()
time.sleep(5)

#get current window handle
p = driver.current_window_handle

#get first child window
chwd = driver.window_handles

for w in chwd:
#switch focus to child window
    if(w!=p):
      driver.switch_to.window(w)

links = driver.find_elements(By.TAG_NAME, 'a')
for link in links:
  if "Declaración Jurada" in link.text:
    link.click()

time.sleep(5)

form = driver.find_element(By.NAME, "formAgregar")
form.submit()
time.sleep(5)


prepaga_btn = driver.find_element(By.ID, "btnEleccionOOSS")
prepaga_btn.click()

time.sleep(5)

listOOSS = Select(driver.find_element(By.ID, "listOOSS"))

print(f"Total de opciones de prepaga: {len(listOOSS.options)}")
if settings.MY_SOCIAL_SERVICE_ID == '':
  with open('obras_sociales.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['codigo', 'nombre_obra_social']) #header row
    
    for opt in listOOSS.options:
      value = opt.get_attribute("value")
      if settings.MY_SOCIAL_SERVICE_NAME in opt.text.lower():
        print(f"Tu posible obra social podria ser: {value} - {opt.text}")
      if settings.MY_SOCIAL_SERVICE_ID == '':
        writer.writerow([value, opt.text])
      elif settings.MY_SOCIAL_SERVICE_ID == value:
        print(f"SELECCIONADA: {value}  ||  {opt.text}")

  # MUERE ACA SI NO HAY OS CONFIGURADA!
  print(f"Se genero un archivo con el listado de obras sociales, dicho archivo llama {os.getcwd()}/obras_sociales.csv.")
  print("Buscar en el archivo el codigo de la obra social que te corresponde y configurar 'MY_SOCIAL_SERVICE_ID' con dicho valor!")
  exit()

listOOSS.select_by_value(settings.MY_SOCIAL_SERVICE_ID)
time.sleep(2)

driver.find_element(By.ID, "btnElegirOOSS").click()
time.sleep(2)

aceptadj_form = driver.find_element(By.NAME, "aceptadj")
select = Select(aceptadj_form)
select.select_by_value('1')
time.sleep(2)

aceptacruce_form = driver.find_element(By.NAME, "aceptacruce")
select = Select(aceptacruce_form)
select.select_by_value('1')
time.sleep(2)

aceptar_button = driver.find_element(By.NAME, "aceptar")
aceptar_button.click()
print("Esperando 10 segundos para aceptar y confirmar la DJ..")
time.sleep(10)

confirmar_button = driver.find_element(By.NAME, "aceptar")
confirmar_button.click()
time.sleep(3)

driver.maximize_window()
time.sleep(2)

now = datetime.datetime.now()
file_date = f"{now.month}-{now.year}"
driver.save_screenshot(f"{settings.SCREENSHOT_PATH}/AFIP-OS-DJ-{file_date}.png")
print("Screenshot guardado en: ", f"{settings.SCREENSHOT_PATH}/AFIP-OS-DJ-{file_date}.png")
