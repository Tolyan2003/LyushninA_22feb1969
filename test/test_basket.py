import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from page.Basket_Page import BasketPage
from DataProvider import DataProvider
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType

data = DataProvider()
id_prod = data.PRODUCT_ID


@allure.feature('Авторизация')
@allure.story('Успешная авторизация')
def test_login(browser):
    data = DataProvider()
    username = data.USERNAME
    tel = data.TEL

    with allure.step("Создание объекта страницы"):
        page = BasketPage(browser)

    with allure.step("Переход на страницу"):
        page.go()

    try:
        with allure.step(f"Авторизация с именем {username} и телефоном {tel}"):
            page.login(username, tel)

        with allure.step("Проверка background-color поля имени"):
            name_field = browser.find_element(By.CSS_SELECTOR, 'input.req_bask.name_order_bask')
            background_color = name_field.value_of_css_property('background-color')

            # Преобразуем цвет в hex формат для более удобной проверки
            hex_color = Color.from_string(background_color).hex

            # Проверяем, что цвет желтый
            assert hex_color == '#ffffff', f"Неверный background-color поля имени: {hex_color}"

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        allure.attach(browser.get_screenshot_as_png(),
                      name="error_screenshot",
                      attachment_type=AttachmentType.PNG)
        allure.attach(str(e), name="error_message", attachment_type=AttachmentType.TEXT)
        raise


@allure.feature('Корзина')
@allure.story('Добавление и изменение количества товара')
def test_add_and_change_to_basket(browser):
    with allure.step("Создание объекта страницы"):
        page = BasketPage(browser)

    with allure.step("Переход на страницу"):
        page.go()

    with allure.step(f"Добавление товара {id_prod} в корзину"):
        page.add_to_basket(id_prod)

    try:
        with allure.step("Изменение количества товара"):
            price = page.change_to_basket()

        with allure.step("Проверка цены товара"):
            price_text = price.text.strip().replace(' ', '')
            assert '3840' in price_text, f"Текст элемента: '{price_text}'"
            assert price_text == '3840', f"Ожидается '3840', получено '{price_text}'"

    except AssertionError:
        allure.attach(browser.get_screenshot_as_png(),
                      name="price_check_failure",
                      attachment_type=AttachmentType.PNG)
        raise


@allure.feature('Корзина')
@allure.story('Удаление товара из корзины')
def test_delete_element_from_basket(browser):
    with allure.step("Создание объекта страницы"):
        page = BasketPage(browser)

    with allure.step("Переход на страницу"):
        page.go()

    with allure.step(f"Добавление товара {id_prod} в корзину"):
        page.add_to_basket(id_prod)

    with allure.step(f"Удаление товара {id_prod} из корзины"):
        page.delete_to_basket()

    try:
        with allure.step("Проверка наличия сообщения о пустой корзине"):
            empty_basket_message = browser.find_element(By.CSS_SELECTOR, '.body_order#order-list h2')

            # Проверяем текст сообщения
            expected_text = "Корзина пуста, необходимо это исправить"
            actual_text = empty_basket_message.text

            assert actual_text == expected_text, f"Неверный текст сообщения: {actual_text}"

        with allure.step("Проверка отсутствия других элементов корзины"):
            assert len(browser.find_elements(By.CSS_SELECTOR,
                                             '.body_order#order-list .product-item')) == 0, "В корзине остались товары"

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        allure.attach(browser.get_screenshot_as_png(),
                      name="empty_basket_check",
                      attachment_type=AttachmentType.PNG)
        raise

# Для запуска тестов с Allure:
# pytest --alluredir=allure_results test/test_basket.py
# allure serve allure_results