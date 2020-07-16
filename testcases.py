import time
import fabric
#from dataentry import data
import pytest
from fabtest import *
from postgres import PostgresDB

@pytest.mark.parametrize("test_input,expected", [('Engine Common','CREATED'),('acdss','CREATED'),('async','CREATED'),('Routing Engine','CREATED'),('Avaya Switch Interface Configurations','CREATED'),('si','CREATED'),('ASLSync','CREATED'),('License','CREATED'),('dal','CREATED'),('Script Executor','CREATED'),('VHT Connector','CREATED'),('Databases','CREATED'),('Lookup','CREATED')])
def test_case_2_component_schema_CREATED_verification(test_input,expected):
        #components=['Engine Common','acdss','async','Routing Engine','Avaya Switch Interface Configurations','si','ASLSync','License','dal','Script Executor','VHT Connector','Databases','Lookup']
        # fabric.tasks.execute(stop_v6_all)
        # time.sleep(20)
        # print('Services stopped successfully')
        # fabric.tasks.execute(stop_config_v)
        # time.sleep(20)
        # fabric.tasks.execute(start_config)
        # time.sleep(20)
        # fabric.tasks.execute(start_config_upgrade)
        # time.sleep(20)
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT operation FROM public.component_log where \"componentName\" ='" +test_input+"' and operation ='"+expected+"'")
        record = cursor.fetchall()
        print(test_input+':')
        print(record)
        assert len(record)==1,'passed'



