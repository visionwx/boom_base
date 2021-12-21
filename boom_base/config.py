import os


def get_aliyun_access_key_id():
    return os.environ.get('ALIYUN_ACCESS_KEY_ID')

def get_aliyun_access_key_secret():
    return os.environ.get('ALIYUN_ACCESS_KEY_SECRET')

def get_aliyun_mns_endpoint():
    return os.environ.get('ALIYUN_MNS_ENDPOINT')
