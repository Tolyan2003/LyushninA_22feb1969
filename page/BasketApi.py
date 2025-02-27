import json
import allure
from allure_commons.types import AttachmentType

from config import Config


@allure.feature('Корзина')
class BasketAPI:
    def __init__(self, session):
        self.session = session

    @allure.step("Добавление товара в корзину")
    def add_to_basket(self, product_id):
        with allure.step(f"Подготовка данных для добавления товара {product_id}"):
            data = {"data": json.dumps({
                "idCookie": self.session.cookies.get('basketor'),
                "idProd": product_id,
                "type": "add"
            })}

            # Добавляем логирование данных
            allure.attach(
                json.dumps(data, indent=2),
                name="Запрос на добавление товара",
                attachment_type=AttachmentType.JSON
            )

        with allure.step("Отправка запроса на добавление товара"):
            response = self.session.post(
                Config.BASE_URL + Config.ORDER_ENDPOINT,
                data=data
            )

            # Добавляем ответ сервера в отчет
            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=AttachmentType.TEXT
            )

        return response

    @allure.step("Просмотр товара в корзине")
    def get_basket(self):
        with allure.step("Подготовка данных для запроса корзины"):
            data = {"data": json.dumps({
                "idCookie": self.session.cookies.get('basketor'),
                "type": "list"
            })}

            allure.attach(
                json.dumps(data, indent=2),
                name="Запрос на просмотр корзины",
                attachment_type=AttachmentType.JSON
            )

        with allure.step("Отправка запроса на просмотр корзины"):
            response = self.session.post(
                Config.BASE_URL + Config.LIST_ENDPOINT,
                data=data
            )

            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=AttachmentType.TEXT
            )

        return response

    @allure.step("Удаление товара из корзины")
    def remove_from_basket(self, product_id):
        with allure.step(f"Подготовка данных для удаления товара {product_id}"):
            data = {"data": json.dumps({
                "idCookie": self.session.cookies.get('basketor'),
                "idProd": product_id,
                "type": "delete"
            })}

            allure.attach(
                json.dumps(data, indent=2),
                name="Запрос на удаление товара",
                attachment_type=AttachmentType.JSON
            )

        with allure.step("Отправка запроса на удаление товара"):
            response = self.session.post(
                Config.BASE_URL + Config.ORDER_ENDPOINT,
                data=data
            )

            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=AttachmentType.TEXT
            )

        return response