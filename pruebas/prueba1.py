from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tabulate import tabulate
import time


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    try:
        # Abrir la página oficial de Python
        driver.get("http://127.0.0.1:5000/Admin")


        time.sleep(2)  # esperar que cargue


        # 1. Verificar el título
        titulo_pagina = driver.title
        print("=" * 50)
        print("📌 TÍTULO DE LA PÁGINA")
        print("=" * 50)
        print(titulo_pagina, "\n")


        # 2. Extraer los eventos próximos de la página principal
        eventos = driver.find_elements(By.CSS_SELECTOR, ".event-widget li")
        eventos_data = []
        for evento in eventos:
            titulo = evento.text
            enlace = evento.find_element(By.TAG_NAME, "a").get_attribute("href")
            eventos_data.append([titulo, enlace])


        print("=" * 50)
        print("📌 PRÓXIMOS EVENTOS")
        print("=" * 50)
        print(tabulate(eventos_data, headers=["Evento", "Enlace"], tablefmt="grid"))
        print()


        # 3. Extraer noticias destacadas
        noticias = driver.find_elements(By.CSS_SELECTOR, ".list-recent-posts li")
        noticias_data = []
        for noticia in noticias:
            titulo = noticia.find_element(By.TAG_NAME, "a").text
            enlace = noticia.find_element(By.TAG_NAME, "a").get_attribute("href")
            noticias_data.append([titulo, enlace])


        print("=" * 50)
        print("📌 NOTICIAS RECIENTES")
        print("=" * 50)
        print(tabulate(noticias_data, headers=["Noticia", "Enlace"], tablefmt="grid"))


    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    main()
