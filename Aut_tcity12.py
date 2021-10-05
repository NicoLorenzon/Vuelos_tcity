from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime


class BuscadorVuelos:

    def set_driver(self):
        '''
        set_driver define el navegador y parámentros de lanzamiento
        '''
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--incognito')
        self.driver = webdriver.Chrome(executable_path='D:/Escritorio/DS/Proyectos/VuelosScrap/chromedriver.exe', options=chrome_options)

    def set_pagina(self):
        '''
        set_pagina trae el driver y ejecuta la página a buscar
        '''
        driver = self.driver
        driver.get('https://www.turismocity.com.ar/')
        time.sleep(2)

    def establecer_Vuelo(self):
        '''
        Función establecer_vuelo: En esta función, luego de abrir la página en el paso anterior, comienza la búsqueda.
        En el primer, se crea la variable buscador, donde recibe el código html de las cajas de búsqueda.
        En segundo lugar se define la variable origen_vuelo, que trae el primer elemento de la variable buscador e ingresa el string "Eze".
        Luego busca la opción correcta y da click.
        Para la vaariable destino, es el mismo procedimiento que la variable origen_vuelo, pero en esta se establece "Mex" como string,
        para así encontrar el destino deseado.
        Luego, se busca dentro del DataPicker las fechas deseadas (ESTE PASO VA A VARIAR SEGÚN LOS MESES VAYAN PASANDO).
        Selecciona las fechas, en este caso 01/20/2022 hasta 07/20/2022
        Finalmente busca el vuelo.
        Dentro del bloque try-except, se busca cerrar una ventana de inicio de sesión, que suele salir algunas veces sí y otras no.
        '''
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[2]/div/div/div').click()
        buscador = driver.find_elements_by_css_selector('input[type="search"]')
        origen_vuelo = buscador[0]
        time.sleep(3)
        origen_vuelo.send_keys('Eze')
        time.sleep(2)
        origen_vuelo.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[2]/div/div/span/span/span[2]/ul/li/div[2]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[3]/div/div/div').click()
        destino_vuelo = buscador[1]
        destino_vuelo.send_keys('Mex')
        time.sleep(2)
        destino_vuelo.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[3]/div/div/span/span/span[2]/ul/li[1]/div[2]').click()
        time.sleep(2)
        # Seleccionar fecha de ida
        data_picker = driver.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[4]/div/div[1]/div')
        data_picker.click()
        pasar_mes = driver.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[4]/div/div[1]/div[2]/div/div[2]/div[1]/a[2]')
        pasar_mes.click()
        pasar_mes.click()
        dia_ida = driver.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[4]/div/div[1]/div[2]/div/div[2]/div[1]/div/div[5]/div[1]/div[6]/div[4]')
        dia_ida.click()
        # Fecha de vuelta
        pasar_mes.click()
        pasar_mes.click()
        pasar_mes.click()
        pasar_mes.click()
        pasar_mes.click()
        pasar_mes.click()
        dia_vuelta = driver.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[2]/div/div[4]/div/div[1]/div[2]/div/div[2]/div[1]/div/div[11]/div[1]/div[6]/div[3]') # Selecciona el DIV del 20 de Julio
        dia_vuelta.click()
        time.sleep(2)
        boton_buscar_vuelo = driver.find_element_by_xpath('//*[@id="flights-tab-container"]/form/div[5]/div/input')
        boton_buscar_vuelo.click()
        time.sleep(30)
        try:
            cerrar_anuncio = driver.find_element_by_xpath('//*[@id="modalLoginImagePopUp"]/div[1]/a')
            cerrar_anuncio.click()
        except:
            pass

    def obtener_link(self):
        '''
        Esta función lo que hace es copiar el url de la búsqueda realizada y copiarlo  dentro de un archivo de texto
        el cual va a ser enviado por email de manera automática.
        '''
        driver = self.driver
        link_oferta = driver.current_url
        with open('Link de ofertas Ezeiza-Ciudad de Mexico.txt', 'a', encoding='utf8') as archivo:
            archivo.write(f'Link del día {datetime.date.today()} \n{link_oferta}\n\n')
        driver.close()

if __name__ == '__main__':
    buscador = BuscadorVuelos()
    buscador.set_driver()
    buscador.set_pagina()
    buscador.establecer_Vuelo()
    buscador.obtener_link()
#########################################################################################

'''
A partir de este punto se configura y desarrolla el script para que una vez que se obtenga 
el archivo .txt con el link de vuelos se envíe automaticamente vía mail.
'''
import smtplib, ssl, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

# Login, asunto, destinatario
usuario = '*******@gmail.com'
password = '******'
destinatario = '********@hotmail.com'
asunto = 'Link de Vuelos'

# Configuración del mensaje 
mensaje = MIMEMultipart('alternative')
mensaje['subject'] = asunto
mensaje['From'] = usuario
mensaje['To'] = destinatario

# Archivo a enviar
archivo = 'Link de ofertas Ezeiza-Ciudad de Mexico.txt'

# Adjuntar el archivo
with open(archivo, "rb") as adjunto:
    contenido_adjunto = MIMEBase('application', 'octet-stream')
    contenido_adjunto.set_payload(adjunto.read())

# Encoding base 64 para no tener error de lectura
encoders.encode_base64(contenido_adjunto)

contenido_adjunto.add_header(
    "Content-Disposition",
    f"attachment; filename= {archivo}",
)

# Archivo del mensaje a string
mensaje.attach(contenido_adjunto)
mensaje_final= mensaje.as_string()

# Crea la conexion segura, hace Login y envía el mail.
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(usuario,password)
    server.sendmail(usuario, destinatario,mensaje_final)
