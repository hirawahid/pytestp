import os
import time

from selenium import webdriver
import psycopg2
from selenium.webdriver import FirefoxProfile, firefox


class AfWebDriver():
    web_driver_directory = "WebDrivers"
    firefox_driver_name = "geckodriver"
    chrome_driver_name = "chromedriver"

    # MySQL DB Config
    mysql_db_name = "afconfig"
    mysql_db_host = "192.168.129.129"
    mysql_db_user = "root"
    mysql_db_password = "Password@11"

    # Postgress DB Config
    postgres_db_name = "afconfig"
    postgres_db_host = "10.25.0.237"
    postgres_db_port = "5434"
    postgres_db_user = "postgres"
    postgres_db_password = "thisshouldbeasecret"

    def login(self,url,driver,step_wait=0.5):
        driver.get(url + '/auth/login')
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[1]/input").clear()
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[1]/input").send_keys("admin")
        time.sleep(step_wait)
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='app']/main/form/div[2]/input").send_keys("admin")
        time.sleep(step_wait)
        driver.find_element_by_xpath("//div[@id='app']/main/form/button").click()
        time.sleep(step_wait)

    def goto_component_config(self,url,driver,step_wait=0.5):
        time.sleep(step_wait)
        driver.get(url + '/config')
        time.sleep(step_wait)
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/header/section[2]/ul/li/a/i').click()
        time.sleep(step_wait)
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/header/section[2]/ul/li/div/ul/li[1]/a/div/span').click()
        time.sleep(step_wait)
        #self.driver.find_element_by_xpath(component_xpath_in_menu).click()
        #time.sleep(step_wait)
    def to_export(self,path,driver,step_wait=0.5):
        driver.find_element_by_xpath(path).click()
        time.sleep(step_wait)

    def get_driver_path(self, browser_name):  # TBD: make it generic for cross OS
        dirname = os.path.dirname(__file__)
        driverpath = dirname + "\\" + self.web_driver_directory + "\\" + browser_name
        return driverpath

    def get_firefox_driver(self):
        driverpath = self.get_driver_path(self.firefox_driver_name)
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", 'C:\\Users\\Hira.Wahid\\Downloads\\temp')
        mime_types = [
            'text/plain',
            'application/json',
            'application/vnd.ms-excel',
            'text/csv',
            'application/csv',
            'text/comma-separated-values',
            'application/download',
            'application/octet-stream',
            'binary/octet-stream',
            'application/binary',
            'application/x-unknown'
        ]
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(mime_types))
        dirname = os.path.dirname(__file__)
        driver = webdriver.Firefox(firefox_profile=fp,executable_path=driverpath)
        return driver

    # def get_chrome_driver(self):
    #     dirname = os.path.dirname(__file__)
    #     driverpath = self.get_driver_path(self.chrome_driver_name)
    #     self.driver = webdriver.Chrome(executable_path=driverpath)
    #     return driver


class PostgresDB:
    def __init__(self):
        self.host = self.postgres_db_host
        self.port = self.postgres_db_port
        self.database = self.postgres_db_name
        self.user = self.postgres_db_user
        self.password = self.postgres_db_password

    def get_connection(self):
        connection = psycopg2.connect(
            user="postgres",
            password="thisshouldbeasecret",
            host="10.32.5.166",
            port="5434",
            database="config")
        return connection

    def close_connection(self, connection):
        connection.close()


class MySQLDB:
    def __init__(self):
        self.host = self.mysql_db_host
        self.database = self.mysql_db_name
        self.user = self.mysql_db_user
        self.password = self.mysql_db_password

    # def get_connection(self):
    #     connection = mysql.connector.connect(
    #         host=self.host,
    #         user=self.user,
    #         passwd=self.password,
    #         database=self.database
    #         )
    #     return connection
    #
    # def close_connection(self,connection):
    #     connection.close()
    #
    # def get_cursor():
    #     return self.db.cursor()
    #
    # def select(self,query):
    #     connection = self.get_connection()
    #     cursor = connection.cursor(buffered=True)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     self.close_connection(connection)
    #     return result

    # def insert(query):
    #     connection = self.get_connection()
    #     cursor = connection.cursor(buffered=True)
    #     cursor.commit(query)
    #     tot_rows = cursor.rowcount
    #     self.close_connection(connection)
    #     return tot_rows #Returns number of rows inserted
    #
    # def update(query):
    #     connection = self.get_connection()
    #     cursor = connection.cursor(buffered=True)
    #     cursor.commit(query)
    #     tot_rows = cursor.rowcount
    #     self.close_connection(connection)

    def delete(self, query):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.commit(query)
        self.close_connection(connection)