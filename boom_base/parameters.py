import os

# 获取环境变量
def getEnvPara(parameterName, default=None, 
    raiseExceptionIfNone=True):
    parameterValue = os.environ.get(parameterName, default)
    if parameterValue is None and raiseExceptionIfNone:
        raise Exception(parameterName + " not defined")
    return parameterValue

# 从环境变量 获取服务配置
def getServiceParaFromEnv():
    return {
        "debug": False,
        "isProduction": False if getEnvPara('is_production') == "false" else True,
        "service": {
            "name": getEnvPara('service_name', "BoomServer"),
            "logPath": getEnvPara('service_log_path', "/var/log/boom.log"),
        },
    }

# 从环境变量获取 mongo 配置参数
#   mongo_host: mongo主机地址
#   mongo_port: 端口号
#   mongo_db:   数据库
#   mongo_auth: 是否开启认证
#   mongo_username: 认证用户名
#   mongo_password: 认证用户密码
def getMongoParaFromEnv():
    return {
        "host":  getEnvPara('mongo_host'),
        "port": int(getEnvPara('mongo_port')),
        "db": getEnvPara('mongo_db'),
        "auth": False if getEnvPara('mongo_auth') == "false" else True,
        "username": getEnvPara('mongo_username'),
        "password": getEnvPara('mongo_password')
    }

# 从环境变量获取 celery 配置参数
#   celery_result_backend: 'redis://boom-redis:6379/5'
#   broker_url: 'redis://boom-redis:6379/6'
def getCeleryParaFromEnv():
    return {
        "resultBackend": getEnvPara('celery_result_backend'),
        "brokerUrl": getEnvPara('celery_broker_url')
    }

# 从环境变量获取 日志 配置参数
def getLogParaFromEnv():
    return {
        "logFilePath": getEnvPara('log_file_path',
            raiseExceptionIfNone=False),
        "logToConsole": getEnvPara('log_to_console', default=True,
            raiseExceptionIfNone=False),
        "backCounts": getEnvPara('back_counts', default=1024*1024,
            raiseExceptionIfNone=False),
        "maxBytes": getEnvPara('max_bytes', default=5,
            raiseExceptionIfNone=False),
    }

# 从环境变量获取redis配置参数
def getRedisParaFromEnv():
    return {
        "host":  getEnvPara('redis_host'),
        "port": int(getEnvPara('redis_port', default=6379)),
        "db": int(getEnvPara('redis_db', default=0)),
        "password": getEnvPara('redis_password', default=None, raiseExceptionIfNone=False),
        "decode_responses": getEnvPara('redis_decode_responses', default=True),
    }