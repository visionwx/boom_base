## Boom Base


## Brief
- 异常基类
- mongodb数据库操作实例
- 日志实例
- 数据模型基类，Collection

## Usage
```
pip install git+https://oauth2:p_xB46CAsVJFz8PsDrpk@gitlab.com/visionwx/boom_base.git

python
from boom_base import *
```

## Change
#### 2021-05-26
- 【优化】modelView 增加traceBack

#### 2021-05-22
- 【修复】modelView修复list获取参数异常bug

#### 2021-05-20
- 【新增】flask新增view基类，auth增加验证token装饰函数
- 【新增】flask/view新增 ResponseResult类
- 【优化】flask/view优化list函数
- 【优化】flask/view优化list函数，增加aggregation功能

#### 2021-04-08
- 【新增】SendSmsCodeFailedException
- 【新增】新增 PhoneCodeVerifyFailedException
- 【新增】增加flask模块
- 【修复】parameters.getEnvPara 参数default拼写错误
- 【优化】增加api_calls 日志
- 【新增】增加api_calls apiCallRecord装饰器

#### 2021-04-07
- 【新增】增加api_calls
- 【新增】增加redisdb