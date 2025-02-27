from time import sleep
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from DataProvider import DataProvider


class BasketPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.data = DataProvider()
        self.url = self.data.URL

    @allure.step("Перейти на страницу магазина")
    def go(self):
        with allure.step('Открытие URL: "https://www.sibdar-spb.ru"'):
            self.driver.get("https://www.sibdar-spb.ru")

        with allure.step("Поиск элемента вкладки"):
            element = self.driver.find_element(By.XPATH, "//*[@id='tab1']")

        with allure.step("Ожидание видимости элемента"):
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of(element)
            )

        with allure.step("Прокрутка к элементу"):
            self.driver.execute_script("arguments[0].scrollIntoView();", element)

        with allure.step("Стабилизационная задержка"):
            sleep(1)

    @allure.step("Добавление товара в корзину")
    def add_to_basket(self, p_id):
        with allure.step(f"Поиск кнопки добавления товара {p_id}"):
            element = self.driver.find_element(
                By.CSS_SELECTOR,
                "#bx_3218110189_204 > div.tabs-item-info > button"
            )
            element.click()

        with allure.step("Ожидание и клик по кнопке корзины"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/a'))
            ).click()

            sleep(5)

    @allure.step("Авторизация")
    def login(self, username, number):
        with allure.step("Ожидание поля ввода имени"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/a'))
            ).click()

        with allure.step("Ввод имени"):
            element = self.driver.find_element(
                By.CSS_SELECTOR,
                "input.req_bask.name_order_bask[name='Имя']"
            )
            element.send_keys(username)

        with allure.step("Ввод телефона"):
            element = self.driver.find_element(
                By.CSS_SELECTOR,
                "input.phone_order_bask[type='tel']"
            )
            element.send_keys(number)

        with allure.step("Стабилизационная задержка"):
            sleep(5)

    @allure.step("Изменение количества товара в корзине")
    def change_to_basket(self):
        with allure.step("Увеличение количества товара"):
            element_plus = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "span.plus_prod[onclick*='204']"
                ))
            )
            element_plus.click()
            element_plus.click()

            with allure.step("Стабилизационная задержка"):
                sleep(5)

        with allure.step("Уменьшение количества товара"):
            element_minus = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "span.minus_prod[onclick*='204']"
                ))
            )
            element_minus.click()

        with allure.step("Стабилизационная задержка"):
            sleep(5)

        with allure.step("Получение стоимости товара"):
            price = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#price_ti_204.price_ti"))
            )

        with allure.step("Возврат элемента с ценой"):
            return price

    @allure.step("Удаление товара из корзины")
    def delete_to_basket(self):
        with allure.step("Ожидание кнопки удаления товара"):
            element_del = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "button[onclick='deleteCardItem(this, 204)']"
                ))
            )

        with allure.step("Клик по кнопке удаления"):
            element_del.click()

        with allure.step("Стабилизационная задержка"):
            sleep(3)

