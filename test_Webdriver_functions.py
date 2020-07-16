import glob
import json
import os
import time

import fabric
import pytest

from Webdriver_functions import AfWebDriver
from fabtest import *
from portal_functions import portal
from postgres import PostgresDB
import configparser

url='http://10.32.5.29:8080'
ip='10.32.5.29'

class Test():
    @pytest.fixture(scope='session')
    def setup(self):
        print('setting up')
        # fabric.tasks.execute(stop_v6_all)
        # time.sleep(20)
        # print('Services stopped successfully')
        # fabric.tasks.execute(stop_config_v)
        # time.sleep(20)
        # fabric.tasks.execute(start_config)
        # time.sleep(20)
        # fabric.tasks.execute(start_config_upgrade)
        # time.sleep(150)
        # data.dataenter('ct.txt', 'ag.txt', 'dn.txt', 'http://10.25.0.237');
        # time.sleep(20)
        self.driver = AfWebDriver().get_firefox_driver()
        obj = portal()
        obj.login(url, self.driver)
        obj.goto_component_config(url, self.driver)
        print(self.driver)
        return self.driver


    def acdr_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 't_acdr' ORDER BY ORDINAL_POSITION;")
        data=cursor.fetchall()
        return ([item[0] for item in data])

    def eval_logs_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'eval_logs' ORDER BY ORDINAL_POSITION;")
        data = cursor.fetchall()
        return ([item[0] for item in data])
    def eval_summary_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'eval_summary' ORDER BY ORDINAL_POSITION;")
        data = cursor.fetchall()
        return ([item[0] for item in data])

    def agent_batch_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'agent_batch' ORDER BY ORDINAL_POSITION;")
        data = cursor.fetchall()
        return ([item[0] for item in data])
    def call_batch_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'call_batch' ORDER BY ORDINAL_POSITION;")
        data = cursor.fetchall()
        return ([item[0] for item in data])
    def instance_batch_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'instance_batch' ORDER BY ORDINAL_POSITION;")
        data = cursor.fetchall()
        return ([item[0] for item in data])

    def acdr_extended_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 't_acdr_extended' ORDER BY ORDINAL_POSITION;")
        data=cursor.fetchall()
        return ([item[0] for item in data])

    def aglog_extended_columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 't_aglog' ORDER BY ORDINAL_POSITION;")
        data=cursor.fetchall()
        return ([item[0] for item in data])

    def callqueuelog__columns(self):
        connection = PostgresDB().get_connection_afiniti()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 't_call_queue_log' ORDER BY ORDINAL_POSITION;")
        data=cursor.fetchall()
        return [item[0] for item in data]
#-------------------------------------------------AFCORE-4075---------------------------------------------------------------------------------------
    def test_case_export_all_RE(self,setup):
        driver=setup
        export_path = '//span[text()=\'Export\']'
        ob = portal()
        ob.to_export(export_path, driver)
        time.sleep(0.5)
        driver.find_element_by_xpath('//div[@id=\'app\']/main/section/ul[@class=\'tab-pills\']//a[@href=\'#routing-entity\']').click()
        time.sleep(0.5)
        input_elements=driver.find_elements_by_tag_name('input')
        req_count=0
        for element in input_elements:
           #print(element.get_attribute('value'))
           req_count=req_count+1
           element.click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//div[@id=\'app\']/main/section/div/section[2]/button[.=\'Export\']').click()
        time.sleep(30)
        list_of_files = glob.glob('C:\\Users\\Hira.Wahid\\Downloads\\temp\\*')  # * means all if need specific format then *.csv
        time.sleep(0.5)
        latest_file = max(list_of_files, key=os.path.getctime)
        #print(latest_file)
        latest_file.replace('/','\\')
        #print(latest_file)
        with open('C:\\Users\\Hira.Wahid\\Downloads\\temp\\RoutingEntitiesExportFile.json') as json_file:
            data = json.load(json_file)
            res_count=0
            for p in data["reSchemas"]:
                #print('Name: ' + p['type'])
                res_count=res_count+1
        assert res_count==req_count,'Download file is incomplete: check for missing REs in downloaded files'

    def test_case_import_all_RE(self,setup):
        driver=setup
        export_path = '//span[text()=\'Import\']'
        driver.find_element_by_xpath(export_path).click()
        time.sleep(0.5)
        config_imp_path='//a[@ href=\'#configuration\']'        #driver.find_element_by_xpath(config_imp_path).click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//input[\'exportFile\']').send_keys('C:\\Users\\Hira.Wahid\\Downloads\\temp\\RoutingEntitiesExportFile.json')
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[.=\'Upload\']').click()
        time.sleep(0.5)


#----------------------------------------------db-less-schema----------------------------------------------------
    def test_itp(self):
        files=fabric.tasks.execute(run_itp,'ts.sim')


    def test_db_less_2_verify_clomuns_in_files(self):
        m_count=0
        cql_columns= self.callqueuelog__columns()
        print('call queue logs column:')
        print(cql_columns)
        resultant_files = fabric.tasks.execute(download_cql)
        cql_file=resultant_files[ip]
        print(cql_file)
        cqs = []
        for line in open('downloads/'+cql_file, 'r'):
            cqs.append(json.loads(line))
        print(cqs)
        for c in cql_columns:
            if c in cqs[0]:
                print(c + ' found')
            else:
                print(c + 'not present in callqueuelog')
                m_count+=1
        assert m_count<=3,'CQL fields mismatch'

    def test_db_less_eval_logs_verify_clomuns_in_files(self):
        m_count=0
        cql_columns= self.eval_logs_columns()
        print('eval logs column:')
        print(cql_columns)
        resultant_files = fabric.tasks.execute(download_eval_logs)
        if resultant_files == []:
            assert False, 'columns not loaded from db'
        cql_file=resultant_files[ip]
        print(cql_file)
        cqs = []
        for line in open('downloads/'+cql_file, 'r'):
            cqs.append(json.loads(line))
        print(cqs)
        for c in cql_columns:
            if c in cqs[0]:
                print(c + ' found')
            else:
                print(c + 'not present in eval_logs')
                m_count+=1
        assert m_count<=3 ,'eval_logs fields mismatch'
    def test_db_less_eval_summary_verify_clomuns_in_files(self):
        m_count=0
        cql_columns= self.eval_summary_columns()
        print('eval summary column:')
        print(cql_columns)
        resultant_files = fabric.tasks.execute(download_eval_summary)
        if resultant_files == []:
            assert False, 'columns not loaded from db'
        cql_file=resultant_files[ip]
        print(cql_file)
        cqs = []
        for line in open('downloads/'+cql_file, 'r'):
            cqs.append(json.loads(line))
        print(cqs)
        for c in cql_columns:
            if c in cqs[0]:
                print(c + ' found')
            else:
                print(c + 'not present in eval_summary')
                m_count+=1
        assert m_count<=3 ,'eval_sumamry fields mismatch'

    def test_db_less_agent_batch_verify_clomuns_in_files(self):
            m_count = 0
            cql_columns = self.agent_batch_columns()
            print('eval summary column:')
            print(cql_columns)
            resultant_files = fabric.tasks.execute(download_agent_batch)
            if resultant_files == []:
                assert False, 'columns not loaded from db'
            cql_file = resultant_files[ip]
            print(cql_file)
            cqs = []
            for line in open('downloads/' + cql_file, 'r'):
                cqs.append(json.loads(line))
            print(cqs)
            for c in cql_columns:
                if c in cqs[0]:
                    print(c + ' found')
                else:
                    print(c + 'not present in agent_batch')
                    m_count += 1
            assert m_count <= 3, 'agent_batch fields mismatch'

    def test_db_less_call_batch_verify_clomuns_in_files(self):
            m_count = 0
            cql_columns = self.call_batch_columns()
            print('call batch column:')
            print(cql_columns)
            resultant_files = fabric.tasks.execute(download_call_batch)
            if cql_columns == []:
                assert False, 'columns not loaded from db'
            cql_file = resultant_files[ip]
            print(cql_file)
            cqs = []
            for line in open('downloads/' + cql_file, 'r'):
                cqs.append(json.loads(line))
            print(cqs)
            for c in cql_columns:
                if c in cqs[0]:
                    print(c + ' found')
                else:
                    print(c + 'not present in call_batch')
                    m_count += 1
            assert m_count <= 3, 'call_batch fields mismatch'

    def test_db_less_instance_batch_verify_clomuns_in_files(self):
            m_count = 0
            cql_columns = self.instance_batch_columns()
            print('instance batch column:')
            print(cql_columns)
            resultant_files = fabric.tasks.execute(download_instance_batch)
            if cql_columns == []:
                assert False, 'columns not loaded from db'
            cql_file = resultant_files[ip]
            print(cql_file)
            cqs = []
            for line in open('downloads/' + cql_file, 'r'):
                cqs.append(json.loads(line))
            print(cqs)
            for c in cql_columns:
                if c in cqs[0]:
                    print(c + ' found')
                else:
                    print(c + 'not present in instance_batch')
                    m_count += 1
            assert m_count <= 1, 'instance_batch fields mismatch'




    def test_db_less_3_verify_clomuns_in_files(self):
        m_count=0
        acdr_columns= self.acdr_columns()
        print(acdr_columns)
        resultant_files = fabric.tasks.execute(download_acdr)
        cql_file=resultant_files[ip]
        print(cql_file)
        cqs = []
        for line in open('downloads/'+cql_file, 'r'):
            cqs.append(json.loads(line))
        print(cqs)
        for c in acdr_columns:
            if c in cqs[0]:
                print(c + ' found')
            else:
                print(c + 'not present in callqueuelog')
                m_count+=1
        assert m_count<=3,'ACDR fields mismatch'

    def test_db_less_4_verify_clomuns_in_files(self):
        m_count=0
        ag_columns= self.aglog_extended_columns()
        print(ag_columns)
        resultant_files = fabric.tasks.execute(download_aglog)
        cql_file=resultant_files[ip]
        print(cql_file)
        cqs = []
        for line in open('downloads/'+cql_file, 'r'):
            cqs.append(json.loads(line))
        print(cqs)
        for c in ag_columns:
            if c in cqs[0]:
                print(c + ' found')
            else:
                print(c + 'not present in callqueuelog')
                m_count+=1
        assert m_count<=3,'AGLOG fields mismatch'

    def test_db_less_5_verify_clomuns_in_files(self):
        m_count=0
        ag_columns= self.acdr_extended_columns()
        print(ag_columns)
        resultant_files = fabric.tasks.execute(download_aglog)
        cql_file=resultant_files[ip]
        print(cql_file)
        cqs = []
        for line in open('downloads/'+cql_file, 'r'):
            cqs.append(json.loads(line))
        print(cqs)
        for c in ag_columns:
            if c in cqs[0]:
                print(c + ' found')
            else:
                print(c + 'not present in callqueuelog')
                m_count+=1
        assert m_count<=3,'ACDR_extended fields mismatch'

    def test_db_less_6(self,setup):
        print('Verify records per file')
        driver = setup
        config = configparser.ConfigParser()
        config.read('airoc.ini')
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,\"activeConfigurationId\" FROM public.component where name = 'dal' and \"tenantId\"='avaya' ")
        record = cursor.fetchall()
        activeconfiguration = record[0][1]
        driver.find_element_by_xpath('//a[contains(@href,\''+activeconfiguration+'\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_dal_data_storage_type').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_dal_data_storage_type').send_keys('3')
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        time.sleep(0.5)
        cursor.execute(
            "SELECT id,\"activeConfigurationId\"	FROM public.component where name = 'async'  and \"tenantId\"='avaya' ")
        record = cursor.fetchall()
        activeconfiguration = record[0][1]
        driver.find_element_by_xpath('//a[contains(@href,\'' + activeconfiguration + '\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_data_dir_path').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_data_dir_path').send_keys(config['db_less_6']['data_directory'])
        time.sleep(0.5)
        option=driver.find_element_by_id("root_async_enable_database_insertion").is_selected()
        time.sleep(0.5)
        if option==True:
            driver.find_element_by_id("root_async_enable_database_insertion").click()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_file_time_limit').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_file_time_limit').send_keys(config['db_less_6']['file_time_limit'])
        time.sleep(0.5)
        driver.find_element_by_id('root_async_number_of_records_per_file').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_number_of_records_per_file').send_keys(config['db_less_6']['number_of_records_per_file'])
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        time.sleep(0.5)
        driver.quit()
        fabric.tasks.execute(restart_async)
        time.sleep(5)
        fabric.tasks.execute(run_itp)
        time.sleep(5)
        files=[]
        files.append(fabric.tasks.execute(download_acdr))
        files.append(fabric.tasks.execute(download_cql))
        files.append(fabric.tasks.execute(download_aglog))
        print(files)
        if '' in files:
            result=0
        assert 'inprogress' not in files[ip][0], 'ACDR files not generated'
        assert 'inprogress' not in files[ip][1], 'CQL files not generated'
        assert 'inprogress' not in files[ip][2], 'AGLOG    files not generated'

    @pytest.mark.order1
    def test_db_less_7(self,setup):
        print('Verify calls are being created')
        driver = setup
        config = configparser.ConfigParser()
        config.read('airoc.ini')
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        #cursor.execute("update public.global_configuration set ")
        cursor.execute(
            "SELECT id,\"activeConfigurationId\" FROM public.component where name = 'dal' and \"tenantId\"='avaya' ")
        record = cursor.fetchall()
        activeconfiguration = record[0][1]
        driver.find_element_by_xpath('//a[contains(@href,\''+activeconfiguration+'\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_dal_data_storage_type').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_dal_data_storage_type').send_keys('3')
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        time.sleep(0.5)
        cursor.execute(
            "SELECT id,\"activeConfigurationId\"	FROM public.component where name = 'async'  and \"tenantId\"='avaya' ")
        record = cursor.fetchall()
        activeconfiguration = record[0][1]
        driver.find_element_by_xpath('//a[contains(@href,\'' + activeconfiguration + '\')]').click()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_data_dir_path').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_data_dir_path').send_keys(config['db_less_7']['data_directory'])
        time.sleep(0.5)
        option=driver.find_element_by_id("root_async_enable_database_insertion").is_selected()
        time.sleep(0.5)
        if option==True:
            driver.find_element_by_id("root_async_enable_database_insertion").click()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_file_time_limit').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_file_time_limit').send_keys(config['db_less_7']['file_time_limit'])
        time.sleep(0.5)
        driver.find_element_by_id('root_async_number_of_records_per_file').clear()
        time.sleep(0.5)
        driver.find_element_by_id('root_async_number_of_records_per_file').send_keys(config['db_less_7']['number_of_records_per_file'])
        time.sleep(0.5)
        driver.find_element_by_xpath('//button[text()=\'Save\']').click()
        time.sleep(0.5)
        driver.quit()
        fabric.tasks.execute(clean_up)
        fabric.tasks.execute(restart_async)
        time.sleep(5)
        fabric.tasks.execute(run_itp)
        time.sleep(5)
        files=[]
        files.append(fabric.tasks.execute(download_acdr))
        files.append(fabric.tasks.execute(download_cql))
        files.append(fabric.tasks.execute(download_aglog))
        files.append(fabric.tasks.execute(download_eval_summary))
        files.append(fabric.tasks.execute(download_eval_logs))
        files.append(fabric.tasks.execute(download_call_batch))
        files.append(fabric.tasks.execute(download_agent_batch))
        files.append(fabric.tasks.execute(download_instance_batch))
        print('v1')
        print(files)
        time.sleep(80)
        fabric.tasks.execute(run_itp)
        time.sleep(5)
        files_new=[]
        files_new.append(fabric.tasks.execute(download_acdr))
        files_new.append(fabric.tasks.execute(download_cql))
        files_new.append(fabric.tasks.execute(download_aglog))
        files_new.append(fabric.tasks.execute(download_eval_summary))
        files_new.append(fabric.tasks.execute(download_eval_logs))
        files_new.append(fabric.tasks.execute(download_call_batch))
        files_new.append(fabric.tasks.execute(download_agent_batch))
        files_new.append(fabric.tasks.execute(download_instance_batch))
        print(files_new)
        if '' in files:
            result=0
        assert files_new[0][ip]!= files[0][ip],files_new[0][ip] +''+files[0][ip] + 'ACDR new files not generated'
        assert files_new[1][ip] != files[1][ip], 'CQL new files not generated'
        assert files_new[2][ip] != files[2][ip], 'AGLOG   new files not generated'
        assert files_new[3][ip] != files[3][ip], 'Eval_Summary files not generated'
        assert files_new[4][ip] != files[4][ip],  'Eval_Logs   new files not generated'
        assert files_new[5][ip] != files[5][ip],  'call_batch   new files not generated'
        assert files_new[6][ip] != files[6][ip],  'agent_batch   new files not generated'
        assert files_new[7][ip] != files[7][ip], 'instance_batch   new files not generated'






