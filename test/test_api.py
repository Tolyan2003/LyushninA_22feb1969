import allure
from config import Config


# Test Data
TEST_PROD_ID = "204"
TEST_COOKIE = "711346"

@allure.story("Проверка cookie")
@allure.severity(allure.severity_level.BLOCKER)
def test_session_cookies(session):
    with allure.step("Первый запрос для инициализации сессии"):
        test_response = session.get('https://www.sibdar-spb.ru/')
        assert test_response.status_code == 200

    with allure.step("Проверяем обновленные cookies"):
        current_cookies = session.cookies.get_dict()
        for cookie_name in Config.REQUIRED_COOKIES:
            assert cookie_name in current_cookies
            print(f"{cookie_name}: {current_cookies[cookie_name]}")


@allure.feature("Управление корзиной")
@allure.story("Добавление товара в корзину")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_to_basket(basket):
    with allure.step("Добавить тестовый товар"):
        response = basket.add_to_basket(TEST_PROD_ID)

    with allure.step("Проверить ответ"):
        assert response.status_code == 200
        print(f"количество товаров в корзине равно {response.text}")

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

@allure.feature("Управление корзиной")
@allure.story("Просмотр содержимого корзины")
@allure.severity(allure.severity_level.CRITICAL)
def test_view_basket(basket):
    with allure.step("Получить содержимое корзины"):
        response = basket.get_basket()

    with allure.step("Проверить ответ"):
        assert response.status_code == 200
        assert "Грузди соленые" in response.text

        allure.attach(response.text, name="Basket Contents", attachment_type=allure.attachment_type.HTML)


@allure.feature("Управление корзиной")
@allure.story("Удаление товара из корзины")
@allure.severity(allure.severity_level.CRITICAL)
def test_remove_from_basket(basket):
    with allure.step("Удалить тестовый товар"):
        response = basket.remove_from_basket(TEST_PROD_ID)

    with allure.step("Проверить ответ"):
        assert response.status_code == 200

        allure.attach(response.text, name="Empty Basket Response", attachment_type=allure.attachment_type.HTML)


@allure.feature("Управление корзиной")
@allure.story("Негативный сценарий добавления товара")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_invalid_product(basket):
    with allure.step("Попытаться добавить несуществующий товар"):
        response = basket.add_to_basket("invalid_id")

    with allure.step("Проверить ошибку"):
        assert response.status_code == 400
        allure.attach(response.text, name="Error Response", attachment_type=allure.attachment_type.TEXT)

# Для запуска тестов с Allure:
# pytest --alluredir=allure_results test/test_api.py
# allure serve allure_results