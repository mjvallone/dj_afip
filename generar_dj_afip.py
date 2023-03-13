import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

########## CONFIGURAR ACA ########## 
MY_CUIT='change-me'
MY_PASSWORD = 'change-me'
MY_SOCIAL_SERVICE = '' # Correr con este valor vacio para obtener el listado de OSs por consola!
# MY_SOCIAL_SERVICE = '113366' #(omint)
SCREENSHOT_PATH = '/home/change-user/Desktop'
####################################

# set up webdriver (assuming you have installed ChromeDriver)
driver = webdriver.Chrome()
driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")

# completamos CUIT
cuil_input = driver.find_element(By.ID, "F1:username")
cuil_input.send_keys(MY_CUIT)
submit_button = driver.find_element(By.ID, "F1:btnSiguiente")
submit_button.click()
time.sleep(5)

# completamos PASSWORD
password_input = driver.find_element(By.ID, "F1:password")
password_input.send_keys(MY_PASSWORD)
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
for opt in listOOSS.options:
  value = opt.get_attribute("value")
  if MY_SOCIAL_SERVICE == '':
    print(f"valor: {value}  ||  texto: {opt.text}")
  elif MY_SOCIAL_SERVICE == value:
    print(f"SELECCIONADA: {value}  ||  {opt.text}")

# MUERE ACA SI NO HAY OS CONFIGURADA!
if MY_SOCIAL_SERVICE == '':
  print("Buscar en el listado y configurar 'MY_SOCIAL_SERVICE' con el valor que corresponda!")
  exit()

listOOSS.select_by_value(MY_SOCIAL_SERVICE)
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
#TODO Descomentar la linea debajo para confirmarrrrrrrrrr!!
# aceptar_button.click()
time.sleep(5)

#TODO mejorar captura de pantalla full-screen y mandar wp para chequear que se hizo?
driver.save_screenshot(SCREENSHOT_PATH+"/AFIP-OS-DJ.png")
print("Screenshot guardado en: ", SCREENSHOT_PATH+"/AFIP-OS-DJ.png")
