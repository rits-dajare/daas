# path config
DATA_FILE_PATH: str = './data/*.json'
CONFIG_FILE_ROOT_PATH: str = './config'
READING_DICT_FILE_PATH: str = CONFIG_FILE_ROOT_PATH + '/reading_dict.csv'
JUDGE_PASS_DICT_PATH: str = CONFIG_FILE_ROOT_PATH + '/judge_pass_dict.txt'
JUDGE_REJECT_DICT_PATH: str = CONFIG_FILE_ROOT_PATH + '/judge_reject_dict.txt'

# text config
TEXT_MAX_LENGTH: int = 30
TIGHT_LENGTH: int = 20
CACHE_SIZE: int = 128

# api config
API_SUCCESS_MSG: str = 'success'
API_RESPONSE: dict = {'message': API_SUCCESS_MSG}
API_HOST: str = '0.0.0.0'
API_PORT: int = 50000
API_DEBUG: bool = False
