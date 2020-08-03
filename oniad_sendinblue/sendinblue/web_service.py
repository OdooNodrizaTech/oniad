# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import tools, _
import codecs

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
_logger = logging.getLogger(__name__)


class SendinblueWebService():

    def __init__(self, company, env):
        self.company = company
        self.custom_env = env
        self.api_key = tools.config.get('sendinblue_api_key')
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = self.api_key
        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        # configuration.api_key_prefix['api-key'] = 'Bearer'
        # create an instance of the API class
        self.api_instance_account_api = sib_api_v3_sdk.AccountApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        self.api_instance_contacts_api = sib_api_v3_sdk.ContactsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
    
    # get_attributes
    def get_attributes(self):
        response = {
            'errors': True,
            'error': "",
            'response': ""
        }
        try:
            api_response = self.api_instance_contacts_api.get_attributes()
            response['response'] = api_response
            response['errors'] = False            
        except ApiException as e:
            response['error'] = \
                _("Exception when calling AccountApi->get_account: %s") % e
        return response
        
    # get_folders
    def get_folders(self):
        response = {
            'errors': True,
            'error': "",
            'response': ""
        }
        try:
            api_response = self.api_instance_contacts_api.get_folders(10, 0)
            response['response'] = api_response
            response['errors'] = False            
        except ApiException as e:
            response['error'] = \
                _("Exception when calling AccountApi->get_account: %s") % e
        return response            
    
    # get_lists
    def get_lists(self):
        response = {
            'errors': True,
            'error': "",
            'response': ""
        }
        try:
            api_response = self.api_instance_contacts_api.get_lists()
            response['response'] = api_response
            response['errors'] = False            
        except ApiException as e:
            response['error'] = \
                _("Exception when calling AccountApi->get_account: %s") % e
        return response
        
    # get_contacts
    def get_contacts(self, limit=1000):
        response = {
            'errors': True,
            'error': "", 
            'response': "", 
        }
        try:
            api_response = self.api_instance_contacts_api.get_contacts(
                limit=10,
                offset=0
            )
            if api_response:
                pages_calculate = float(api_response.count)/float(limit)
                pages_calculate = "{0:.2f}".format(pages_calculate)
                pages_calculate_split = pages_calculate.split('.')
                if pages_calculate_split[1] != "00":
                    pages_calculate = int(pages_calculate_split[0])+1
                                        
                response['response'] = {
                    'count': api_response.count,
                    'contacts': []                    
                }                                        
                
                for i in range(1, pages_calculate+1):
                    offset = 0
                    if i > 1:
                        offset = limit*i
                        offset = offset-limit    
                    response_page = self.get_contacts_real(limit, offset)
                    if response_page:
                        response['response']['contacts'].extend(response_page.contacts)
                                    
                response['errors'] = False            
        except ApiException as e:
            response['error'] = \
                _("Exception when calling AccountApi->get_account: %s") % e
        return response
        
    def get_contacts_real(self, limit, offset):        
        try:
            return self.api_instance_contacts_api.get_contacts(
                limit=limit,
                offset=offset
            )
        except ApiException as e:
            return False
