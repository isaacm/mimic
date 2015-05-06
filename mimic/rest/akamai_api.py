# -*- test-case-name: mimic.test.test_auth -*-
"""
Defines get current customer
"""

import datetime
import json
import random

from twisted.web.server import Request

from mimic.rest.mimicapp import MimicApp
from mimic.canned_responses import akamai

Request.defaultContentType = 'application/json'


class AkamaiApi(object):
    """
    Rest endpoints for mocked Akamai api.
    """

    app = MimicApp()

    def __init__(self, core):
        """
        :param MimicCore core: The core to which this AkamaiApi will be
            communicating.
        """
        self.core = core
        self.services = {}
        self.akamai_response = akamai.AkamaiResponse()

    @app.route('/partner-api/v1/network/production/properties/'
               '<string:customer_id>/sub-properties/'
               '<string:policy_name>/policy',
               methods=['PUT'])
    def create_policy(self, request, customer_id, policy_name):
        """
        Returns PUT policy.
        """
        data = request.content.read()
        response = self.akamai_response.create_policy(data,
                                                      customer_id, policy_name)
        return json.dumps(response[0])

    @app.route('/partner-api/v1/network/production/properties/'
               '<string:customer_id>/sub-properties/'
               '<string:policy_name>/policy',
               methods=['GET'])
    def get_policy(self, request, customer_id, policy_name):
        """
        Returns POST Service.
        """
        response = self.akamai_response.get_policy(policy_name)
        return json.dumps(response)

    @app.route('/partner-api/v1/network/production/properties/'
               '<string:customer_id>/sub-properties/'
               '<string:policy_name>/policy',
               methods=['DELETE'])
    def delete_policy(self, request, customer_id, policy_name):
        """
        Returns DELETE Policy.
        """
        response = self.akamai_response.delete_policy(customer_id, policy_name)
        return json.dumps(response)
    
    
    @app.route('/ccu/v2/queues/default',
               methods=['POST'])
    def purge_content(self, request):
        """
        Returns DELETE Policy.
        """
        request.setResponseCode(201)
        response = self.akamai_response.purge_content()
        return json.dumps(response)
      
    @app.route('/config-secure-provisioning-service/v1'
               '/sps-requests/',
               methods=['POST'])
    def sps_post(self, request):
        """
        Akamai Secure Provisioning Service endpoint.
        """
        spsId = random.randint(999,9999)
        jobId = random.randint(9999,99999)
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        request.setResponseCode(202)
        response = {
            "requestList":
                [{"resourceUrl": "/config-secure-provisioning-service/"
                                 "v1/sps-requests/%s" % str(spsId),
                 "lastStatusChange": now,
                    "spsId": spsId,
                    "status": "SUCCESS",
                    "jobId": jobId}]}
        return json.dumps(response)
    
    @app.route('/config-secure-provisioning-service/v1'
               '/sps-requests/<string:spsId>',
               methods=['GET'])
    def sps_get(self, request, spsId):
        """
        Akamai Secure Provisioning Service endpoint.
        """
        jobId = random.randint(9999,99999)
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        request.setResponseCode(200)
        response = { 'requestList': [   
            {   'jobId': jobId,
                'lastStatusChange': now,
                'resourceUrl': u'/config-secure-provisioning-service/v1/sps-requests/6632',
                'spsId': spsId,
                'status': u'SPS Request Complete'}]
            }
        return json.dumps(response)
    
    @app.route('/papi/v0/properties/<string:propertyId>/',
               methods=['GET'])
    def get_property_detail(self, request, propertyId):
        
        jobId = random.randint(9999,99999)
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        request.setResponseCode(200)
        response = {
          "properties" : {
            "items" : [ {
              "accountId" : "act_1-RMX47R",
              "contractId" : "ctr_C-2M6JYA",
              "groupId" : "grp_23174",
              "propertyId" : propertyId,
              "propertyName" : "ssl.altcdn.com_pm",
              "latestVersion" : 5,
              "stagingVersion" : 5,
              "productionVersion" : 5
            } ]
          }
        }
        return json.dumps(response)
    
    @app.route('/papi/v0/properties/<string:propertyId>/versions/<string:version>',
               methods=['GET'])
    def get_version_detail(self, request, propertyId, version):
        
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        request.setResponseCode(200)
        response = {
          "propertyId" : "prp_226831",
          "propertyName" : "ssl.altcdn.com_pm",
          "accountId" : "act_1-RMX47R",
          "contractId" : "ctr_C-2M6JYA",
          "groupId" : "grp_23174",
          "versions" : {
            "items" : [ {
              "propertyVersion" : version,
              "updatedByUser" : "dbartosh",
              "updatedDate" : now,
              "productionStatus" : "ACTIVE",
              "stagingStatus" : "DEACTIVATED",
              "productId" : "prd_Site_Del",
              "etag" : "d94e495db395c92eac894219cf96d69e1578cbfa"
            } ]
          }
        }
        return json.dumps(response)

    
    @app.route('/papi/v0/properties/<string:propertyId>/versions/',
               methods=['POST'])
    def post_new_version(self, request, propertyId):
        
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        request.setResponseCode(201)
        response = {
          "versionLink": "/papi/v0/properties/%s/versions/6?"
                         "contractId=ctr_C-2M6JYA&groupId=grp_23174" % propertyId
        }
        return json.dumps(response)
    
    @app.route('/papi/v0/properties/edgehostnames/',
               methods=['GET'])
    def get_edgehost_names(self, request):
        request.setResponseCode(200)
        response = {
            "accountId" : "act_1-RMX47R",
            "contractId" : "ctr_C-2M6JYA",
            "groupId" : "grp_23174",
            "edgeHostnames" : {
                "items" : [ {
                  "edgeHostnameId" : "ehn_284849",
                  "domainPrefix" : "stg2.cloudfiles.racklabs.com",
                  "domainSuffix" : "edgesuite.net",
                  "ipVersionBehavior" : "IPV4",
                  "secure" : False,
                  "edgeHostnameDomain" : "stg2.cloudfiles.racklabs.com.edgesuite.net"
                }, {
                  "edgeHostnameId" : "ehn_286611",
                  "domainPrefix" : "a0.rackcdn.com.mdc",
                  "domainSuffix" : "edgesuite.net",
                  "ipVersionBehavior" : "IPV6_COMPLIANCE",
                  "secure" : False,
                  "edgeHostnameDomain" : "a0.rackcdn.com.mdc.edgesuite.net"
                }]
            }
        }
        return json.dumps(response)


    @app.route('/papi/v0/properties/<string:propertyId>/versions/<string:version>/hostnames/',
               methods=['GET', 'PUT'])
    def get_host_names(self, request, propertyId, version):
        
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        request.setResponseCode(200)
        response = {
          "accountId" : "act_1-RMX47R",
          "contractId" : "ctr_C-2M6JYA",
          "groupId" : "grp_23174",
          "propertyId" : "prp_232289",
          "propertyName" : "san1.raxcdn.com_pm",
          "propertyVersion" : version,
          "etag" : "61af12161483eb402fc7f9396e714a4d72c6b184",
          "hostnames" : {
            "items" : [ {
              "cnameType" : "EDGE_HOSTNAME",
              "edgeHostnameId" : "ehn_1217865",
              "cnameFrom" : "secure1.san1.raxcdn.com",
              "cnameTo" : "secure1.san1.raxcdn.com.edgekey.net"
            }, {
              "cnameType" : "EDGE_HOSTNAME",
              "edgeHostnameId" : "ehn_1217859",
              "cnameFrom" : "secure2.san1.raxcdn.com",
              "cnameTo" : "secure2.san1.raxcdn.com.edgekey.net"
            }, {
              "cnameType" : "EDGE_HOSTNAME",
              "edgeHostnameId" : "ehn_1217860",
              "cnameFrom" : "secure3.san1.raxcdn.com",
              "cnameTo" : "secure3.san1.raxcdn.com.edgekey.net"
            }, {
              "cnameType" : "EDGE_HOSTNAME",
              "edgeHostnameId" : "ehn_1217861",
              "cnameFrom" : "secure4.san1.raxcdn.com",
              "cnameTo" : "secure4.san1.raxcdn.com.edgekey.net"
            }, {
              "cnameType" : "EDGE_HOSTNAME",
              "edgeHostnameId" : "ehn_1217862",
              "cnameFrom" : "secure5.san1.raxcdn.com",
              "cnameTo" : "secure5.san1.raxcdn.com.edgekey.net"
            }, {
              "cnameType" : "EDGE_HOSTNAME",
              "edgeHostnameId" : "ehn_1217863",
              "cnameFrom" : "secure6.san1.raxcdn.com",
              "cnameTo" : "secure6.san1.raxcdn.com.edgekey.net"
            }, {
              "cnameType" : "EDGE_HOSTNAME",
              "edgeHostnameId" : "ehn_1217864",
              "cnameFrom" : "secure7.san1.raxcdn.com",
              "cnameTo" : "secure7.san1.raxcdn.com.edgekey.net"
            } ]
          }
        }
        return json.dumps(response)
