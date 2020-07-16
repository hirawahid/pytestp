import json
import os
import time

import fabric
import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Webdriver_functions import AfWebDriver
from fabtest import *
from portal_functions import portal
from postgres import PostgresDB
import configparser

from swagapi import swaggerData
url1='http://10.32.5.29'
url='http://10.32.5.29:8080'
ip='10.32.5.29'

class Test():
    @pytest.fixture(scope='session')
    def setup(self):
        self.driver = AfWebDriver().get_firefox_driver()
        obj = portal()
        obj.login(url, self.driver)
        obj.goto_component_config(url, self.driver)
        print(self.driver)
        return self.driver

    def test_data_loading(self,setup):
        driver = setup
        config = configparser.ConfigParser()
        config.read('airoc.ini')
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,\"activeConfigurationId\" FROM public.component where name = 'airo_haglog_service' and \"tenantId\"='avaya' ")
        record = cursor.fetchall()
        activeconfiguration = record[0][1]
        driver.find_element_by_xpath('//a[contains(@href,\'' + activeconfiguration + '\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_local_configuration_number_of_days').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_local_configuration_number_of_days').send_keys(config['test_haglog_1']['number_of_days'])
        time.sleep(0.5)
        r=driver.find_element_by_id('root_postgres_configuration_postgres_create_schema').is_selected()
        time.sleep(0.5)
        if r == False:
            driver.find_element_by_id('root_postgres_configuration_postgres_create_schema').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_postgres_configuration_postgres_host').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_postgres_configuration_postgres_host').send_keys(ip)
        time.sleep(0.5)
        driver.find_element_by_id('root_postgres_configuration_postgres_password').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_postgres_configuration_postgres_password').send_keys(config['test_haglog_1']['postgres_pwd'])
        time.sleep(0.5)
        driver.find_element_by_id('root_postgres_configuration_postgres_username').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_postgres_configuration_postgres_username').send_keys(
            config['test_haglog_1']['user'])
        time.sleep(0.5)
        r = driver.find_element_by_id('root_postgres_configuration_postgres_truncate').is_selected()
        time.sleep(0.5)
        if r == False:
            driver.find_element_by_id('root_postgres_configuration_postgres_truncate').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        time.sleep(0.5)
        cursor.execute(
            "SELECT id,\"activeConfigurationId\" FROM public.component where name = 'airo_haglog_service_status' and \"tenantId\"='avaya' ")
        record = cursor.fetchall()
        activeconfiguration = record[0][1]
        driver.find_element_by_xpath('//a[contains(@href,\'' + activeconfiguration + '\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_airo_haglog_service_status_batch_processed').clear()
        driver.find_element_by_id('root_airo_haglog_service_status_batch_processed').send_keys(0)
        time.sleep(0.5)
        driver.find_element_by_id('root_airo_haglog_service_status_completion_in_percentage').clear()
        driver.find_element_by_id('root_airo_haglog_service_status_completion_in_percentage').send_keys(0)
        time.sleep(0.5)
        driver.find_element_by_id('root_airo_haglog_service_status_days_completed').clear()
        driver.find_element_by_id('root_airo_haglog_service_status_days_completed').send_keys(0)
        time.sleep(0.5)
        driver.find_element_by_id('root_airo_haglog_service_status_total_batch').clear()
        driver.find_element_by_id('root_airo_haglog_service_status_total_batch').send_keys(0)
        time.sleep(0.5)
        driver.find_element_by_id('root_airo_haglog_service_status_total_days').clear()
        driver.find_element_by_id('root_airo_haglog_service_status_total_days').send_keys(0)
        time.sleep(0.5)
        driver.find_element_by_id('root_airo_haglog_service_status_service_status').clear()
        driver.find_element_by_id('root_airo_haglog_service_status_service_status').send_keys('not_started')
        time.sleep(0.5)
        select=driver.find_element_by_id("root_airo_haglog_service_status_service_action").click()
        time.sleep(3)
        swapToActive = driver.find_element_by_id("root_airo_haglog_service_status_service_action")
        swapToActive = driver.switch_to.active_element
        swapToActive.send_keys(Keys.DOWN)
        swapToActive.send_keys(Keys.DOWN)
        swapToActive.send_keys(Keys.DOWN)
        swapToActive.send_keys(Keys.RETURN)
        time.sleep(3)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT count(*) FROM haglog_schema.haglog;")
        count = cursor.fetchall()
        hag_log_count_p = count[0][0]
        print(hag_log_count_p)
        time.sleep(3)
        driver.refresh()
        time.sleep(0.5)
        service_status=driver.find_element_by_id('root_airo_haglog_service_status_service_status').get_attribute('value')
        time.sleep(3)
        driver.refresh()
        time.sleep(0.5)
        driver.quit()
        time.sleep(20)
        # complete=0
        # complete_p=0
        # while int(complete) <= 200:
        #     driver.refresh()
        #     time.sleep(10)
        #     service_status=driver.find_element_by_id('root_airo_haglog_service_status_service_status').get_attribute('value')
        #     if(service_status=='completed' or service_status == 'select'):
        #         print('Service is done')
        #         break
        #     else:
        #         print('service is processing')
        print('service finished processing')
        cursor.execute(
            "SELECT count(*) FROM haglog_schema.haglog;")
        count = cursor.fetchall()
        hag_log_count = count[0][0]
        print(hag_log_count)
        assert hag_log_count > hag_log_count_p, 'Data not loaded in haglog table'

    #------------------------------------------------------ECHI-----------------------------------

    def test_data_loading_echi(self,setup):
        #------------------truncate echi tables tbi
        driver = setup
        config = configparser.ConfigParser()
        config.read('airoc.ini')
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,\"activeConfigurationId\" FROM public.component where name = 'RealTimeECHI' and \"tenantId\"='avaya' ")
        record = cursor.fetchall()
        activeconfiguration = record[0][1]
        driver.find_element_by_xpath('//a[contains(@href,\'' + activeconfiguration + '\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_ArchivalDays').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_ArchivalDays').send_keys(config['echi']['archival'])
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_ArchivalDaysLimit').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_ArchivalDaysLimit').send_keys(config['echi']['archivaldayslimit'])
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_DBType').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_DBType').send_keys(config['echi']['dbtype'])
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_ArchivalThreadCount').clear()
        driver.find_element_by_id('root_RealTimeECHI_ArchivalThreadCount').send_keys(config['echi']['threads'])
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_DatabaseConnectionString').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_DatabaseConnectionString').send_keys(config['echi']['connstr'])
        time.sleep(0.5)
        r=driver.find_element_by_id('root_RealTimeECHI_HAStandAloneProcessing').is_selected()
        if r== False:
            r = driver.find_element_by_id('root_RealTimeECHI_HAStandAloneProcessing').click()
        time.sleep(0.5)
        r=driver.find_element_by_id('root_RealTimeECHI_EnableArchival').is_selected()
        if r==False:
            driver.find_element_by_id('root_RealTimeECHI_EnableArchival').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_HostName').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_HostName').send_keys(config['echi']['cmsip'])
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_LocalEchDirectoryPath').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_LocalEchDirectoryPath').send_keys(config['echi']['local'])
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_PrimaryPassword').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_PrimaryPassword').send_keys(config['echi']['cmspwd'])
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_PrimaryUsername').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_RealTimeECHI_PrimaryUsername').send_keys(config['echi']['cmsuname'])
        time.sleep(0.5)
        r=driver.find_element_by_id('root_RealTimeECHI_GenerateOutputFiles').is_selected()
        if r == True:
            driver.find_element_by_id('root_RealTimeECHI_GenerateOutputFiles').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        time.sleep(3)
        cursor.execute(
            "SELECT id,\"activeConfigurationId\" FROM public.component where name = 'echi_status' and \"tenantId\"='avaya' ")
        record = cursor.fetchall()

        activeconfiguration = record[0][1]
        componentid=record[0][0]
        driver.find_element_by_xpath('//a[contains(@href,\'' + activeconfiguration + '\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_archival_completed').clear()
        driver.find_element_by_id('root_archival_completed').send_keys('not_started')
        time.sleep(0.5)
        driver.find_element_by_id('root_total_archival_days').clear()
        driver.find_element_by_id('root_total_archival_days').send_keys(0)
        time.sleep(0.5)
        driver.find_element_by_id('root_archival_days_processed').clear()
        driver.find_element_by_id('root_archival_days_processed').send_keys(0)
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        time.sleep(3)
        driver.quit()
        fabric.tasks.execute(restart_echi)
        time.sleep(3)
        cursor.execute("SELECT \"schemaId\"	FROM public.configuration where id = '" + activeconfiguration + "'")
        record1 = cursor.fetchall()
        connection.close()
        print('schemaid:' + record1[0][0])
        schemaid = record1[0][0]
        completed=0
        obj=swaggerData()
        iterations=0
        while completed != 'Completed' and iterations <= 30:
            completed=obj.check_echi_status(componentid,schemaid,activeconfiguration,'avaya',url1)
            print(completed)
            iterations+=1
            time.sleep(10)
        if iterations > 30:
            print('echi data dump not successful')
        else:
            print('echi completed')
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT count(*) FROM echi_schema.echirecords;")
        count = cursor.fetchall()
        connection.close()
        echi_count = count[0][0]
        print(echi_count)
        assert echi_count > 0, 'Data not loaded in echi table'
        print('service finished processing')




