## Boom Base


## Brief
- 异常基类
- mongodb数据库操作实例
- 日志实例
- 数据模型基类，Collection

## Usage
```
pip3 install git+https://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@github.com/visionwx/boom_base.git@v0.1.48

python
from boom_base import *
```

## Change
#### 2021-07-21
- 【新增】model/base.py view.py 增加get参数 _before_
- 【优化】删除logger

#### 2021-07-16
- 【优化】model/base.py view.py 优化

#### 2021-07-15
- 【优化】model/base.py 优化aggregate接口 limit逻辑

#### 2021-07-10
- 【优化】view.py create 接口exception处理

#### 2021-07-07
- 【新增】view.py list接口新增_sort_参数，-1降序，1升序。修复 limit 参数类型错误bug

#### 2021-07-06
- 【新增】新增 dataModel
- 【优化】调整 view.py _type_,_after_,_limit_参数格式
- 【优化】更新版本
- 【优化】优化view.py get和list接口

#### 2021-07-03
- 【新增】flask/auth.py 新增 verifyUserToken装饰函数
- 【新增】flask/request_parser.py 新增 verifyPara参数
- 【新增】model/base.py 新增CollectionUpdateType, 以及新增exception
- 【新增】exception.py 新增share相关的exception
- 【修复】verifyUserToken bug 修复

#### 2021-06-08
- 【新增】model/base.py update_v2接口新增，支持inc/push/addToSet等高级更新；flask.view update接口同步更新

#### 2021-06-05
- 【修复】model/base.py aggregateGet接口 bug 修复
- 【优化】自定义exception全部实现__str__接口

#### 2021-06-04
- 【优化】flask/view.py modelView get接口增加高级查询功能
- 【修复】flask/view.py modelView get接口BUG修复

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