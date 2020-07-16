import pytest

from dataentry_native import *
from fabtest import stop_v6_all, stop_config_v, start_config, start_config_upgrade
from postgres import PostgresDB
from swagapi import swaggerData

url="http://10.32.5.161"

class Test():
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        print('\nsetting up')
        #service must be started and working
        data.dataenter('airo/ct.txt', 'airo/ag_add.txt', 'airo/dn.txt',url);

    def test_1_set_new_awt(self):
        print('Verify that when a new profile is linked to AG then it gets notified dynamically in RE logs')
        obj=swaggerData()
        print('Adding new profile for awt:')
        obj.add_awt(url,'airo/awt.txt')
        print('updating Ag with new profile for awt:')
        obj.add_AG(url,'airo/1_ag_update.txt')
        #go to db routing entity table check 80051 has awtprofile=2

    def test_2_update_awt_value_on_linked_awt_profile(self):
        print('Verify that when a linked awt profile awt value is edited then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('Setting awt=50 for awt_id=2:')
        obj.add_awt(url, 'airo/2_awt_update_awt_profile.txt')

    def test_3_update_aawtmultiplier_value_on_linked_awt_profile(self):
        print('Verify that when a linked awt profile awt-multiplier value is edited then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('Setting aawt-multiplier=3 for awt_id=2:')
        obj.add_awt(url, 'airo/3_awt_update.txt')

    def test_5_update_awt_name_on_linked_awt_profile(self):
        print('Verify that when a linked awt profile name is edited then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('Setting awt name to awt-2 for awt_id=2:')
        obj.add_awt(url, 'airo/5_awt_update.txt')

    def test_4_disable_awt_on_linked_awt_profile(self): #critical
        print('Verify that when a linked awt profile is disabled then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('disabling awt_id=2:')
        obj.add_awt(url, 'airo/4_awt_update.txt')

    def test_8_enable_awt_on_linked_awt_profile(self): #critical
        print('Verify that when a linked awt profile is disabled then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('disabling awt_id=2:')
        obj.add_awt(url, 'airo/6_awt_update.txt')

    def test_6_monitor_mode_enable(self): #critical
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,\"activeConfigurationId\",\"tenantId\"	FROM public.component where name = '\"Engine Common\"'")
        record = cursor.fetchall()
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute(
            "Update public.configuration SET data->>\"General\"->>\"monitor_mode\" = True where id = '" +activeconfiguration+ "'")
        connection.commit()

    def test_7_monitor_mode_disable(self): #critical
        connection = PostgresDB().get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,\"activeConfigurationId\",\"tenantId\"	FROM public.component where name = '\"Engine Common\"'")
        record = cursor.fetchall()
        print('componentid:' + record[0][0])
        print('tenant:' + record[0][2])
        componentid = record[0][0]
        tenant = record[0][2]
        print('activeconfiguration:' + record[0][1])
        activeconfiguration = record[0][1]
        cursor.execute(
            "Update public.configuration SET data->>\"General\"->>\"monitor_mode\" = False where id = '" +activeconfiguration+ "'")
        connection.commit()

#-------------------------------------------------------------------------------------------------------------------------------------cwt

    def test_9_set_new_cwt(self):
        print('Verify that when a new cwt profile is linked to AG then it gets notified dynamically in RE logs')
        obj=swaggerData()
        print('Adding new profile for cwt:')
        obj.add_cwt(url,'airo/cwt_9.txt')
        print('updating Ag with new profile for cwt:')
        obj.add_AG(url,'airo/9_ag_update.txt')

    def test_10_update_cwt_value_on_linked_awt_profile(self):
        print('Verify that when a linked cwt profile cwt value is edited then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('Setting cwt=60 for cwt_id=2:')
        obj.add_cwt(url, 'airo/10_cwt_update.txt')

    def test_11_update_cwt_name_on_linked_cwt_profile(self):
        print('Verify that when a linked cwt profile name is edited then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('Setting awt name to cwt-2 for cwt_id=2:')
        obj.add_cwt(url, 'airo/11_cwt_update.txt')

    def test_12_disable_cwt_on_linked_awt_profile(self):
        print('Verify that when a linked cwt profile is disabled then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('disabling cwt_id=2:')
        obj.add_cwt(url, 'airo/12_cwt_update.txt')

    def test_13_enable_cwt_on_linked_ag_profile(self):
        print('Verify that when a linked cwt profile is disabled then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('enabling cwt_id=2:')
        obj.add_cwt(url, 'airo/13_cwt_update.txt')
#----------------------------------------------------------------cwt on ct-----------------------------------------------

    def test_14_set_new_cwt(self):
        print('Verify that when a new cwt profile is linked to CT then it gets notified dynamically in RE logs')
        obj=swaggerData()
        print('Adding new profile for cwt:')
        obj.add_cwt(url,'airo/cwt_9.txt')
        print('updating CT with new profile for cwt:')
        obj.add_ct(url,'airo/14_ct_update.txt')

    def test_15_update_cwt_value_on_linked_ct_profile(self):
        print('Verify that when a linked cwt profile cwt-value is edited then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('Setting cwt=60 for cwt_id=2:')
        obj.add_cwt(url, 'airo/10_cwt_update.txt')

    def test_16_update_cwt_name_on_linked_ct_profile(self):
        print('Verify that when a linked cwt profile name is edited then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('Setting awt name to cwt-2 for cwt_id=2:')
        obj.add_cwt(url, 'airo/11_cwt_update.txt')

    def test_17_disable_cwt_on_linked_ct_profile(self):
        print('Verify that when a linked cwt profile is disabled then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('disabling cwt_id=2:')
        obj.add_cwt(url, 'airo/12_cwt_update.txt')

    def test_18_enable_cwt_on_linked_ct_profile(self):
        print('Verify that when a linked cwt profile is disabled then it gets notified dynamically in RE logs')
        obj = swaggerData()
        print('enabling cwt_id=2:')
        obj.add_cwt(url, 'airo/13_cwt_update.txt')
#----Script Executor is currently listening to Add and Update operation on DN but limited to only benchmarks.-----------

    def test_19_set_new_bm_on_dn(self):
        print('Verify that when a new bm profile is linked to dn then it gets notified dynamically in SE logs')
        obj=swaggerData()
        print('Adding new profile for bm:')
        obj.add_bm(url,'airo/bm_19.txt')
        print('updating CT with new profile for cwt:')
        obj.add_ct(url,'airo/14_ct_update.txt')

    def test_20_disable_bm_on_dn(self):
        print('Verify that when a bm profile is disabled linked to dn then it gets notified dynamically in SE logs')
        obj=swaggerData()
        print('Adding new profile for bm:')
        obj.add_bm(url,'airo/bm_20.txt')

    def test_21_enable_bm_on_dn(self):
        print('Verify that when a bm profile is enabled linked to dn then it gets notified dynamically in SE logs')
        obj=swaggerData()
        print('Adding new profile for bm:')
        obj.add_bm(url,'airo/bm_21.txt')

    def test_22_cycleinmin_update_bm_on_dn(self):
        print('Verify that when a bm profile is enabled linked to dn then it gets notified dynamically in SE logs')
        obj=swaggerData()
        print('Adding new profile for bm:')
        obj.add_bm(url,'airo/bm_22.txt')

    def test_23_useleadingdigits_update_bm_on_dn(self):
        print('Verify that when a bm profile is enabled linked to dn then it gets notified dynamically in SE logs')
        obj=swaggerData()
        print('Adding new profile for bm:')
        obj.add_bm(url,'airo/bm_23.txt')

    def test_24_offpercentage_update_bm_on_dn(self):
        print('Verify that when a bm profile is enabled linked to dn then it gets notified dynamically in SE logs')
        obj=swaggerData()
        print('Adding new profile for bm:')
        obj.add_bm(url,'airo/bm_24.txt')
#------------------------------------------------------db-less-production