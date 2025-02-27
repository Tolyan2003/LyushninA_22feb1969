class Config:
    BASE_URL = "https://www.sibdar-spb.ru"
    ORDER_ENDPOINT = "/ajax/basketOrder.php"
    LIST_ENDPOINT = "/ajax/basketList.php"
    DOMAIN = "sibdar-spb.ru"
    REQUIRED_COOKIES = ['PHPSESSID', 'BX_USER_ID', 'basketor']
    USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )