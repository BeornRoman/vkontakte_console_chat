from Pages.loginPage import LoginPage
from Pages.dialogPage import DialogPage
from selenium import webdriver
import unittest
import getpass
import pyautogui


class TestMethod(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        self.driver.implicitly_wait(10)
        self.dialog_procedure = True
        self.login_procedure = True
        self.message = 'start!'

    def tearDown(self):
        self.driver.close()

    def test_send_massage(self):
        # Авторизация
        login_page = LoginPage(self.driver)
        while self.login_procedure:
            login = input('Введите логин: ')
            password = getpass.getpass('Введите пароль: ')
            login_page.enter_site('https://vk.com', True)
            login_page.enter_username(f'{login}')
            login_page.enter_password(f'{password}')
            if login_page.log_into(True):
                self.login_procedure = False

        # Выбор диалога
        dialog_page = DialogPage(self.driver)
        while self.dialog_procedure:
            result = dialog_page.load_friend_edit_interface_and_get_id_result()
            if dialog_page.enter_dialog(result, login, password):
                self.dialog_procedure = False

        # Общение
        while self.message.lower() != 'stop!':
            self.message = input(f'> ')
            dialog_page.send_message(f'{self.message}')

        # hard reset
        for i in range(3):
            pyautogui.hotkey('ctrl', 'c')


if __name__ == '__main__':
    unittest.main()




