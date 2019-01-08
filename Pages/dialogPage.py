from selenium.webdriver.common.keys import Keys
import json
import os
from Pages.loginPage import LoginPage
from selenium import webdriver
from multiprocessing import Process
import time
import pyautogui


def message_loop(login, password, dialog_id):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

    driver.implicitly_wait(10)
    login_page = LoginPage(driver)
    login_page.enter_site('https://vk.com', False)
    login_page.enter_username(f'{login}')
    login_page.enter_password(f'{password}')
    login_page.log_into(False)
    driver.get(f'https://vk.com/im?sel={dialog_id}')
    print('Completed...\n== Подключение завершено ==')
    time.sleep(0.1)
    pyautogui.hotkey('enter')
    with open('resources/friends.json') as f:
        data = json.load(f)
        lm = driver.find_elements_by_xpath("//*[@class='im-mess--text wall_module _im_log_body']")[-1]
        while True:
            time.sleep(0.1)
            message = driver.find_elements_by_xpath("//*[@class='im-mess--text wall_module _im_log_body']")[-1]
            if lm != message:
                for key, value in data.items():
                    if message.find_element_by_xpath('../../../..').get_attribute('data-peer') == str(dialog_id):
                        if dialog_id == value:
                            print(f'{key} > {message.text}')
                            time.sleep(0.1)
                            pyautogui.hotkey('enter')
                lm = message


class DialogPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_dialog(self, dialog_id, login, password):
        self.driver.get(f'https://vk.com/im?sel={dialog_id}')
        try:
            time.sleep(1)

            if self.driver.find_element_by_xpath("//span[@class='_im_chat_input_error']").text:
                raise AssertionError

            self.textbox = self.driver.find_element_by_id(f'im_editable{dialog_id}')
            messages = self.driver.find_elements_by_xpath("//*[@class='im-mess--text wall_module _im_log_body']")
            with open('resources/friends.json') as f:
                data = json.load(f)
                for message in messages:
                    for key, value in data.items():
                        if message.find_element_by_xpath('../../../..').get_attribute('data-peer') == str(value):
                            print(f'{key} > {message.text}')
            print('== Дождитесь полного подключения ==')
            p = Process(target=message_loop, args=(login, password, dialog_id))
            p.start()
            time.sleep(1)

        except Exception as e:
            # print(e)
            print('== Диалог для Вас закрыт ==')
            return False
        return True

    def send_message(self, message):

        self.textbox.send_keys(f'{message}')
        self.textbox.send_keys(Keys.RETURN)

    def load_friend_edit_interface_and_get_id_result(self):
        with open(os.path.abspath('resources/friends.json')) as f:
            # Подгрузка пользователей из friends.json
            data = json.load(f)

            # Создание списка пользователей с уточнением по id
            result = list(map((lambda x, y: [x, y]), list(range(len(data))), sorted([f'{name}' for name in data])))

            # Вывод пользователей из result
            for i in result:
                time.sleep(0.1)
                print(f'{i[0]}. {i[1]}')

            dec = input('== Выберите личность для разговора ==\n')
            if dec not in f'{[user[0] for user in result]}':
                print('== Неверно выбран id ==')
                return False
            else:
                return data[result[int(dec)][1]]
