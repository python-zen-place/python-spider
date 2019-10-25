from selenium.webdriver import ActionChains, Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import config


class Crawler:
    def __init__(self, username, password):
        self.option = ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_argument('--headless')
        self.username = username
        self.password = password
        self.driver = Chrome(options=self.option)
        self.is_login = False

    def login(self):
        self.driver.get(config['login_url'])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'item_account')))
        username_text = self.driver.find_elements_by_class_name('item_account')[0]
        password_text = self.driver.find_elements_by_class_name('item_account')[1]
        btn = self.driver.find_element_by_id('login-button')
        username_text.send_keys(self.username)
        password_text.send_keys(self.password)
        ActionChains(self.driver).move_to_element(btn).click(btn).perform()
        self.is_login = True

    def get_mi9pro(self):
        assert self.is_login, 'Login required'
        self.driver.get(config['mi9pro_url'])
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'J_proBuyBtn')))
        btn = self.driver.find_elements_by_class_name('J_proBuyBtn')[0]
        assert '购买' in btn.text, 'Not the time'
        ActionChains(self.driver).move_to_element(btn).click(btn).perform()
        self.driver.get(config['cart_url'])
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'J_goCheckout')))
        btn = self.driver.find_elements_by_class_name('J_goCheckout')[0]
        ActionChains(self.driver).move_to_element(btn).click(btn).perform()




