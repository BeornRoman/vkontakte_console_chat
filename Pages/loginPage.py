class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_site(self, site, debug):
        if debug:
            print(f'== Входим -> {site} ==')
        self.driver.get(f'{site}')

    def enter_username(self, username):
        self.driver.find_element_by_id('index_email').send_keys(f'{username}')

    def enter_password(self, password):
        self.driver.find_element_by_id('index_pass').send_keys(f'{password}')

    def log_into(self, debug):
        if debug:
            print('== Авторизация ==')
        self.driver.find_element_by_id('index_login_button').click()
        # time.sleep(2)
        try:
            self.driver.find_element_by_id('l_pr')
            if debug:
                print('== Доступ разрешён ==')
            return True
        except:
            if debug:
                print('== Неправильный пароль ==')
            return False



