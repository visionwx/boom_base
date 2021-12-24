import json
import traceback
class BoomConfig:
    _instance = None
    
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
