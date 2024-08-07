import io
import os
import json
import requests
import logging

## example OCI infrastructure log
## {
##   "datetime": 1723061051541,
##   "logContent": {
##     "data": {
##       "msg": "\tTroubleshooting Tips: See https://docs.oracle.com/iaas/Content/API/References/apierrors.htm#apierrors_400__400_invalidparameter for more information about resolving this error."
##     },
##     "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
##     "oracle": {
##       "compartmentid": "ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
##       "ingestedtime": "2024-08-07T20:05:09.650Z",
##       "loggroupid": "ocid1.loggroup.oc1.us-sanjose-1.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
##       "logid": "ocid1.log.oc1.us-sanjose-1.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
##       "tenantid": "ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
##       "tenantid": "ocid1.tenancy.oc1..aaaaaaaa36ve5oi3grywaezgro65tvvmia2gvnxmir5du6ezuzbcyzlwqera"
##     },
##     "source": "cloud-controller-manager",
##     "specversion": "1.0",
##     "time": "2024-08-07T20:04:11.541Z",
##     "type": "com.oraclecloud.kubernetes.cluster.controlplane"
##  },
##  "regionId": "us-sanjose-1"
##}

def process(body):
    try:
        namespace = os.environ['APICA_NAMESPACE']
        appname = os.environ['APICA_APPNAME']
        time = body.get("time")

        ## one can create filtered logs here
        ##get json data, time, and source information
        #data = body.get("data", {}) 
        #source = body.get("source") 
        #service = "OCI Logs"
        #payload = {}
        #payload.update({"source":source}) 
        #payload.update({"time": time}) 
        #payload.update({"timestamp": time}) 
        #payload.update({"data":data})
        #payload.update({"namespace": namespace}) 
        #payload.update({"appname": service}) 
        #payload.update({"service":service})
        
        # get all 
        payload = body
        payload.update({"namespace": namespace}) 
        payload.update({"appname": appname}) 
        payload.update({"timestamp": time})
        

        #Apica endpoint URL and token to call the REST interface. These are defined in the func.yaml file. 
        apicahost = os.environ['APICA_HOST']
        apicatoken = os.environ['APICA_TOKEN']

        #Invoke Apica API with the payload. If the payload contains more than one log this will be ingested as once. 
        #headers = {'Content-type': 'application/json', 'DD-API-KEY': apicatoken}
        headers = {'Content-type': 'application/json', 'Authorization': apicatoken}
        x = requests.post(apicahost, data = json.dumps(payload), headers=headers) 
        logging.getLogger().info("OCI handler response=%s", x.text)

    except (Exception, ValueError) as ex:
        logging.getLogger().error("process exit err=%s", str(ex))


"""
This function receives the logging json and invokes the Apica endpoint for ingesting logs. https://docs.cloud.oracle.com/en-us/iaas/Content/Logging/Reference/top_level_logging_format. htm#top_level_logging_format
If this Function is invoked with more than one log the function go over each log and invokes the Apica endpoint for ingesting one by one.
"""
def handler(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue())
        if isinstance(body, list):
            # Batch of CloudEvents format
            for b in body:
                process(b)
        else:
            # Single CloudEvent
            process(body)
    except (Exception, ValueError) as ex:
        logging.getLogger().error("handler exit err=%s", str(ex))
