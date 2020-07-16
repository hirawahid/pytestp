import configparser
import glob
import os
import datetime

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from xml.dom.minidom import parseString
import json
import ijson
import objectpath
import sshtunnel
import MySQLdb
import MySQLdb as db
import time
import fabric
import pytest
from selenium import *
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from Webdriver_functions import AfWebDriver
from dataentry import *
from fabtest import stop_v6_all, stop_config_v, start_config, start_config_upgrade, run_itp
from portal_functions import portal
from postgres import *
from swagapi import swaggerData

config = configparser.ConfigParser()
config.read('settings.ini')
url=config['config-server']['url']

class Test():
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        print('\nsetting up')
        # fabric.tasks.execute(stop_v6_all)
        # time.sleep(20)
        # print('Services stopped successfully')
        # fabric.tasks.execute(stop_config_v)
        # time.sleep(20)
        # fabric.tasks.execute(start_config)
        # time.sleep(20)
        # fabric.tasks.execute(start_config_upgrade)
        # time.sleep(150)
        #data.dataenter('ct.txt', 'ag.txt', 'dn.txt',url);
        # time.sleep(30)
        # obj = swaggerData()
        # obj.add_dn('http://10.25.0.237', 'RE_updation_scenario/dn_file')
        # time.sleep(20)
        # obj.delete_RE('http://10.25.0.237', 'dn')

        # fabric stop-v6-all,staop config -v,start-config here
        # add routing_entity updates here

        def teardown():
            print('tearing down()')

#-------------------------Config server Audit trail-----------------------------------------------------------------------------------

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'CREATED'), ('acdss', 'CREATED'), ('async', 'CREATED'),
                              ('Routing Engine', 'CREATED'), ('Avaya ECD Switch Interface Configurations', 'CREATED'),
                              ('si', 'CREATED'), ('ASLSync', 'CREATED'), ('License', 'CREATED'), ('dal', 'CREATED'),
                              ('Script Executor', 'CREATED'), ('VHT Connector', 'CREATED'), ('Databases', 'CREATED'),
                              ('Lookup', 'CREATED')])
    def test_case_1_component_schema_created_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.component_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        # print(record)
        assert record[0][0] == expected, test_input + ': Schemas not created at service startup'

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'UPDATED'), ('acdss', 'UPDATED'), ('async', 'UPDATED'),
                              ('Routing Engine', 'UPDATED'), ('Avaya ECD Switch Interface Configurations', 'UPDATED'),
                              ('si', 'UPDATED'), ('ASLSync', 'UPDATED'), ('License', 'UPDATED'), ('dal', 'UPDATED'),
                              ('Script Executor', 'UPDATED'), ('VHT Connector', 'UPDATED'), ('Databases', 'UPDATED'),
                              ('Lookup', 'UPDATED')])
    def test_case_2_component_schema_UPDATED_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.component_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        # print(record)
        assert record[0][0] == expected, test_input + ': Schemas not UPDATED and ACTIVATED at service startup'

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'DELETED'), ('acdss', 'DELETED'), ('async', 'DELETED'),
                              ('Routing Engine', 'DELETED'), ('Avaya ECD Switch Interface Configurations', 'DELETED'),
                              ('si', 'DELETED'), ('ASLSync', 'DELETED'), ('License', 'DELETED'), ('dal', 'DELETED'),
                              ('Script Executor', 'DELETED'), ('VHT Connector', 'DELETED'), ('Databases', 'DELETED'),
                              ('Lookup', 'DELETED')])
    def test_case_3_component_Deletion_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id,\"activeConfigurationId\",\"tenantId\"	FROM public.component where name = '" + test_input + "'")
        record = cursor.fetchall()
        print(test_input + ':')
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute("Update public.component SET \"activeConfigurationId\" = Null where name = '" + test_input + "' and \"tenantId\"='" + tenant + "'")
        connection.commit()
        obj = swaggerData()
        obj.component_deletion(componentid,tenant, 'http://10.25.0.237')
        cursor.execute("SELECT operation FROM public.component_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record2 = cursor.fetchall()
        print(record2)
        assert record2[0][0] == expected, test_input + " not deleted"
        # TODO:deletion

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'CREATED'), ('acdss', 'CREATED'), ('async', 'CREATED'),
                              ('Routing Engine', 'CREATED'), ('Avaya ECD Switch Interface Configurations', 'CREATED'),
                              ('si', 'CREATED'), ('ASLSync', 'CREATED'), ('License', 'CREATED'), ('dal', 'CREATED'),
                              ('Script Executor', 'CREATED'), ('VHT Connector', 'CREATED'), ('Databases', 'CREATED'),
                              ('Lookup', 'CREATED')])
    def test_case_5_component_configuration_CREATED_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.configuration_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        # print(record)
        assert record[0][0] == expected, test_input + ': Configuration not created at service startup'

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'UPDATED'), ('acdss', 'UPDATED'), ('async', 'UPDATED'),
                              ('Routing Engine', 'UPDATED'), ('Avaya ECD Switch Interface Configurations', 'UPDATED'),
                              ('si', 'UPDATED'), ('ASLSync', 'UPDATED'), ('License', 'UPDATED'), ('dal', 'UPDATED'),
                              ('Script Executor', 'UPDATED'), ('VHT Connector', 'UPDATED'), ('Databases', 'UPDATED'),
                              ('Lookup', 'UPDATED')])
    def test_case_5_component_configuration_UPDATED_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.configuration_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        print(record)
        assert record[0][0] == expected, test_input + ': Configuration not updated at service startup or not updated'

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'ACTIVATED'), ('acdss', 'ACTIVATED'), ('async', 'ACTIVATED'),
                              ('Routing Engine', 'ACTIVATED'), ('Avaya ECD Switch Interface Configurations', 'ACTIVATED'),
                              ('si', 'ACTIVATED'), ('ASLSync', 'ACTIVATED'), ('License', 'ACTIVATED'),
                              ('dal', 'ACTIVATED'),
                              ('Script Executor', 'ACTIVATED'), ('VHT Connector', 'ACTIVATED'),
                              ('Databases', 'ACTIVATED'),
                              ('Lookup', 'ACTIVATED')])
    def test_case_5_component_configuration_ACTIVATED_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.configuration_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        print(record)
        assert record[0][0] == expected, test_input + ': Configuration not activated at service startup or not updated'

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'CREATED'), ('acdss', 'CREATED'), ('async', 'CREATED'),
                              ('Routing Engine', 'CREATED'),
                              ('Avaya ECD Switch Interface Configurations', 'CREATED'),
                              ('si', 'CREATED'), ('ASLSync', 'CREATED'), ('License', 'CREATED'),
                              ('dal', 'CREATED'),
                              ('Script Executor', 'CREATED'), ('VHT Connector', 'CREATED'),
                              ('Databases', 'CREATED'),
                              ('Lookup', 'CREATED')])
    def test_case_5_component_schema_CREATED_SCHEMA_LOG_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.schema_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        print(record)
        assert record[0][0] == expected, test_input + ': Schema not created in schema_log at service startup or not updated'

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 'DELETED'),('acdss', 'DELETED'), ('async', 'DELETED'),
                              ('Routing Engine', 'DELETED'),
                              ('Avaya ECD Switch Interface Configurations', 'DELETED'),
                              ('si', 'DELETED'), ('ASLSync', 'DELETED'), ('License', 'DELETED'),
                              ('dal', 'DELETED'),
                              ('Script Executor', 'DELETED'), ('VHT Connector', 'DELETED'),
                              ('Databases', 'DELETED'),
                              ('Lookup', 'DELETED')])
    def test_case_3_component_configuration_Deletion_verification(self, test_input, expected):
        data.dataenter('ct.txt', 'ag.txt', 'dn.txt', 'http://10.25.0.237');
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id,\"activeConfigurationId\",\"tenantId\"	FROM public.component where name = '" + test_input + "'")
        record = cursor.fetchall()
        print(test_input + ':')
        print(record)
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute("SELECT \"schemaId\"	FROM public.configuration where id = '" + activeconfiguration + "'")
        record1 = cursor.fetchall()
        print('schemaid:'+record1[0][0])
        schemaid = record1[0][0]
        cursor.execute("Update public.component SET \"activeConfigurationId\" = Null where name = '" + test_input + "' and \"tenantId\"='"+tenant+"'")
        connection.commit()
        obj=swaggerData()
        obj.configuration_deletion(componentid,schemaid,tenant,'http://10.25.0.237',activeconfiguration)
        cursor.execute("SELECT operation FROM public.configuration_log where \"componentName\" ='" + test_input + "' and operation ='" + expected + "'")
        record2 = cursor.fetchall()
        print(record2)
        assert record2[0][0] == expected,test_input + " not deleted"
        # TODO:deletion from configuration
    #----Routing-Entity---------------------------------------
    @pytest.mark.parametrize("test_input,expected",
                             [('acd', 'CREATED'), ('dn', 'CREATED'), ('cwt', 'CREATED'),
                              ('benchmark', 'CREATED'), ('lineOfBusiness', 'CREATED'),
                              ('serviceProvider', 'CREATED'), ('vector', 'CREATED'), ('callType', 'CREATED'),
                              ('agentGroup', 'CREATED'),
                              ('awt', 'CREATED')])
    def test_case_1_routing_entity_CREATED_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.routing_entity_log where \"routingEntityType\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        print(record)
        assert record[0][0] == expected, test_input + ': Routing Entity not created at service startup'

    @pytest.mark.parametrize("test_input,expected",
                             [ ('dn', 'UPDATED')])
    def test_case_1_routing_entity_UPDATED_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.routing_entity_log where \"routingEntityType\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        # print(test_input + ':')
        # print(record)
        assert record[0][0] == expected, test_input + ': Configuration not UPDATED at service startup'

    @pytest.mark.parametrize("test_input,expected",
                             [('callType', 'DELETED'),
                              ('agentGroup', 'DELETED'), ('dn', 'DELETED'),('vector', 'DELETED'), ('cwt', 'DELETED'),
                              ('benchmark', 'DELETED'), ('lineOfBusiness', 'DELETED'),
                              ('acd', 'DELETED'), ('serviceProvider', 'DELETED'),
                              ('awt', 'DELETED')])
    def test_case_1_routing_entity_DELETED_verification(self, test_input, expected):
        test=swaggerData()
        status=test.delete_RE('http://10.25.0.237', test_input)
        print(status)
        time.sleep(0.5)
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT operation FROM public.routing_entity_log where \"routingEntityType\" ='" + test_input + "' and operation ='" + expected + "'")
        record = cursor.fetchall()
        print(record)
        # print(test_input + ':')
        # print(record)
        assert record[0][0] == expected, test_input + ': Configuration not DELETED at service startup'

        # -----------------------------------------AFCORE-3964--------------------------------------------------------------------------------------------

    @pytest.mark.parametrize("test_input,expected",
                                 [('serviceProvider', 400), ('cwt', 400),
                                  ('benchmark',400), ('lineOfBusiness',400),
                                  ('acd',400), ('vector', 400),
                                  ('awt', 400)])
    def test_lookup_RE_Deletion_3964(self,test_input,expected):
            data.dataenter('ct.txt', 'ag.txt', 'dn.txt', 'http://10.25.0.237');
            obj = swaggerData()
            status = obj.delete_RE('http://10.25.0.237',test_input)
            print(status)
            assert status >= expected, test_input + ': Configuration not DELETED at service startup'
    # ----------------------------------------------AFCORE-3965----------------------------------------------------number 2
    #before runnning this group comment-out setup fixture create another tenant=genesys and put data in tenant avaya for RE
    # Importing back export from the same config server causes issues since UUIDs collide
    # Configurations dont get activated when they are imported
    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 1), ('acdss', 1), ('async', 1),
                              ('Routing Engine', 1),
                              ('Avaya ECD Switch Interface Configurations',1),
                              ('si',1), ('ASLSync',1), ('License',1),
                              ('dal',1),
                              ('Script Executor',1), ('VHT Connector',1),
                              ('Databases',1),
                              ('Lookup',1)])
    def test_import_and_export_component_configuration_3965(self,test_input,expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        if(test_input== 'License'):
            cursor.execute("select count(data->>'LICENSE_KEY') from public.configuration")
        else:
            cursor.execute("select count(data->>'" + test_input + "') from public.configuration")
        result = cursor.fetchall()
        p_count=result[0][0]
        cursor.execute("SELECT id,\"activeConfigurationId\",\"tenantId\" FROM public.component where name = '" + test_input + "'")
        record = cursor.fetchall()
        print(test_input + ':')
        print(record)
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute("SELECT \"schemaId\"	FROM public.configuration where id = '" + activeconfiguration + "'")
        record1 = cursor.fetchall()
        print('schemaid:' + record1[0][0])
        schemaid = record1[0][0]
        obj=swaggerData()
        resp=obj.export(url,tenant,componentid,schemaid,activeconfiguration)
        r = json.dumps(resp)
        status=obj.i_import(url,tenant, r)
        print(status)
        # if(test_input== 'License'):
        #     cursor.execute("select count(data->>'LICENSE_KEY') from public.configuration")
        # elif(test_input=='Engine Common'):
        #     cursor.execute("select count(data->>'Avaya Native') from public.configuration")
        # elif(test_input=='Script Executor'):
        #     cursor.execute("select count(data->>'Failsafe') from public.configuration")
        # else:
        #     cursor.execute("select count(data->>'" + test_input + "') from public.configuration")
        # result = cursor.fetchall()
        # count=result[0][0]
        # print(result)
        # print(count)
        # cursor.execute("SELECT id,\"activeConfigurationId\",\"tenantId\" FROM public.component where name = '" + test_input + "'")
        # record = cursor.fetchall()
        # n_acid=record[0][1]
        #print('New configurationid=' + n_acid)
        assert status>200, test_input + 'import not successful'
    @pytest.mark.parametrize("test_input,expected",
                                 [('acd', 200), ('dn', 200), ('cwt', 200),
                                  ('benchmark', 200), ('lineOfBusiness', 200),
                                  ('serviceProvider', 200), ('vector', 200), ('callType', 200),
                                  ('agentGroup', 200),
                                  ('awt', 200)])
    def test_import_and_export_routing_entity_3965(self,test_input,expected):
        tenant='avaya'
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        obj=swaggerData()
        resp=obj.export_re(url,tenant,test_input)
        r = json.dumps(resp)
        status=obj.re_import(url,tenant, r)
        print(status)
        assert status<300, test_input + 'import not successful'


    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 1), ('acdss', 1), ('async', 1),
                              ('Routing Engine', 1),
                              ('Avaya ECD Switch Interface Configurations',1),
                              ('si',1), ('ASLSync',1), ('License',1),
                              ('dal',1),
                              ('Script Executor',1), ('VHT Connector',1),
                              ('Databases',1),
                              ('Lookup',1)])
    def test_import_and_activated_configuration_3965(self,test_input,expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id,\"activeConfigurationId\",\"tenantId\" FROM public.component where name = '" + test_input + "'")
        record = cursor.fetchall()
        print(test_input + ':')
        print(record)
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute("SELECT \"schemaId\"	FROM public.configuration where id = '" + activeconfiguration + "'")
        record1 = cursor.fetchall()
        print('schemaid:' + record1[0][0])
        schemaid = record1[0][0]
        obj=swaggerData()
        resp=obj.export(url,tenant,componentid,schemaid,activeconfiguration)
        r = json.dumps(resp)
        obj.i_import(url,tenant, r)
        cursor.execute("SELECT id,\"activeConfigurationId\",\"tenantId\" FROM public.component where name = '" + test_input + "'")
        record = cursor.fetchall()
        n_acid=record[0][1]
        print('New configurationid='+n_acid)
        assert activeconfiguration!=n_acid, test_input + 'import not successfully activated'

        # -----------------------------exporting and importing from other tenants---------------------------------------------
    @pytest.mark.parametrize("test_input,expected",
                                 [('acd', 200), ('dn', 200), ('cwt', 200),
                                  ('benchmark', 200), ('lineOfBusiness', 200),
                                  ('serviceProvider', 200), ('vector', 200), ('callType', 200),
                                  ('agentGroup', 200),
                                  ('awt', 200)])
    def test_export_re_avaya_to_genesys_3965(self,test_input,expected):
        #there must be another tenant like genesys enabled with user
        #avaya tenant must have re data schema working for both tenants
        #data.dataenter('ct.txt', 'ag.txt', 'dn.txt',url);
        obj=swaggerData()
        data=obj.export_re(url,'avaya',test_input)
        print(data)
        r = json.dumps(data)
        status=obj.re_import(url, 'genesys', r)
        assert status==201,test_input+' not imported on different tenant'

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 200), ('acdss', 200), ('async', 200),
                              ('Routing Engine', 200),
                              ('Avaya ECD Switch Interface Configurations',200),
                              ('si',200), ('ASLSync',200), ('License',200),
                              ('dal',200),
                              ('Script Executor',200), ('VHT Connector',200),
                              ('Databases',200),
                              ('Lookup',200)])
    def test_export_component_configurations_avaya_to_genesys_3965(self,test_input,expected):
        #there must be another tenant like genesys enabled with user
        #avaya tenant must have re data
        #data.dataenter('ct.txt', 'ag.txt', 'dn.txt',url);
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id,\"activeConfigurationId\",\"tenantId\" FROM public.component where name = '" + test_input + "' and \"tenantId\"= 'avaya'")
        record = cursor.fetchall()
        print(test_input + ':')
        print(record)
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute("SELECT \"schemaId\"	FROM public.configuration where id = '" + activeconfiguration + "'")
        record1 = cursor.fetchall()
        print('schemaid:' + record1[0][0])
        schemaid = record1[0][0]
        obj=swaggerData()
        resp=obj.export(url,tenant,componentid,schemaid,activeconfiguration)
        r = json.dumps(resp)
        status=obj.i_import(url,'genesys', r)
        print(status)
        assert status==201,test_input + 'component not imported to other tenant'



#------------------------------------------------------AFCORE-4453--------------------------------------------------

    @pytest.mark.parametrize("test_input,expected",
                             [('Engine Common', 1), ('acdss', 1), ('async', 1),
                              ('Routing Engine', 1),
                              ('Avaya ECD Switch Interface Configurations', 1),
                              ('si', 1), ('ASLSync', 1), ('License', 1),
                              ('dal', 1),
                              ('Script Executor', 1), ('VHT Connector', 1),
                              ('Databases', 1),
                              ('Lookup', 1)])
    def test_schema_and_customtypes_Deletion_verification(self, test_input, expected):
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,\"activeConfigurationId\",\"tenantId\"	FROM public.component where name = '" + test_input + "'")
        record = cursor.fetchall()
        print(test_input + ':')
        print(record)
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute("SELECT \"schemaId\"	FROM public.configuration where id = '" + activeconfiguration + "'")
        record1 = cursor.fetchall()
        print('schemaid:' + record1[0][0])
        schemaid = record1[0][0]
        cursor.execute("SELECT \"customTypeUsedId\"	FROM public.schema_meta_data where \"schemaId\" = '" + schemaid + "'")
        record2 = cursor.fetchall()
        print(record2)
        if record2:
            obj=swaggerData()
            cursor.execute("Update public.component SET \"activeConfigurationId\" = Null where name = '" + test_input + "' and \"tenantId\"='" + tenant + "'")
            connection.commit()
            status = obj.schema_deletion(componentid, schemaid, tenant, url)
        cursor.execute("SELECT count(*)	FROM public.schema_meta_data where \"schemaId\" = '" + schemaid + "'")
        record3 = cursor.fetchall()
        assert record3[0][0] == 0, test_input + " Schema not deleted"

    def test_AFCORE_5308(self):
        files = fabric.tasks.execute(run_itp, 'ts.sim')
        connection = MySQLdb.connect(config['mysql']['host'],config['mysql']['user'],config['mysql']['pwd'],config['mysql']['name'])
        cursor=connection.cursor()
        cursor.execute("SELECT tenant FROM afiniti.t_acdr order by call_time desc limit 1;")
        t_name=cursor.fetchall()
        print(t_name)
        assert t_name[0][0]=='avaya','Tenant name not getting set in SHM'

    def test_AFCORE_5098(self):
        #there must be two tenants
        source=config['5098']['source']
        destination=config['5098']['dest']
        obj=swaggerData()
        obj.tenant_data_migration(source, destination, url)
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT c.name,a.\"data\" FROM public.component as c inner join public.configuration as a on a.id =c.\"activeConfigurationId\"  where \"tenantId\" = '"+source+"';")
        source_configuration_data = cursor.fetchall()
        print(source)
        print(source_configuration_data)
        cursor.execute(
            "SELECT c.name,a.\"data\" FROM public.component as c inner join public.configuration as a on a.id =c.\"activeConfigurationId\"  where \"tenantId\" = '" + destination + "';")
        destination_configuration_data = cursor.fetchall()
        print(destination)
        print(destination_configuration_data)
        for item in source_configuration_data:
            if item in destination_configuration_data:
                print(item)
                print('found')

            else:
                print(item)
                print('not found')
                assert False,item + ' not synced properly'

    def test_AFCORE_5098_RE(self):
        #there must be two tenants
        source=config['5098']['source']
        destination=config['5098']['dest']
        obj=swaggerData()
        obj.tenant_data_migration(source, destination, url)
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT key,data,type FROM public.routing_entity where \"tenantId\" ='"+source+"';")
        source_RE_data = cursor.fetchall()
        print(source)
        print(source_RE_data)
        cursor.execute(
            "SELECT key,data,type FROM public.routing_entity where \"tenantId\" ='" + destination + "';")
        destination_RE_data = cursor.fetchall()
        print(destination)
        print(destination_RE_data)
        for item in source_RE_data:
            if item in destination_RE_data:
                print(item)
                print('found')

            else:
                print(item)
                print('not found')
                assert False,item + ' re not synced properly'

#----------------------------------snapshots-2721------------------------------------------
    def delete_files(self,path):
        files = glob.glob(path)
        for f in files:
            os.remove(f)
    def get_latest_file(self,path):
        list_of_files = glob.glob(path)  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file.replace('\'', '\'\'')
        return latest_file

    def test_2721_create_snapshot(self,config_fresh_start):
        tenant=config['2721']['tenant']
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        obj=swaggerData()
        with open("2721/config-export.json", "r") as f:
            config_body = f.read()
        status=obj.config_import(url,tenant,config_body)
        with open("2721/re-export.json", "r") as f:
            re_body = f.read()
        status_re = obj.re_import(url, tenant, re_body)
        if status < 300 and status_re < 300:
            pass
        else:
            assert False, 'Configurations and Routing Entities are not getting imported'
        r=obj.create_snapshot(tenant,url)
        assert r.status_code < 300,'Snaptshot not created successfully'

    def test_restore_snapshot(self):
        tenant = config['2721']['tenant']
        obj=swaggerData()
        obj.delete_components('avaya', url)
        s=obj.get_snapshot(tenant,url)
        if  s.json() != []:
            Current_Date = datetime.date.today()
            previous_date= Current_Date - datetime.timedelta(days = 1)
            print (previous_date)
            start=str(previous_date)+'T00:00:00Z'
            end=str(Current_Date) + 'T23:59:59Z'
            status=obj.restore_snapshot(tenant,url,start,end)
            print(status.content.decode())
        else:
            assert False, 'Snapshot not found'
        assert status.status_code < 300, 'Snapshot restoration failed'

    def test_compare_snapshot_data(self):
        #self.delete_files('C:\\Users\\Hira.Wahid\\Downloads\\temp\\*')
        self.driver = AfWebDriver().get_firefox_driver()
        obj = portal()
        base_url = url + ":" + str(8080)
        obj.login(base_url, self.driver)
        obj.goto_component_config(base_url, self.driver)
        self.driver.find_element_by_xpath("//*[text() = 'Export']").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//button[text() = 'Add All Items']").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//button[text() = 'Save']").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[text() = 'Routing Entity']").click()
        time.sleep(10)
        latest_file=self.get_latest_file('C:\\Users\\Hira.Wahid\\Downloads\\temp\\*')
        #C:\\Users\\Hira.Wahid\\Downloads\\temp\\RoutingEntitiesExportFile.json
        with open(latest_file) as json_file:
            data = json.load(json_file)
        print(data)
        exported_components=data['components']
        #print(exported_components)
        e_comp=data['components']
        e_schemas=data['schemas']
        e_configurations=data['configurations']
        with open("2721/config-export.json", "r") as f:
           body = json.load(f)
        # print(body)
        imported_components=body['components']
        #print(imported_components)
        i_names=[]
        e_names=[]
        #comparing components------------
        for item in imported_components:
            i_names.append(item['name'])
        for item in exported_components:
            e_names.append(item['name'])
        e_names.sort()
        i_names.sort()
        print(e_names)
        print(i_names)
        for i in i_names:
            if i in e_names:
                pass
            else:
                assert False,'Components are not restored'
        # #----------comparing active configurations-----------------
        imported_ac=[]
        imported_configurations=[]
        for item in body['components']:
            imported_ac.append(item['activeConfigurationId'])
        print(imported_ac)
        for id in imported_ac:
            for con in body['configurations']:
                if con['id'] == id:
                    temp=con
                    temp['id']="0"
                    temp['schemaId'] = "0"
                    temp['componentId'] = "0"
                    imported_configurations.append(temp)
        print(imported_configurations)
        ex_ac = []
        ex_configurations = []
        for item in data['components']:
            ex_ac.append(item['activeConfigurationId'])
        print(ex_ac)
        for id in ex_ac:
            for con in data['configurations']:
                if con['id'] == id:
                    temp = con
                    temp['id'] = "0"
                    temp['schemaId']="0"
                    temp['componentId'] = "0"
                    ex_configurations.append(temp)
        print(ex_configurations)
        for i in imported_configurations:
            if i in ex_configurations:
                pass
            else:
                assert False,'Configurations are not restored'
        #self.delete_files('C:\\Users\\Hira.Wahid\\Downloads\\temp\\*')
        self.driver.find_element_by_xpath("//*[@class = 'mb-2']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'callflowCommand']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'callflowFunction']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'megaGlobalConfiguration']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'megaLocation']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'megaReasonCode']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'megaAesServer']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'customGroup']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@value = 'vectorVariable']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[text()= 'Export']").click()
        time.sleep(40)
        latest_file = self.get_latest_file('C:\\Users\\Hira.Wahid\\Downloads\\temp\\*')
        with open(latest_file) as json_file:
            RES = json.load(json_file)
        e_re=RES['routingEntities']
        for item in e_re:
            item['id']=0
            item['data']['createdAt']=0
            item['data']['updatedAt']=0
        print('exported')
        #print(e_re)
        print('r_re^')
        with open("2721/re-export.json", "r") as f:
            re = ijson.kvitems(f, 'routingEntities.item')
            entities=list(re).__len__()
        self.driver.quit()
        assert entities >= 113568, 'REs not imorted properly'

    def test_restore_latest_snapshot(self):
        tenant = config['2721']['tenant']
        obj = swaggerData()
        prev = obj.create_snapshot('avaya',url)
        print(prev.json()["name"])
        time.sleep(10)
        new = obj.create_snapshot('avaya',url)
        print(new.json()["name"])
        if prev.json() != [] and new.json() != []:
            Current_Date = datetime.date.today()
            previous_date = Current_Date - datetime.timedelta(days=1)
            print(previous_date)
            start = str(previous_date) + 'T00:00:00Z'
            end = str(Current_Date) + 'T23:59:59Z'
            status = obj.restore_snapshot(tenant, url, start, end)
            restored=status.content.decode()
            if new.json()["name"] in restored:
                test=True
            print(status.content.decode())
        else:
            assert False, 'Snapshot creation failed'
        assert status.status_code < 300 and test == True, 'Snapshot restoration failed'

    def test_restore_snapshot_no_snapshot_indb(self,config_fresh_start):
        tenant = config['2721']['tenant']
        obj = swaggerData()
        obj.delete_components('avaya', url)
        s = obj.get_snapshot(tenant, url)
        if s < 300:
            Current_Date = datetime.date.today()
            previous_date = Current_Date - datetime.timedelta(days=1)
            print(previous_date)
            start = str(previous_date) + 'T00:00:00Z'
            end = str(Current_Date) + 'T23:59:59Z'
            status = obj.restore_snapshot(tenant, url, start, end)
            print(status.content.decode())
        else:
            assert False, 'Snapshot not found'
        assert status.status_code < 300, 'Snapshot restoration failed'

    def test_2721_create_snapshot_no_Data(self,config_fresh_start):
        tenant=config['2721']['tenant']
        obj=swaggerData()
        r=obj.create_snapshot(tenant,url)
        print(r)
        if(r<300):
            pass
        else:
            assert False, 'Snaptshot not created'
        assert True

    #----------------------------------AFCORE-5928----------Regression-config-RE
    @pytest.fixture
    def config_fresh_start(self):
        fabric.tasks.execute(stop_v6_all)
        time.sleep(20)
        print('Services stopped successfully')
        fabric.tasks.execute(stop_config_v)
        time.sleep(20)
        fabric.tasks.execute(start_config)
        time.sleep(180)

    @pytest.fixture
    def config_upgrade(self):
        fabric.tasks.execute(start_config_upgrade)
        time.sleep(10)

    def test_create_REs_bulk(self,config_fresh_start):
        tenant=config['5928']['tenant']
        with open("airo/5928/re_export.json", "r") as f:
            body = f.read()
        obj=swaggerData()
        start = time.process_time()
        print(start)
        status=obj.re_import(url,tenant,body)
        print(time.process_time() - start)
        assert status < 300

    def test_update_REs_bulk(self):
        tenant=config['5928']['tenant']
        with open("airo/5928/re_export_updation.json", "r") as f:
            body = f.read()
        obj=swaggerData()
        start = time.process_time()
        print(start)
        status=obj.re_import(url,tenant,body)
        print(time.process_time())
        print(time.process_time() - start)
        assert status < 300

    def test_patch_REs(self):
        tenant=config['5928']['tenant']
        obj=swaggerData()
        # data=obj.get_re(tenant,url,'agentGroup')
        # print(data['enum'])
        # for id in data['enum']:
        status=obj.patch_re(tenant,url,'2641','agentGroup')
        assert status < 300, "patch not working properly"
    def test_config_upgrade_data_present(self,config_fresh_start):
        tenant = config['5928']['tenant']
        obj = swaggerData()
        with open("airo/5928/incomp_schema_ag.json", "r") as f:
            body = f.read()
        obj.schema_push(tenant,url,body,'agentGroup')
        with open("airo/5928/incomp_ag_export.json", "r") as f:
            body = f.read()
        status = obj.re_import(url, tenant, body)
        if status < 300:
            re_2892=obj.get_re_with_key(tenant,url,'agentGroup',2892)
            print(re_2892['data'])
        if 'slt_percent' in re_2892['data'] :
            print('yes')
            assert False, 'Import updated schema'
        else:
           fabric.tasks.execute(start_config_upgrade)
           time.sleep(180)
        re_2892 = obj.get_re_with_key(tenant, url, 'agentGroup', 2892)
        if 'slt_percent' not in re_2892['data'] :
            #print('yes')
            assert False, 'Config upgrade does not updated schema in specified time which is 3 minutes'
        else:
            assert True

    #-------------------------AFCORE-5348----------------------------------------------
    def test_set_creation_manual(self,config_fresh_start,config_upgrade):
        self.driver = AfWebDriver().get_firefox_driver()
        obj = portal()
        base_url = url + ":" + str(8080)
        obj.login(base_url, self.driver)
        obj.goto_component_config(base_url, self.driver)
        self.driver.find_element_by_xpath("//a[@href='/config/sets/add']").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//input[@class='form-input']").clear()
        time.sleep(5)
        self.driver.find_element_by_xpath("//input[@class='form-input']").send_keys('mytestset')
        time.sleep(5)
        swapToActive=self.driver.find_element_by_xpath("//*[contains(@class,'select__dropdown')]").click()
        swapToActive = self.driver.switch_to.active_element
        swapToActive.send_keys(Keys.RETURN)
        time.sleep(3)
        droplist=self.driver.find_elements_by_xpath("//*[contains(@class,'select__dropdown-indicator')]")
        print(droplist)
        droplist.pop(0)
        for item in droplist:
            swapToActive = item.click()
            swapToActive = self.driver.switch_to.active_element
            swapToActive.send_keys(Keys.RETURN)
            time.sleep(2)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        time.sleep(5)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Saved']")))
        activelabel=self.driver.find_element_by_xpath("//p[contains(text(),'Active Set')]").is_displayed()
        self.driver.quit()
        assert activelabel==True, 'Set is not avtivated by default'

    def test_set_creation_button(self, config_fresh_start, config_upgrade):
        self.driver = AfWebDriver().get_firefox_driver()
        obj = portal()
        base_url = url + ":" + str(8080)
        obj.login(base_url, self.driver)
        obj.goto_component_config(base_url, self.driver)
        self.driver.find_element_by_xpath("//a[@href='/config/sets/add']").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//input[@class='form-input']").clear()
        time.sleep(5)
        self.driver.find_element_by_xpath("//input[@class='form-input']").send_keys('mytestset')
        time.sleep(5)
        self.driver.find_element_by_xpath("//button[text()='Save Active Configurations']").click()
        #time.sleep(2)
        #self.driver.find_element_by_xpath("//button[text()='Save']").click()
        time.sleep(5)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Saved']")))
        activelabel = self.driver.find_element_by_xpath("//p[contains(text(),'Active Set')]").is_displayed()
        self.driver.quit()
        assert activelabel == True, 'Set is not avtivated by default'

    def test_activate_Set_button_availability(self):
        tenant = config['5348']['tenant']
        self.driver = AfWebDriver().get_firefox_driver()
        self.driver.implicitly_wait(5)
        obj = portal()
        base_url = url + ":" + str(8080)
        obj.login(base_url, self.driver)
        obj.goto_component_config(base_url, self.driver)
        ob=swaggerData()
        with open("5348/config-export.json", "r") as f:
            config_body = f.read()
        status=ob.config_import(url,tenant,config_body)
        self.driver.find_element_by_xpath("//*[text()='mytestset']").click()
        time.sleep(5)
        self.driver.refresh()
        wait=WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,"//button[text()='Activate Set']")))
        result=self.driver.find_element_by_xpath("//button[text()='Activate Set']").is_displayed()
        self.driver.quit()
        assert result==True,'Activate Set is not available for unactivated configuration'

    def test_activated_ids_match_activeconfigs(self):
        tenant = config['5348']['tenant']
        self.driver = AfWebDriver().get_firefox_driver()
        self.driver.implicitly_wait(5)
        obj = portal()
        base_url = url + ":" + str(8080)
        obj.login(base_url, self.driver)
        obj.goto_component_config(base_url, self.driver)
        self.driver.find_element_by_xpath("//*[text()='mytestset']").click()
        self.driver.find_element_by_xpath("//button[text()='Activate Set']").click()
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT \"activeConfigurationId\"	FROM public.component where \"tenantId\"='"+tenant+"'")
        comp_acid = cursor.fetchall()
        a=set(comp_acid)
        cursor.execute("SELECT id FROM public.set where name='mytestset'")
        set_id = cursor.fetchall()
        print(set_id)
        cursor.execute("SELECT \"configurationId\" FROM public.set_configuration_configuration where \"setId\"='"+set_id[0][0]+"'")
        set_conf_acids = cursor.fetchall()
        b=set(set_conf_acids)
        self.driver.quit()
        assert a==b,'Configurations activated successfully'

    def test_delete_set(self):
        tenant = config['5348']['tenant']
        self.driver = AfWebDriver().get_firefox_driver()
        self.driver.implicitly_wait(5)
        obj = portal()
        base_url = url + ":" + str(8080)
        obj.login(base_url, self.driver)
        obj.goto_component_config(base_url, self.driver)
        self.driver.find_element_by_xpath("//*[text()='mytestset']").click()
        self.driver.find_element_by_xpath("//button[text()='Delete']").click()
        self.driver.switch_to_alert().accept()
        wait=WebDriverWait(self.driver,20).until(EC.invisibility_of_element_located((By.XPATH,"//*[text()='mytestset']")))
        self.driver.quit()





