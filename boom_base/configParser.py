import json
import traceback
import typing

class BoomConfig:
    _instance = None
    config = None
    def __new__(cls, configPath: str) -> object:
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                with open(configPath, 'r', encoding='utf-8') as f:
                    configContent = f.read()
                    cls.config = json.loads(configContent)
            except:
                raise Exception(f"BoomConfig load failed: {traceback.format_exc()}")
        return cls._instance
    @classmethod
    def get(cls):
        if cls.config is None:
            raise Exception("BoomConfig not init")
        return cls.config
    @classmethod
    def getVersion(cls):
        if cls.config is None:
            raise Exception("BoomConfig not init")
        return cls.config.get("version")
    @classmethod
    def getName(cls):
        if cls.config is None:
            raise Exception("BoomConfig not init")
        return cls.config.get("name")
    @classmethod
    def getApiDomain(cls):
        if cls.config is None:
            raise Exception("BoomConfig not init")
        return cls.config.get("api_domain")
    @classmethod
    def getIsProduction(cls):
        if cls.config is None:
            raise Exception("BoomConfig not init")
        return cls.config.get("is_production", False)
    @classmethod
    def getEnableCORS(cls):
        if cls.config is None:
            raise Exception("BoomConfig not init")
        return cls.config.get("enable_cors", False)
    @classmethod
    def getRemoteConfig(cls):
        if cls.config is None:
            raise Exception("BoomConfig not init")
        return cls.config.get("remote_config", False) 

class RelationDatabaseType:
    MONGO = "mongodb"
    MYSQL = "mysql"

class CoreServiceNames:
    authentication = "authentication"
    media = "media"
    video = "video"
    document = "document"
    team = "team"
    task = "task"
    payment = "payment"
    subscription = "subscription"
    mgmt = "mgmt"

class ConfigBase:
    KEY = None
    _main_instance = None
    MAIN_INSTANCE = "main"

    @classmethod
    def fromDict(cls, data, **kwargs) -> object:
        return cls

    @classmethod
    def _fromConfig(cls, instance_name, **kwargs) -> object:
        if instance_name is None:
            raise Exception("instance name not provide")
        # 获取配置
        data = BoomConfig.get()
        data = data.get(cls.KEY, {}).get(instance_name,{})
        config = cls.fromDict(data, **kwargs)
        return config
    
    @classmethod
    def fromConfig(cls, **kwargs) -> object:
        # 是否已经初始化过
        if cls._main_instance is None:
            # 获取配置
            cls._main_instance = cls._fromConfig(cls.MAIN_INSTANCE, **kwargs)
        return cls._main_instance

class RelationDatabaseConfig(ConfigBase):
    """
        "type": "mongodb",
        "host": "172.18.74.220",
        "port": 3717,
        "username": "lms",
        "password": "lms123456",
        "auth": false,
        "db": "lms"
    """
    
    KEY = "relational_database"

    def __init__(self, _type, host, port, 
        username, password, 
        auth, db):
        self._type = _type
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth = auth
        self.db = db

    @classmethod
    def fromDict(cls, data) -> object:
        if data is None or data == {}:
            raise Exception("relation database config data none")
        return cls(
            _type = data.get("type", None),
            host = data.get("host", None),
            port = data.get("port", None),
            username = data.get("username", None),
            password = data.get("password", None),
            auth = data.get("auth", None),
            db = data.get("db", None),
        )

class SubscriptionRelationDatabaseConfig(RelationDatabaseConfig):

    _subscription_instance = None
    SUBSCRIPTION_INSTANCE = "subscription"
    
    @classmethod
    def fromConfig(cls) -> object:
        # 是否已经初始化过
        if cls._subscription_instance is None:
            # 获取配置
            cls._subscription_instance = cls._fromConfig(cls.SUBSCRIPTION_INSTANCE)
        return cls._subscription_instance

class KvStoreConfig(ConfigBase):
    """
        "kv_store": {
            "main": {
                "type": "redis",
                "host": "172.18.74.220",
                "port": 8379,
                "password": "",
                "auth": false,
                "db": 0
            }
        }
    """
    KEY = "kv_store"
    def __init__(self, _type, host, port, 
        username, password, 
        auth, db):
        self._type = _type
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth = auth
        self.db = db

    @classmethod
    def fromDict(cls, data) -> object:
        if data is None or data == {}:
            raise Exception("kv store config data none")
        return cls(
            _type = data.get("type", None),
            host = data.get("host", None),
            port = data.get("port", None),
            username = data.get("username", None),
            password = data.get("password", None),
            auth = data.get("auth", None),
            db = data.get("db", None),
        )

class ServiceConfig(ConfigBase):
    KEY = "core_services"
    def __init__(self, name, port, image, path, logDict, analysisDict):
        self.name = name
        self.port = port
        self.image = image
        self.path = path
        self.log:FileRotateConfig = FileRotateConfig.fromDict(logDict)
        self.analysis:FileRotateConfig = FileRotateConfig.fromDict(logDict)

    @classmethod
    def fromDict(cls, data, requiredLog = True, requiredAnalysis = True):
        if data is None or data == {}:
            raise Exception("service config data none")
        if data.get("log", {}) == {} and requiredLog:
            raise Exception("log config is required")
        if data.get("analysis", {}) == {} and requiredAnalysis:
            raise Exception("analysis config is required")
        return cls(
            name = data.get("name", None),
            port = data.get("port", None),
            image = data.get("image", None),
            path = data.get("path", None),
            logDict = data.get("log", {}),
            analysisDict = data.get("analysis", {}),
        )

class MgmtServiceConfig(ServiceConfig):
    _mgmt_instance = None
    MGMT_INSTANCE = "mgmt"
    
    @classmethod
    def fromConfig(cls, requiredLog = True, requiredAnalysis = True) -> object:
        # 是否已经初始化过
        if cls._mgmt_instance is None:
            # 获取配置
            cls._mgmt_instance = cls._fromConfig(cls.MGMT_INSTANCE, **{
                "requiredLog": requiredLog,
                "requiredAnalysis": requiredAnalysis
            })
        return cls._mgmt_instance

class AuthenticationServiceConfig(ServiceConfig):
    _auth_instance = None
    AUTH_INSTANCE = "authentication"
    
    @classmethod
    def fromConfig(cls) -> object:
        # 是否已经初始化过
        if cls._auth_instance is None:
            # 获取配置
            cls._auth_instance = cls._fromConfig(cls.AUTH_INSTANCE)
        return cls._auth_instance

class FileRotateConfig:

    def __init__(self, path, file, fileSize, fileCounts):
        self.path = path
        self.file = file
        self.fileSize = fileSize
        self.fileCounts = fileCounts

    @classmethod
    def fromDict(cls, data):
        return cls(
            path = data.get("path", None),
            file = data.get("file", None),
            fileSize = data.get("file_size", None),
            fileCounts = data.get("file_counts", None),
        )

class ObjectStorageConfig(ConfigBase):
    """
      "type": "oss",
      "bucket": "boom-upload-test",
      "region": "cn-shenzhen",
      "domain": "ossupload.tf.visionwx.com",
      "enable_cdn": true,
      "enable_static": true,
      "credentials": {
        "access_key_id": "XXXX",
        "access_key_secret": "XXXX",
        "access_role": "XXXX"
      }
    """
    KEY = "object_storage"
    def __init__(self, _type, bucket, region, 
        domain, enable_cdn, 
        enable_static, credentials):
        self._type = _type
        self.bucket = bucket
        self.region = region
        self.domain = domain
        self.enable_cdn = enable_cdn
        self.enable_static = enable_static
        self.credentials = credentials

    @classmethod
    def fromDict(cls, data) -> object:
        if data is None or data == {}:
            raise Exception("object storage config data none")
        return cls(
            _type = data.get("type", None),
            bucket = data.get("bucket", None),
            region = data.get("region", None),
            domain = data.get("domain", None),
            enable_cdn = data.get("enable_cdn", None),
            enable_static = data.get("enable_static", None),
            credentials = data.get("credentials", None),
        )

class UploadObjectStorageConfig(ObjectStorageConfig):

    _upload_instance = None
    UPLOAD_INSTANCE = "upload"
    
    @classmethod
    def fromConfig(cls) -> object:
        # 是否已经初始化过
        if cls._upload_instance is None:
            # 获取配置
            cls._upload_instance = cls._fromConfig(cls.UPLOAD_INSTANCE)
        return cls._upload_instance

class DownloadObjectStorageConfig(ObjectStorageConfig):

    _download_instance = None
    DOWNLOAD_INSTANCE = "download"
    
    @classmethod
    def fromConfig(cls) -> object:
        # 是否已经初始化过
        if cls._download_instance is None:
            # 获取配置
            cls._download_instance = cls._fromConfig(cls.DOWNLOAD_INSTANCE)
        return cls._download_instance