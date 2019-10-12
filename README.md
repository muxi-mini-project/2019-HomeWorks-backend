# HomeWorks

HomeWorks：

一个Android APP

提供华师云课堂作业查看，以及自定义邮件提醒服务

该仓库代码提供的功能：

+ 后端 API 服务
+ 邮件定时发送服务

## 创建数据库

```python
>> from app import db
>> db.create_all()
```

## 设置环境变量

```shell
export MAIL_USERNAME =
export MAIL_PASSWORD =
```

## 本地测试

### HomeWorks API 服务

```shell
flask run
# ./manage.py
```

### 邮件定时提醒 celery 服务

```shell
celery -A celery_run worker -B
```

## 服务器端运行

```shell
./run.sh
```
