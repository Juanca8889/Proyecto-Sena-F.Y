from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time

# Configuración del driver
def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

# Test de login contra servidor Flask
def test_formulario_servidor():
    driver = setup_driver()
    try:
        # 👉 Aquí apuntas a tu servidor Flask
        driver.get("http://127.0.0.1:5000/login")

        print("⏳ Esperando a que el formulario de login esté listo...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        print("✅ Formulario cargado")

        # Llenar usuario y contraseña
        campos = [
            ("username", "admin", "Usuario"),
            ("password", "1234", "Contraseña")
        ]
        for campo_id, valor, nombre in campos:
            campo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, campo_id))
            )
            campo.clear()
            campo.send_keys(valor)
            print(f"✅ {nombre} llenado")

        # Click en el botón Ingresar
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.save_screenshot("antes_login.png")
        login_button.click()
        print("🖱️ Botón de login clickeado")

        # Esperar a que redirija (ej: a /dashboard o /productos)
        try:
            WebDriverWait(driver, 10).until(
                EC.url_changes("http://127.0.0.1:5000/login")
            )
            print("✅ Redirección detectada")
        except TimeoutException:
            print("⚠️ No hubo redirección después del login")

        time.sleep(2)
        driver.save_screenshot("despues_login.png")
        print("📸 Screenshots guardados")

    except TimeoutException as e:
        print(f"❌ Timeout esperando elemento: {e}")
    except Exception as e:
        print(f"💥 Error en la prueba: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_formulario_servidor()
