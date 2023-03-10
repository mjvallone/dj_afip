import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


MY_CUIT='change-me'
MY_PASSWORD = 'change-me'
MY_SOCIAL_SERVICE = 'change-me'

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
print("Child window title: " + driver.title)

links = driver.find_elements(By.TAG_NAME, 'a')
for link in links:
  # print(f'text: {link.text} - href: {link.get_attribute("href")} - link: {link.get_attribute("target")}')
  if "Declaración Jurada" in link.text:
    link.click()

time.sleep(5)

form = driver.find_element(By.NAME, "formAgregar")
form.submit()
time.sleep(5)


prepaga_btn = driver.find_element(By.ID, "btnEleccionOOSS")
# FIXME por alguna razon al clickear este boton no abre el modal, ventana
prepaga_btn.click()

# modal = driver.find_element(By.ID, "modal-default")

dropdown = driver.find_element(By.ID, "listOOSS")
select = Select(dropdown)
print(f"len(select.options): {len(select.options)}")
for opt in select.options:
  print(opt.text)
# select.select_by_value("113366")
time.sleep(10)

close_btn = driver.find_element(By.ID, "btnModalCerrar")
close_btn.click()

# search_prepaga = driver.find_element(By.CLASS_NAME, "select2-search__field")
# search_prepaga.send_keys(MY_SOCIAL_SERVICE)
# search_prepaga.select_by_index(1)


aceptadj_form = driver.find_element(By.NAME, "aceptadj")
select = Select(aceptadj_form)
select.select_by_value('1')

aceptacruce_form = driver.find_element(By.NAME, "aceptacruce")
select = Select(aceptacruce_form)
select.select_by_value('1')
time.sleep(5)

# main_form = driver.find_element(By.ID, "formDj")
# main_form.submit()
# time.sleep(5)

#TODO hacer captura de pantalla y mandar wp para chequear que se hizo?