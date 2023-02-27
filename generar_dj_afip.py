import time
from selenium import webdriver
from selenium.webdriver.common.by import By

MY_CUIT='change-me'
MY_PASSWORD = 'change-me'

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
time.sleep(2)

## WIP no aparece el boton para generar la DJ, asi que a esperar  ##
# dj_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Declaración Jurada')]")
# dj_button = driver.find_element(By.CSS_SELECTOR, 'div.col-xs-12')
# dj_button.click()
time.sleep(5)
dj_button2 = driver.find_element(By.CSS_SELECTOR, 'div.col-xs-12').find_element(By.XPATH, "//span[contains(text(), 'Declaraciones Juradas')]")
dj_button2.click()
time.sleep(5)
# form = driver.find_element(By.name, "formAgregar")
# form.submit()
