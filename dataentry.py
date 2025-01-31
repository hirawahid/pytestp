import requests
import json
import threading
import time
import logging
import csv
class data():
    def dataenter(ct,ag,dn,url):
        # setting up parameters for requests
        # url = "http://10.25.0.236"
        api_port = "9000"
        login_port = "8080"
        base_url = url + ":" + api_port
        request_interval = 0.05  # seconds

        # setting up parameters other than ags to be added manually
        acdId = "1"
        awt = "1"
        cwt = "1"
        lobId = "1"
        serviceproviderid = "1"
        occupancy_threshold = 0
        tenantId = "avaya"
        isactive = True
        benchmark = "1"

        benchmarkId = 1
        channelType = "1"
        description = "description"
        enableForCms = False
        expression = "Skill1 > 0 & Skill2 > 0 & Skill3 > 0"
        number = "1"
        slt_percent = 0
        slt_time = 0
        vktr = "[{ \t\"Command\": \"var\", \t\"Expression\": \"\", \t\"P1\": \"attachedDataMap\", \t\"P2\": \"map<string, string>\", \t\"P3\": \"vector\", \t\"P4\": \"\", \t\"P5\": \"getAttachedDataMap(vectorExecutionContext.callID, \\\"=\\\", \\\"|\\\")\", \t\"Step\": \"1\" }, { \t\"Command\": \"var\", \t\"Expression\": \"\", \t\"P1\": \"target_expression\", \t\"P2\": \"string\", \t\"P3\": \"vector\", \t\"P4\": \"\", \t\"P5\": \"\", \t\"Step\": \"2\" }, { \t\"Command\": \"set\", \t\"Expression\": \"\", \t\"P1\": \"target_expression\", \t\"P2\": \"[=]() -> string{ if(vector->attachedDataMap.count(\\\"TargetExpression\\\") == 1) { return vector->attachedDataMap[\\\"TargetExpression\\\"].erase(0,1).erase(vector->attachedDataMap[\\\"TargetExpression\\\"].size()-1, 1); ; } return \\\"\\\"; }()\", \t\"P3\": \"vector\", \t\"P4\": \"\", \t\"P5\": \"\", \t\"Step\": \"3\" }, { \t\"Command\": \"var\", \t\"Expression\": \"return true\", \t\"P1\": \"ag_id_from_exp\", \t\"P2\": \"int\", \t\"P3\": \"vector\", \t\"P4\": \"\", \t\"P5\": \"getAGFromExp(vector->target_expression)\", \t\"Step\": \"4\" }, { \t\"Command\": \"QueueToAG\", \t\"Expression\": \"\", \t\"P1\": \"vector->ag_id_from_exp\", \t\"P2\": \"1\", \t\"P3\": \"\", \t\"P4\": \"\", \t\"P5\": \"false\", \t\"Step\": \"5\" }]"
        success_ag = 0
        #failed_ag = 0

        def login():

            login_url = url + ":" + api_port + "/keycloak/auth/realms/afiniti/protocol/openid-connect/token"
            # print(login_url)
            login_payload = "username=admin&password=admin&grant_type=password&client_id=afiniti-ui&client_secret="
            login_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                             'A': 'application/json, text/plain, */*'}
            response = requests.request("POST", login_url, headers=login_headers, data=login_payload)

            if response.status_code >= 200 and response.status_code < 300:
                json_rsponse = response.json()
                token = json_rsponse['access_token']
                logging.info("Logged In")
                return token
            else:
                logging.error("Login Failed. Status Code: " + str(response.status_code))
                return False

        def ag_request(agent_id, url, body, headers):
            global success_ag
            global failed_ag
            r = requests.post(url, data=json.dumps(body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                # print(name+": "+str(r.status_code)+" "+str(r.json))
                success_ag = success_ag + 1
                logging.error("AG: " + agent_id + " " + str(r.status_code))
            else:
                # print(name+": "+str(r.status_code))
                #failed_ag = failed_ag + 1
                logging.info("AG: " + agent_id + " " + str(r.status_code))
            # pass

        def dn_request(dn_id, dn_url, dn_body, headers):
            r = requests.post(dn_url, data=json.dumps(dn_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("DN: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("DN: " + dn_id + " " + str(r.status_code) + " " + str(r.json()))
            # pass
            else:
                # print("DN: "+str(r.status_code))
                logging.info("DN: " + dn_id + " " + str(r.status_code))
            # pass

        def ct_request(ct_id, ct_url, ct_body, headers):
            r = requests.post(ct_url, data=json.dumps(ct_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("CT: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("CT: " + ct_id + " " + str(r.status_code))
            # pass
            else:
                # print(str(count)+"CT: "+str(r.status_code))
                logging.info("CT: " + ct_id + " " + str(r.status_code))
            # pass

        def v_request(v_id, v_url, v_body, headers):

            # Vector Request
            r = requests.post(v_url, data=json.dumps(v_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("Vector: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("Vector: " + v_id + " " + str(r.status_code))
            # pass
            else:
                # print(str(count)+"Vector: "+str(r.status_code))
                logging.info("Vector: " + v_id + " " + str(r.status_code))
            # pass

        def cwt_request(cwt_id, cwt_url, cwt_body, headers):

            # Vector Request
            r = requests.post(cwt_url, data=json.dumps(cwt_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("CWT: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("CWT: " + cwt_id + " " + str(r.status_code))
            # pass
            else:
                logging.info("CWT: " + cwt_id + " " + str(r.status_code))
            # pass

        def awt_request(awt_id, awt_url, awt_body, headers):

            # Vector Request
            r = requests.post(awt_url, data=json.dumps(awt_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("AWT: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("AWT: " + awt_id + " " + str(r.status_code))
            # pass
            else:
                logging.info("AWT: " + awt_id + " " + str(r.status_code))
            # pass

        def sid_request(sp_id, sid_url, sid_body, headers):

            # Vector Request
            r = requests.post(sid_url, data=json.dumps(sid_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("SPID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("SPID: " + sp_id + " " + str(r.status_code))
            # pass
            else:
                logging.info("SPID: " + sp_id + " " + str(r.status_code))
            # pass

        def lob_request(lob_id, lob_url, lob_body, headers):

            # Vector Request
            r = requests.post(lob_url, data=json.dumps(lob_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("lobID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("lobID: " + lob_id + " " + str(r.status_code))
            # pass
            else:
                logging.info("lobID: " + lob_id + " " + str(r.status_code))
            # pass

        def bm_request(bm_id, bm_url, bm_body, headers):

            # Vector Request
            r = requests.post(bm_url, data=json.dumps(bm_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("bmID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("bmID: " + bm_id + " " + str(r.status_code))
            # pass
            else:
                logging.info("bmID: " + bm_id + " " + str(r.status_code))
            # pass

        def acd_request(acd_id, acd_url, acd_body, headers):

            # Vector Request
            r = requests.post(acd_url, data=json.dumps(acd_body), headers=headers)
            status = int(r.status_code)
            if status >= 300:
                print("acdID: " + str(r.status_code) + " " + str(r.reason) + " " + str(r.json()))
                logging.error("acdID: " + acd_id + " " + str(r.status_code))
            # pass
            else:
                logging.info("acdID: " + acd_id + " " + str(r.status_code))
            # pass

        print("Logging in " + url + '\n')
        logging.info("Logging in " + url)
        token = login()
        auth = "Bearer " + str(token)

        agurl = base_url + '/config/tenant/avaya/routing-entity/agentGroup'
        dnurl = base_url + '/config/tenant/avaya/routing-entity/dn'
        cturl = base_url + '/config/tenant/avaya/routing-entity/callType'
        v_url = base_url + '/config/tenant/avaya/routing-entity/vector'

        headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Content-type': 'application/json',
                   'Accept': 'application/json, text/plain, */*', 'Authorization': auth}

        # adding basic Service provider ID
        sid_url = base_url + '/config/tenant/avaya/routing-entity/serviceProvider'
        sid_body = {"routingEntityDtos": [{"key": str(1), "data": {"id": 1, "name": "sp1", "tenantId": "avaya"}}]}
        thread = threading.Thread(target=sid_request, args=(str(1), sid_url, sid_body, headers))
        thread.start()
        thread.join()

        # adding basic Line of Business ID
        lob_url = base_url + '/config/tenant/avaya/routing-entity/lineOfBusiness'
        lob_body = {"routingEntityDtos": [{"key": str(1),
                                           "data": {"monitor_mode": False, "alphaId": "2", "id": 1, "isactive": True,
                                                    "name": "lob2", "tenantId": "avaya"}}]}
        thread = threading.Thread(target=lob_request, args=(str(1), lob_url, lob_body, headers))
        thread.start()
        thread.join()

        # add acdID here logical manner
        acd_url = base_url + '/config/tenant/avaya/routing-entity/acd'
        acd_body = {"routingEntityDtos": [{"key": str(1), "data": {"id": 1, "name": "1", "tenantId": "avaya"}}]}
        thread = threading.Thread(target=acd_request, args=(str(1), acd_url, acd_body, headers))
        thread.start()
        thread.join()

        # adding basic BM
        bm_url = base_url + '/config/tenant/avaya/routing-entity/benchmark'
        bm_body = {"routingEntityDtos": [{"key": str(1), "data": {"lobId": "1", "serviceproviderId": "1", "acdId": "1",
                                                                  "benchmarkAlgorithm": "Inline BTN",
                                                                  "benchmarkStartDate": "2018-12-31 19:48:12",
                                                                  "cycleMinutes": int(2), "isactive": True,
                                                                  "name": "inlinebtn", "noOfDigits": int(2),
                                                                  "offpercentage": int(48), "useleadingDigits": True,
                                                                  "tenantId": "avaya"}}]}
        thread = threading.Thread(target=bm_request, args=(str(1), bm_url, bm_body, headers))
        thread.start()
        thread.join()

        # adding basic vector
        v_body = {"routingEntityDtos": [{"key": str(1),
                                         "data": {"acdId": acdId, "id": int(1), "isactive": isactive, "number": "1",
                                                  "lobId": lobId, "name": str('GV'),
                                                  "serviceproviderId": serviceproviderid,
                                                  "tenantId": tenantId, "vectorjson": vktr}}]}
        thread = threading.Thread(target=v_request, args=(str(1), v_url, v_body, headers))
        thread.start()
        thread.join()

        # adding basic cwt
        cwt_url = base_url + '/config/tenant/avaya/routing-entity/cwt'
        cwt_body = {
            "routingEntityDtos": [{"key": str(1), "data": {"cwt": int(10), "ewt_multiplier": int(1), "name": "cwt1",
                                                           "tenantId": "avaya", "enable_ewt": True}}]}
        thread = threading.Thread(target=cwt_request, args=(str(1), cwt_url, cwt_body, headers))
        thread.start()
        thread.join()

        # adding basic awt
        awt_url = base_url + '/config/tenant/avaya/routing-entity/awt'
        awt_body = {"routingEntityDtos": [{"key": str(1),
                                           "data": {"aawt_multiplier": 1, "awt": 15, "name": "awt1",
                                                    "tenantId": "avaya",
                                                    "enable_aawt": True}}]}
        thread = threading.Thread(target=awt_request, args=(str(1), awt_url, awt_body, headers))
        thread.start()
        thread.join()

        with open(ag) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                ag_body = {"routingEntityDtos": [{"key": str(row[0]),
                                                  "data": {"acdId": acdId, "awt": "1", "cwt": "1", "lobId": lobId,
                                                           "benchmarkId": benchmarkId, "channelType": channelType,
                                                           "description": description, "enableForCms": enableForCms,
                                                           "expression": row[1], "number": str(row[0]),
                                                           "slt_percent": slt_percent, "slt_time": slt_time,
                                                           "serviceproviderId": serviceproviderid, "id": int(row[0]),
                                                           "name": str(row[0]),
                                                           "occupancy_threshold": occupancy_threshold,
                                                           "skill_number": int(row[0]), "tenantId": tenantId,
                                                           "isactive": isactive}}]}
                thread = threading.Thread(target=ag_request, args=(str(row[0]), agurl, ag_body, headers))
                thread.start()
                thread.join()
                time.sleep(request_interval)
                line_count += 1

        with open('dn.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader: # dn picking id from row 0 and name from row 1
                dn_body = {"routingEntityDtos": [{"key": str(row[0]),
                                                  "data": {"originAnnouncement": {}, "vectorId": str(1),
                                                           "number": number,
                                                           "acdId": acdId, "benchmark": benchmark, "id": int(row[0]),
                                                           "isactive": isactive, "lobId": lobId, "name": str(row[1]),
                                                           "serviceproviderId": serviceproviderid, "enableForCms": True,
                                                           "internal_line_number": int(1), "is_vht_callback": False,
                                                           "skill1": "0", "skill2": "0", "skill3": "0",
                                                           "tenantId": tenantId, "MonitoringType": int(1),
                                                           "Switch_instance_Id": "1"}}]}
                thread = threading.Thread(target=dn_request, args=(str(row[0]), dnurl, dn_body, headers))
                thread.start()
                thread.join()
                time.sleep(request_interval)
                line_count += 1

        with open('ct.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                ct_body = {"routingEntityDtos": [{"key": str(row[0]),
                                                  "data": {"vectorId": str(1), "V1": "0", "V2": "0", "V3": "0",
                                                           "V4": "0",
                                                           "V5": "0", "V6": "0", "V7": "0", "V8": "0", "V9": "0",
                                                           "number": number, "channelType": "0", "skill1": "0",
                                                           "skill2": "0", "skill3": "0", "acdId": acdId, "cwt": "1",
                                                           "id": int(row[0]), "isactive": isactive, "lobId": lobId,
                                                           "name": str(row[0]), "serviceproviderId": serviceproviderid,
                                                           "tenantId": tenantId}}]}
                thread = threading.Thread(target=ct_request, args=(str(row[0]), cturl, ct_body, headers))
                thread.start()
                thread.join()

if __name__ == '__main__':
    data.dataenter('ct.txt','ag.txt','dn.txt',"http://10.25.0.237")