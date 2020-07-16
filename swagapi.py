import csv
import urllib.parse
import json
import requests


class swaggerData():
    def login(self,url,api_port=9000):
        login_url = url + ":" + str(api_port) + "/keycloak/auth/realms/afiniti/protocol/openid-connect/token"
        # print(login_url)
        login_payload = "username=admin&password=admin&grant_type=password&client_id=afiniti-ui&client_secret="
        login_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                     'A': 'application/json, text/plain, */*'}
        response = requests.request("POST",login_url, headers=login_headers, data=login_payload)
        if response.status_code >= 200 and response.status_code < 300:
            json_rsponse = response.json()
            token = json_rsponse['access_token']
            print("Logged In")
            return token
        else:
            print("Login Failed. Status Code: " + str(response.status_code))
            return False

    def login_genesys(self,url,api_port=9000):
        login_url = url + ":" + str(api_port) + "/keycloak/auth/realms/afiniti/protocol/openid-connect/token"
        # print(login_url)
        login_payload = "username=admin1&password=admin&grant_type=password&client_id=afiniti-ui&client_secret="
        login_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                     'A': 'application/json, text/plain, */*'}
        response = requests.request("POST",login_url, headers=login_headers, data=login_payload)
        if response.status_code >= 200 and response.status_code < 300:
            json_rsponse = response.json()
            token = json_rsponse['access_token']
            print("Logged Into genesys")
            return token
        else:
            print("Login Failed. Status Code: " + str(response.status_code))
            return False

    def tenant_data_migration(self,source_tenant,dest_tenant,url):
        token = self.login(url, 9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        schema_del=url+':4000/tenant/source/'+source_tenant+'/target/'+dest_tenant;
        r = requests.put(schema_del, headers=headers)
        status = int(r.status_code)
        if status <= 300:
            print("Component " + source_tenant + " moved to "+dest_tenant+" successfully " + str(r.status_code))
        else:
            print("Component " + source_tenant+'-->'+dest_tenant + " migration failed " + str(r.status_code))

    def delete_components(self,tenant,url):
        token = self.login(url, 9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        schema_del=url+':4000/tenant/'+tenant+'/component'
        components = requests.get(schema_del, headers=headers)
        status = int(components.status_code)
        if status < 300:
            ids=components.json()
            print(ids)
            c_id=[]
            for i in ids:
                c_id.append(i['id'])
        for item in c_id:
            comp_del = url + ':4000/tenant/' + tenant + '/component/'+item
            del_s = requests.delete(comp_del, headers=headers)
            status = int(del_s.status_code)
            print(status)
        RE=['Agent','agentGroup','callType','dn','vector','benchmark','lineOfBusiness','holiday','cwt','awt','serviceProvider','skillGroup','airoDnToAgMapping','afinitiMode','acd']
        for item in RE:
            r=self.delete_RE(url,item)
            print(r)




    def create_snapshot(self,tenant,url):
        token = self.login(url, 9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        schema_del=url+':4000/tenant/'+tenant+'/snapshot/create'
        r = requests.put(schema_del, headers=headers)
        status = int(r.status_code)
        if status <= 300:
            print("Component " + tenant + " snapshot created successfully " + str(r.status_code))
        else:
            print("Component " + tenant+" snapshot creation failed " + str(r.status_code))
        return r

    def get_snapshot(self,tenant,url):
        token = self.login(url, 9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        schema_del=url+':4000/tenant/'+tenant+'/snapshot'
        r = requests.get(schema_del, headers=headers)
        status = int(r.status_code)
        print(r)
        if status <= 300:
            print("Component " + tenant + " snapshot taken successfully " + str(r.status_code))
        else:
            print("Component " + tenant+" snapshot failed " + str(r.status_code))
        return r

    def restore_snapshot(self,tenant,url,start,end):
        token = self.login(url, 9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        schema_del=url+':4000/tenant/'+tenant+'/snapshot/restoreByTimeRange/start/'+start+'/end/'+end
        r = requests.put(schema_del, headers=headers)
        status = int(r.status_code)
        print(r)
        if status <= 300:
            print("Component " + tenant + " snapshot restored successfully " + str(r.status_code))
        else:
            print("Component " + tenant+" snapshot restoration failed " + str(r.status_code))
        return r

    def component_deletion(self,componentid,tenant,url):
        token = self.login(url, 9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        schema_del=url+':4000/tenant/avaya'+'/component/'+componentid;
        r = requests.delete(schema_del, headers=headers)
        status = int(r.status_code)
        if status <= 300:
            print("Component " + componentid + " deleted successfully " + str(r.status_code))
        else:
            print("Component " + componentid + " deletion failed " + str(r.status_code))

    def configuration_deletion(self,componentid,schemaid,tenant,url,configurationid):
        token = self.login(url,9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        config_del=url+':4000/tenant/avaya/component/'+componentid+'/schema/'+schemaid+'/configuration/'+configurationid;
        #http://10.25.0.237:4000/tenant/avaya/component/47b8aa9c-484d-4e64-9c1d-8b93664b0c6d/schema/b35fb3ae-ac60-4014-9e25-d1ba64443f49/configuration/973b7a27-4fd6-4a84-a03f-382c28d5e285
        r = requests.delete(config_del,headers=headers)
        status = int(r.status_code)
        if status <= 300:
            print("Configuration " + componentid + " deleted successfully " + str(r.status_code))
        else:
            print("Configuration " + componentid + " deletion failed " + str(r.status_code))

    def check_echi_status(self,componentid,schemaid,confid,tenant,url):
        token = self.login(url,9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        _url=url+':4000/tenant/avaya/component/'+componentid+'/schema/'+schemaid+'/configuration/'+confid;
        r = requests.get(_url, headers=headers)
        status = int(r.status_code)
        res=r.json()
        return res['data']['archival_completed']

    def schema_deletion(self,componentid,schemaid,tenant,url):
        token = self.login(url,9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        config_del=url+':4000/tenant/avaya/component/'+componentid+'/schema/'+schemaid;
        #http://10.25.0.237:4000/tenant/avaya/component/47b8aa9c-484d-4e64-9c1d-8b93664b0c6d/schema/b35fb3ae-ac60-4014-9e25-d1ba64443f49/configuration/973b7a27-4fd6-4a84-a03f-382c28d5e285
        r = requests.delete(config_del,headers=headers)
        #resp=r.json()
        status = int(r.status_code)
        if status <= 300:
            print("Schema " + schemaid + " deleted successfully " + str(r.status_code))
        else:
            print("Schema " + schemaid + " deletion failed " + str(r.status_code))
        return status

    def add_acd(self,url,acd_file):
        token = self.login(url, 9000);
        api_port=9000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        acd_url = base_url + '/config/tenant/avaya/routing-entity/acd'
        with open(acd_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                acd_id=row[1]
                acd_body = {"routingEntityDtos": [{"key": str(row[0]), "data": {"id": int(row[1]), "name": str(row[2]), "tenantId": str(row[3])}}]}
            r = requests.post(acd_url, data=json.dumps(acd_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("acdID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                print("acdID: " + acd_id + " " + str(r.status_code))
            else:
                print("acdID: " + acd_id + " " + str(r.status_code))


    def export(self,url,tenant,componentid,schemaid,configurationid):
        token = self.login(url, 9000);
        api_port=4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        acd_url = base_url + '/' +tenant+ '/export'
        export_body = {
                "components": {
                "objects": [
                        {
        "id": componentid,
        "schemas": {
          "objects": [
            {
              "id": schemaid,
              "configurations": {
                "objects": [
                  configurationid
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
        r = requests.post(acd_url, data=json.dumps(export_body), headers=headers)
        status = int(r.status_code)
        response=r.json()
        if status >= 300:
            print("Export " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Export: " + componentid + str(r.status_code))
        else:
            print("Export: " + componentid + " " + str(r.status_code))
        return response

    def add_dn(self,url,dn_file):
        token = self.login(url, 9000);
        api_port=9000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        dnurl = base_url + '/config/tenant/avaya/routing-entity/dn'
        with open(dn_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                DN_id=row[1]
                oa=row[1]
                print(oa)
                dn_body = {"routingEntityDtos": [{"key": str(row[0]),
                                                  "data": {"originAnnouncement":int(row[1]) , "vectorId": row[2],
                                                           "number": row[3],
                                                           "acdId": row[4], "benchmark": row[5], "id":int(row[1]),
                                                           "isactive": True, "lobId": row[8], "name": str(row[9]),
                                                           "serviceproviderId": row[10], "enableForCms": True,
                                                           "internal_line_number": int(row[12]), "is_vht_callback": False,
                                                           "skill1": row[14], "skill2": row[15], "skill3": row[16],
                                                           "tenantId": row[17], "MonitoringType": int(1),
                                                           "Switch_instance_Id": row[19]}}]}
        r = requests.post(dnurl, data=json.dumps(dn_body), headers=headers)
        status = int(r.status_code)
        if status >= 300:
            print("DNID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("DNID: " + DN_id + " " + str(r.status_code))
        else:
            print("DNID: " + DN_id + " " + str(r.status_code))

    def add_awt(self,url,awt_file):
        token = self.login(url, 9000);
        api_port=9000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        dnurl = base_url + '/config/tenant/avaya/routing-entity/awt'
        with open(awt_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                awt_body = {"routingEntityDtos": [{"key": str(row[0]),
                                           "data": {"aawt_multiplier": int(row[1]), "awt": int(row[2]), "name": str(row[3]),
                                                    "tenantId": str(row[4]),
                                                    "enable_aawt": bool(row[5])}}]}
            r = requests.post(dnurl, data=json.dumps(awt_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("AWTID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                print("AWTID: " + row[0] + " " + str(r.status_code))
            else:
                print("AWTID: " + row[0] + " " + str(r.status_code))

    def add_ct(self,url,awt_file):
        token = self.login(url, 9000);
        api_port=9000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        dnurl = base_url + '/config/tenant/avaya/routing-entity/ct'
        with open(awt_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                ct_body = {"routingEntityDtos": [{"key": str(row[0]),
                                                  "data": {"vectorId": str(1), "V1": "1", "V2": "1", "V3": "1",
                                                           "V4": "1",
                                                           "V5": "1", "V6": "1", "V7": "1", "V8": "1", "V9": "1",
                                                           "number": str(row[0]), "channelType": "", "skill1": "",
                                                           "skill2": "", "skill3": "", "acdId": str(row[1]),
                                                           "id": int(row[0]), "isactive": bool(row[2]), "lobId": str(row[3]),
                                                           "name": str(row[0]), "serviceproviderId": str(row[4]),
                                                           "tenantId": str(row[5]),"cwt":str(row[6])}}]}
            r = requests.post(dnurl, data=json.dumps(ct_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("CWTID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                print("CWTID: " + row[0] + " " + str(r.json()))
            else:
                print("CWTID: " + row[0] + " " + str(r.json()))

    def add_cwt(self,url,cwt_file):
        token = self.login(url, 9000);
        api_port=9000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        dnurl = base_url + '/config/tenant/avaya/routing-entity/cwt'
        with open(cwt_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                cwt_body = {
                    "routingEntityDtos": [
                        {"key": str(row[0]), "data": {"cwt": int(row[1]), "ewt_multiplier": int(row[2]), "name": str(row[3]),
                                                 "tenantId": str(row[4]), "enable_ewt": bool(row[5])}}]}
            r = requests.post(dnurl, data=json.dumps(cwt_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("AWTID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                print("AWTID: " + row[0] + " " + str(r.status_code))
            else:
                print("AWTID: " + row[0] + " " + str(r.status_code))

    def add_AG(self,url,awt_file):
        token = self.login(url, 9000);
        api_port=9000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        dnurl = base_url + '/config/tenant/avaya/routing-entity/agentGroup'
        with open(awt_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                ag_body = {"routingEntityDtos": [{"key": str(row[0]),
                                                  "data": {"acdId": str(row[1]), "awt": str(row[2]), "cwt": str(row[3]), "lobId": str(row[4]),
                                                           "benchmarkId": int(row[5]), "channelType": str(row[6]),
                                                           "description": str(row[7]), "enableForCms": bool(row[8]),
                                                           "expression": row[9], "number": str(row[10]),
                                                           "slt_percent": int(row[11]), "slt_time": int(row[12]),
                                                           "serviceproviderId": row[13], "id": int(row[14]),
                                                           "name": str(row[15]),
                                                           "occupancy_threshold": int(row[16]),
                                                           "skill_number": int(row[17]), "tenantId": str(row[18]),
                                                           "isactive": bool(row[19])}}]}
            r = requests.post(dnurl, data=json.dumps(ag_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("AGID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                print("AGID: " + row[0] + " " + str(r.status_code))
            else:
                print("AGID: " + row[0] + " " + str(r.status_code))

    def add_bm(self,url,bm_file):
        token = self.login(url, 9000);
        api_port=9000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        dnurl = base_url + '/config/tenant/avaya/routing-entity/bm'
        with open(bm_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                bm_body = {
                        "routingEntityDtos": [{"key": str(row[0]), "data": {"lobId": str(row[1]), "serviceproviderId": str(row[2]), "acdId": str(row[3]),
                                                                       "benchmarkAlgorithm": str(row[4]),
                                                                       "benchmarkStartDate": str(row[5]),
                                                                       "cycleMinutes": int(row[6]), "isactive": row[7],
                                                                       "name": str(row[8]), "noOfDigits": int(row[9]),
                                                                       "offpercentage": int(row[10]), "useleadingDigits": row[11],
                                                                       "tenantId": row[12]}}]}
            r = requests.post(dnurl, data=json.dumps(bm_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("bmID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                print("bmID: " + row[0] + " " + str(r.status_code))
            else:
                print("bmID: " + row[0] + " " + str(r.status_code))

    def delete_RE(self,url,re):
        token = self.login(url, 9000);
        api_port = 4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        deleting_url = base_url + '/tenant/avaya/routing-entity/'+re
        print(deleting_url)
        r = requests.delete(deleting_url, headers=headers)
        status = int(r.status_code)
        if status >= 300:
            print("Routing_Entity: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Routing_Entity deletion failed: " + re + " " + str(r.status_code))
        else:
            print("Routing Entity deleted: " + re + " " + str(r.status_code))
        return status

    def i_import(self,url,tenant,body):
        if tenant == 'genesys':
            token = self.login_genesys(url, 9000);
        else:
            token = self.login(url, 9000);
        api_port=4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        import_url = base_url + '/' +tenant+ '/import'
        r = requests.post(import_url,body,headers=headers)
        status = int(r.status_code)
        if status >= 300:
            print("Import " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Import" + str(r.status_code))
        else:
            print("Import successful " + str(r.status_code))
        return status

    def re_import(self,url,tenant,body):
        if tenant == 'genesys':
            token = self.login_genesys(url, 9000);
        else:
            token = self.login(url, 9000);
        api_port=4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        import_url = base_url + '/' +tenant+ '/import/re'
        r = requests.post(import_url,body,headers=headers)
        status = int(r.status_code)
        if status >= 300:
            print("Import " + str(r.status_code) + " " + str(r.reason)+ " " + str(r.json()))
            print("Import" + str(r.status_code))
        else:
            print("Import successful " + str(r.status_code))
        return status

    def config_import(self,url,tenant,body):
        if tenant == 'genesys':
            token = self.login_genesys(url, 9000);
        else:
            token = self.login(url, 9000);
        api_port=4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        import_url = base_url + '/' +tenant+ '/import'
        r = requests.post(import_url,body.encode('utf-8'),headers=headers)
        status = int(r.status_code)
        if status >= 300:
            print("Import " + str(r.status_code) + " " + str(r.reason)+ " " + str(r.json()))
            print("Import" + str(r.status_code))
        else:
            print("Import successful " + str(r.status_code))
        return status

    def export_re(self, url, tenant,re):
        token = self.login(url, 9000);
        api_port = 4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        acd_url = base_url + '/' + tenant + '/export/re?'+re+'='
        r = requests.get(acd_url, headers=headers)
        status = int(r.status_code)
        response = r.json()
        if status >= 300:
            print("Export " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Export: " + re + str(r.status_code))
        else:
            print("Export: " + re + " " + str(r.status_code))
        return response
    def create_si(self,tenant,url):
        token = self.login(url, 9000);
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}

        url_si='http://10.32.5.46:9000/aes/aes/AVAYA%23CM713%23CSTA-S%23PLAT2AES/450/afiniti/S@tmap01/1/10'
        #url_si='http://10.25.0.199:9000/aes/cms/informix/10.32.17.113/50000/root/P@ssword/cms_net/onsoctcp'

        #url_si='http://10.32.5.46:9000/aes/cms/ssh/10.32.17.113/root/P@ssword1'
        r = requests.get(url_si, headers=headers)
        status = int(r.status_code)
        print(r.json())

    def get_re(self,tenant,url,re):
        #tenant/avaya/routing-entity/agentGroup/lookup
        token = self.login(url, 9000);
        api_port = 4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        acd_url = base_url +'/tenant/avaya/routing-entity/' + re + '/lookup'
        r = requests.get(acd_url, headers=headers)
        status = int(r.status_code)
        response = r.json()
        if status >= 300:
            print("Export " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Export: " + re + str(r.status_code))
        else:
            print("Export: " + re + " " + str(r.status_code))
        return response

    def patch_re(self,tenant,url,id,re):
        #tenant/avaya/routing-entity/agentGroup/lookup
        token = self.login(url, 9000);
        api_port = 4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        acd_url = base_url +'/tenant/'+tenant+'/routing-entity/' + re
        body="{\"routingEntityDtos\": [ { \"key\": \""+id+"\", \"data\": {\"slt_percent\":0} } ]}"
        r = requests.patch(acd_url,body,headers=headers)
        status = int(r.status_code)
        response = r.json()
        if status >= 300:
            print("Export " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Export: " + re + str(r.status_code))
        else:
            print("Export: " + re + " " + str(r.status_code))
        return status

    def schema_push(self,tenant,url,body,re):
        #tenant/avaya/routing-entity/agentGroup/lookup
        token = self.login(url, 9000);
        api_port = 4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        acd_url = base_url +'/tenant/'+tenant+'/routing-entity/' + re+'/schema'
        r = requests.post(acd_url,body,headers=headers)
        status = int(r.status_code)
        response = r.json()
        if status >= 300:
            print("Export " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Export: " + re + str(r.status_code))
        else:
            print("Export: " + re + " " + str(r.status_code))
        return status

    def get_re_with_key(self,tenant,url,re,key):
        #tenant/avaya/routing-entity/agentGroup/lookup
        token = self.login(url, 9000);
        api_port = 4000
        auth = "Bearer " + token
        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}
        base_url = url + ":" + str(api_port)
        acd_url = base_url +'/tenant/avaya/routing-entity/' + re + '/'+ str(key)
        r = requests.get(acd_url, headers=headers)
        status = int(r.status_code)
        response = r.json()
        if status >= 300:
            print("Export " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
            print("Export: " + re + str(r.status_code))
        else:
            print("Export: " + re + " " + str(r.status_code))
        return response





if __name__ == '__main__':
    obj=swaggerData()
    #obj.add_dn('http://10.25.0.237', 'RE_updation_scenario/dn_file')
    #obj.delete_RE('http://10.25.0.237', 'dn')
    #obj.configuration_deletion('47b8aa9c-484d-4e64-9c1d-8b93664b0c6d','b35fb3ae-ac60-4014-9e25-d1ba64443f49','avaya','http://10.25.0.237','973b7a27-4fd6-4a84-a03f-382c28d5e285')
    # resp=obj.export('http://10.25.0.237','avaya','afc6a3eb-2ceb-41d5-9fd5-dac52876e46e','89eecf26-1545-4755-a928-b6bbd5cf8a7a','e9c2307f-f5d2-4e29-a186-66d81b685226')
    # r=json.dumps(resp)
    # obj.i_import('http://10.25.0.237','avaya',r)
    # resp=obj.export_re('http://10.25.0.236','avaya','agentGroup')
    # print(resp)
    # r = json.dumps(resp)
    # obj.re_import('http://10.25.0.236','genesys',r)
    #obj.create_si('avaya','http://10.32.5.46')
    obj.delete_components('avaya','http://10.25.0.236')