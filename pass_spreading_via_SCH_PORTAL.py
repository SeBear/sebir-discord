import pandas as pd
import selenium.webdriver as browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import os
import re
import PySimpleGUI  as sg

os.chdir(os.path.curdir + "\\data")


class FileParser(pd.DataFrame):

    def __init__(self):
        super().__init__(self.__get_auth_list)

    @property
    def __get_auth_list(self):
        auth_list = pd.read_csv("school_auth.csv", sep=";", encoding="windows-1251")
        return auth_list


class Chrome(browser.Chrome):

    def __init__(self):

        def chromeSetOptions():
            options = browser.ChromeOptions()
            # options.add_experimental_option("prefs",{"download.default_directory": workingDir + "\\puraches\\" + number ,"download_restrictions": 0}) #Место загрузки по умолчанию
            options.binary_location = os.path.abspath(os.curdir) + "\\chrome-bin\\chrome.exe"
            # UNCOMMENT TO RUN HEADLESS#
            # options.headless = True
            return options

        super().__init__(os.path.abspath(os.curdir) + '\\chromedriver.exe',
                         # UNCOMMENT TO RUN HEADLESS#
                         # service_args=["-silent"],
                         options=chromeSetOptions()
                         )
        self.waitFor = 5

    def await_for_element_presentation(self, by_method, xpath):
        if by_method == 'XPATH':
            isPresented = expected_conditions.presence_of_element_located((By.XPATH, xpath))
        if by_method == 'NAME':
            isPresented = expected_conditions.presence_of_element_located((By.NAME, xpath))
        if by_method == 'PART_OF_LINK':
            isPresented = expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, xpath))
        if by_method == 'ID':
            isPresented = expected_conditions.presence_of_element_located((By.ID, xpath))
        try:
            element = WebDriverWait(self, self.waitFor).until(isPresented)
            return element
        except TimeoutException:
            if xpath != '//iframe':
                print("Can not find element by", by_method, xpath)
            else:
                # Блядь, разрабы ШП просто конченые обнюханные клеем долбоебы-вуайеристы. Ебал их в рот. Нахуя блядь для сообщений использовать iframe?!
                return

    def login(self, username, password):
        self.get('https://login.school.mosreg.ru')
        elem_login = self.await_for_element_presentation("NAME", "login")
        elem_pass = self.await_for_element_presentation("NAME", "password")
        elem_submit_button = self.await_for_element_presentation("XPATH",
                                                                 "//input[@class='mosreg-button mosreg-button_red mosreg-login-form__submit']")
        elem_login.send_keys(username)
        elem_pass.send_keys(password)
        elem_submit_button.click()

    def find_person(self, name):
        name = re.sub(' ', '+', name)
        link = 'https://schools.school.mosreg.ru/school.aspx?school=2000000000582&view=members&group=all&filter=&search=' + name + '&class='
        self.get(link)
        message_href = self.await_for_element_presentation("XPATH",
                                                           "//tr[1]//td[@class='tdButtons']//ul[@class='icons']//li[@class='iM' and 1]/a[1]")
        try:
            message_href.click()
        except:
            print('NO SEND TO', name)

    def send_message(self, message, to_nick):
        message_window = self.await_for_element_presentation("XPATH", "//div[@id='mceu_2']")
        try:
            message_window.click()
            message_window = self.await_for_element_presentation("XPATH", "//iframe")
            send_button = self.await_for_element_presentation("XPATH", "//input[@id='save']")
            self.switch_to.frame(message_window)
        except:
            print('NO SEND BUTTON', to_nick)
        try:
            message_window = self.await_for_element_presentation("XPATH", "//body/p/br")
        except StaleElementReferenceException or NoSuchElementException:
            message_window = self.await_for_element_presentation("XPATH", "//body/p")
        if message_window is not None:
            try:
                message_window.send_keys(message)
            except StaleElementReferenceException or NoSuchElementException:
                # Блядь, разрабы ШП просто конченые обнюханные клеем долбоебы-вуайеристы. Ебал их в рот. Нахуя блядь для сообщений использовать iframe?!
                pass
        else:
            print("CAN NOT SEND", to_nick, message)
        try:
            self.switch_to.parent_frame()
            send_button.click()
        except:
            pass

class GUI():

    def __init__(self, data, browser):
        """

        :type data: pd.DataFrame
        """
        self.browser_instance = browser
        self.data = data
        sg.theme('SystemDefault1')
        self.progress = 0
        input_win = [
            [sg.Input(size=(20, 5), default_text="MorisAlle"), sg.Input(size=(20, 5), default_text="sexisyour13scar")]
        ]
        progressbar = [
            [sg.ProgressBar(len(self.data.index), orientation='h', size=(47, 20), key='progressbar'),
             sg.Text(str(self.progress) + "/" + str(len(self.data.index)), size=(5, 1), key='progress')]
        ]
        outputwin = [
            [sg.Output(size=(78, 20))]
        ]
        layout = [
            [sg.Frame('Логин и пароль', layout=input_win)],
            [sg.Frame('Progress', layout=progressbar)],
            [sg.Frame('Output', layout=outputwin)],
            [sg.Submit('Войти в ШП'), sg.Submit('Разослать пароли'), sg.Cancel()]
        ]
        self.window = sg.Window('Рассылка в ШП', layout)
        self.progress_bar = self.window['progressbar']
        self.run()

    def updateGUIProgress(self, currentProgress):
        self.progress_bar.UpdateBar(currentProgress + 1)
        self.progress += 1
        self.window['progress'].update(str(self.progress) + "/" + str(len(self.data.index)))

    def run(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event in ('Cancel', None):
                try:
                    self.browser_instance.browser.quit()
                except NameError:
                    # If browser is not running
                    pass
                except AttributeError:
                    pass
                os._exit(0)
            if self.event == 'Войти в ШП':
                self.browser_instance.login(self.values[0], self.values[1])
            if self.event == 'Разослать пароли':
                for i, row in self.data.iterrows():
                    self.browser_instance.find_person(row['nick'])
                    self.browser_instance.send_message("Пароль для аутентификации в Discord: " + row['pass'] + "\n"
                                                                                                               "Для получения доступа пройдите по ссылке: http://discord.gg/2Qzy4ag\n"
                                                                                                               "Впишите этот пароль и отправьте его нажатием кнопки ВВОД на клавиатуре.",
                                                       row['nick'])
                    self.updateGUIProgress(i)


auth = FileParser()
chrome = Chrome()
start = GUI(auth, chrome)
