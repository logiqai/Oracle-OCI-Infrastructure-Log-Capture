# Oracle-OCI-Infrastructure-Log-Capture

## Summary
* Utilizing OCI function and OCI service connector to create conduit to ingest OCI infrastructure logs into Apica data pipeline platform
* Files needed for implementing the feature
  * python OCI function handler: func.py
  * Configuration files: func.yaml, requiement.txt
  * func.yaml has fileds that user needs to manually filled
    * <end_point>, <ingest_token>, <namespace>, <appname>
  * The handler function can be customized to extract/filter the json field of OCI log payload.
  * Current OCI logs are in the form of JSON format:
```
{
   "datetime": 1723061051541,
   "logContent": {
     "data": {
       "msg": "\tTroubleshooting Tips: See https://docs.oracle.com/iaas/Content/API/References/apierrors.htm#apierrors_400__400_invalidparameter for more information about resolving this error."
     },
     "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
     "oracle": {
       "compartmentid": "ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
       "ingestedtime": "2024-08-07T20:05:09.650Z",
       "loggroupid": "ocid1.loggroup.oc1.us-sanjose-1.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
       "logid": "ocid1.log.oc1.us-sanjose-1.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
       "tenantid": "ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
       "tenantid": "ocid1.tenancy.oc1..aaaaaaaa36ve5oi3grywaezgro65tvvmia2gvnxmir5du6ezuzbcyzlwqera"
     },
     "source": "cloud-controller-manager",
     "specversion": "1.0",
     "time": "2024-08-07T20:04:11.541Z",
     "type": "com.oraclecloud.kubernetes.cluster.controlplane"
  },
  "regionId": "us-sanjose-1"
}
```
