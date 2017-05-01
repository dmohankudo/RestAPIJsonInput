'''
This client invokes  API's with json input and 
client authentication and verifies the response
__maintaner__: debaditya mohankudo 

guidelines: 
call all function using keywords -> helps to shuffle order

why to use @proprties
https://www.programiz.com/python-programming/property
'''
from logging import basicConfig, debug, DEBUG, error, info
from  os import path, makedirs
from requests import  Session
from requests.packages.urllib3.exceptions import NewConnectionError, NewConnectionError
from time import ctime


log_dir = 'LOG' 
if not path.isdir(log_dir):
    makedirs(log_dir)







def compare_values(_value1, _value2):
    return _value1==_value2, _value1, _value2


class API(object):
    """ API access using client cert and verify response
       No function returns
    """

    def __init__(self, _base_url, _client_cert, _api):
        '''
        @baseurl: https://xxxxxxxxxxxxxxxxxxxxx.xxx
        @client_cert : client cert in pem format
        '''
        self.host = _base_url
        self.__client_cert = _client_cert
        self.api = _api
        # create pass and fail directory
        logfile_name = 'APILog_' + _api + '_'
        logfile_name += ctime().replace(' ', '-').replace(':', '_')
        logfile_path = path.join(path.abspath(log_dir), logfile_name)

        basicConfig(filename=logfile_path ,level=DEBUG)

        info('client cert is {cert}'.format(cert=self.client_cert))

    @property
    def client_cert(self):
        if self.__client_cert.endswith('.pem'):
            return self.__client_cert

    @property
    def endpoint_url(self):
        ''' returns end poit url '''

        return '{base}/vswebservices/config/{api}'.format(
            base=self.host,
            api=self.api)

    def create_session(self):
        self.session = Session()
 

    def set_authentication_values(self):
        self.create_session()
        self.session.cert = self.client_cert

    def post_request(self, _data_json):
        self.set_authentication_values()
        self.response = self.session.post(url=self.endpoint_url, json=_data_json)

    def invoke_api(self, _data_json=None):
        '''Call  api with test data, the last two argument not used yet'''
        
        info('post data is:{d}'.format(d=_data_json))
        self.post_request(_data_json=self.tc_post_data)
        info('response is: {r}-{code}'.format(r=self.response.json(), code=self.response.status_code))

    def verify_response(self, _status_code, _status_message, _tc_desc):
        ''' verify json respone from  '''
        resp_json = self.response.json()
        bool_stat1, bool_stat2 = None, None
        if _status_code:
            if 'statusCode' in resp_json:
                bool_stat1, exp1, act1 = compare_values(_value1=str(_status_code), 
                    _value2=str(resp_json['statusCode']))
                info('{status}-{exp}-{act}'.format(status=bool_stat1,
                                                            exp=exp1,
                                                            act=act1))
        if _status_message:
            if 'statusMessage' in resp_json:
                bool_stat2, exp2, act2 = compare_values(_value1=_status_message, 
                    _value2=resp_json['statusMessage'])
                info('{status}-{exp}-{act}'.format(status=bool_stat2,
                                                            exp=exp2,
                                                            act=act2))
        if False in (bool_stat1, bool_stat2):
            self.tc_status = 'Fail'
            error('TC Desc:{d}TC status:{s}'.format(s=self.tc_status,d=_tc_desc))
        else:
            self.tc_status = 'Pass'
            info('TC Desc:{d}TC status:{s}'.format(s=self.tc_status,d=_tc_desc))


    def testAPI(self, _data_json=None, _exp_statusCode=None, _exp_statusMessage=None):

        self.tc_data = _data_json
        self.tc_desc = self.tc_data['desc']
        self.tc_post_data = self.tc_data['post_data']
        info('TestCae Desc: {desc}'.format(desc=self.tc_desc))
        self.invoke_api(_data_json=self.tc_post_data)
        if self.response.status_code in ( 200, 400):
            self.verify_response(_status_code=_exp_statusCode, 
            _status_message=_exp_statusMessage, 
            _tc_desc=self.tc_desc)
        print('API call done...')

