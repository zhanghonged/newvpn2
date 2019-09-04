token校验
====

Django1.11.18框架

# 功能列表
## andoid app
1. 用户第一次请求`client/init`接口，初始化用户存储数据库，生成token并返回。
2. 用户非第一次请求`client/init`，更新用户请求次数，更新token并返回。
3. 装饰器实现token验证，除`client/init`外一律校验token。
4. 请求必须在header携带token，并携带aid参数进行校验（GET、POST均支持）。

## event app
1. 将用户发过来的jsonn时间存入ElasticSearch引擎。