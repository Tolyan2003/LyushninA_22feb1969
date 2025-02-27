import os
import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from page.BasketApi import BasketAPI
from DataProvider import  DataProvider
from config import Config
from requests.cookies import RequestsCookieJar


class SmartSession(requests.Session):
    def __init__(self, initial_cookies=None):
        super().__init__()
        self.cookies = RequestsCookieJar()
        if initial_cookies:
            self._update_cookies(initial_cookies)

    def _update_cookies(self, new_cookies):
        for name, value in new_cookies.items():
            self.cookies.set(
                name, value,
                domain=Config.DOMAIN,
                path='/',
                secure=True,
                rest={'HttpOnly': True}
            )

    def request(self, method, url, **kwargs):
        response = super().request(method, url, **kwargs)
        self._process_response_cookies(response)
        return response

    def _process_response_cookies(self, response):
        new_cookies = {
            c.name: c.value
            for c in response.cookies
            if c.name in Config.REQUIRED_COOKIES
        }
        if new_cookies:
            self._update_cookies(new_cookies)


@pytest.fixture(scope='session')
def session(initial_cookies):
    with SmartSession(initial_cookies=initial_cookies) as s:
        s.headers.update({
            'User-Agent': Config.USER_AGENT,
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'X-Requested-With': 'XMLHttpRequest'
        })
        yield s
        # Очистка корзины после всех тестов
        s.post(
            Config.BASE_URL + Config.ORDER_ENDPOINT,
            data={'data': '{"type":"clear_all"}'}
        )


@pytest.fixture(scope='session')
def initial_cookies():
    return {
        'PHPSESSID': os.getenv('PHPSESSID', 'RzBgNBnZLWUgDYt5sfCp3mj6t4LgR2Ns'),
        'BX_USER_ID': os.getenv('BX_USER_ID', '90cd9c43c36aef092a1f92ab502fcd9c'),
        'basketor': os.getenv('basketor', '711346')
    }

@pytest.fixture
def basket(session):
    return BasketAPI(session)


@pytest.fixture
def browser():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver

    with allure.step("Закрыть браузер"):
        driver.quit()


@pytest.fixture
def test_data():
    return DataProvider()