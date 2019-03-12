# API文档

## 登录
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/login |POST  |  None  |

### POST Data
```
{
    "userName": String,    //登录账号（学号）
    "password": String,     //登录密码
}
```

### Return Data
```
{
    'code': int,        //成功:1，失败:0
    'msg': String,      //登录结果信息
    'cookie':String,
    'userInfo': {                       //用户信息
                'userName': String,     //用户学号
                'realName': String,     //用户姓名
                'userId': String,
                }
}
```

### Status Code
```
200 成功
401 用户名或密码错误
```

## 获取课堂
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/class/list |POST  |  cookie(string)  |

### Post Data
```
{
    "userId": String
}
```

### Return Data
```
{
    "code": Int,
    "msg": String,
    'cookie': String,
    "userId": String,
    'total': Int,
    'classList': [
            {
                "className": String,
                "teacher": String,
                "siteId": String,
            }
    ]
}
```
### Status Code
```
200 成功
400 参数不全
401 身份认证错误
```

## 获取某一课堂任务列表
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/class/assignment/ |POST  |  cookie(string)  |

### Post Data
```
{
    "userId": String,
    "siteId": String
}
```
### Return Data
```
{
    "code": Int,
    "msg": String,
    "cookie": String,
    "userId": String,
    "siteId": String,
    "total": Int,
    "data": [
        {
            "status": Int,      //未提交：0，待批阅：1，已驳回：2，已批阅：3
            "assignName": String,
            "beginTime": Int,
            "endTime": Int,
            "assignId": String,     //任务ID
        }
    ]
}
```
### Status Code
```
200 成功
400 参数不全
401 身份认证错误
404 未找到，参数错误
```

## 任务详情
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/assignment/info |POST  |  cookie(string)  |

### Post Data
```
{
    "userId": String,
    "siteId": String,
    "assignId": String
}
```
### Return Data
```
{
    "code": Int,
    "msg": String,
    "cookie": String,
    "userId": String,
    "siteId": String,
    "assignId": String,
    "className": String,        //课堂（科目）名
    "assignName": String,       //任务（作业）名
    "status": Int,              //未提交：0，待批阅：1，已驳回：2，已批阅：3
    "beginTime": Int,
    "endTime": Int,
    "content": String,          //作业要求，颁布的作业
    "pointNum": Int,            //已批阅数
    "isGroup": Int,             //分组作业：1，个人作业：0
    "groupNum": Int,            //小组数
    "studentNum": Int,          //学生数
    "groupPoint": Int,          //小组得分
    "personalPoint": Int,       //个人得分
    "feedback": String,         //作业反馈
    "assignAttachmentNum": Int,       //作业要求的附件数
    "assignAttachment": [
                {
                    "id": String,
                    "name": String,
                    "ext": String,      //附件格式
                }
    ]
    "submitAttachmentNum": Int,         //提交的附件数
    "submitAttachment": [
              {
                    "id": String,
                    "name": String,
                    "ext": String,
                    "uploadTime": String,
              }
    ]
    "submitContent": String,    //作业内容，提交的作业
}
```
### Status Code
```
200 成功
```

## 获取任务列表
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/assignment/list |POST  |  cookie(string)  |

### Post Data
```
{
    'userId': string
}
```
### Return Data
```
{
    "code": Int,
    "msg": String,
    'cookie': String,
    "userId": String,
    "total": Int,
    'assignList': [
        {
            "siteId": String,
            "status": Int,
            "className": String,
            "assignName": String,
            "teacher": String,
            "beginTime": String,
            "endTime": String,
            "assignId": String,
        }
    ]
}
```
### Status Code
```
200 成功
```

## 个人信息
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/userInfo|POST  |  cookie(string)  |

### Post Data
```
{
    'userId': String
}
```
### Return Data
```
{
    "code": Int,
    "msg": String,
    "cookie": String,
    "userId": String,
    'realName': String,     //姓名
    'userName': String,     //学号
    "apartment": String,    //院系
    "mail": String,
}
```
### Status Code
```
200 成功
```

## 未提交任务提醒
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/notice |POST  |  cookie(string)  |

### Post Data
```
{
    "userId": String,
}
```
### Return Data
```
{
    "code": Int,
    "msg": String,
    "cookie": String,
    "userId": String,
    "realName": String,
    "userName": String,
    "total": Int,           //未提交总数
    "data": [
        {
            "className": String,
            "assignName": String,
            "teacher": String,
            "siteId": String,
            "assignId": String,
            "beginTime": String,
            "endTime": String,
        }
    ]
}
```
### Status Code
```
200 成功
```

## 搜索
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/search |POST  |  cookie(string)  |
### URL Params
```
keyword: String
```
### Post Data
```
{
    "userId": String
}
```
### Return Data
```
{
    "code": Int,
    "msg": String,
    "cookie": String,
    "userId": String,
    "total": Int,
    "data": [
        {
            "assignId": String,
            "siteId": String,
            "assignName": String,
            "className": String,
            "status": Int,
            "beginTime": String,
            "endTime": String,
            "teacher": String,
        }
    ]
}
```
### Status Code
```
200 成功
```

## <center> 名词规范表 </center>
|关键字|表意|
|:---:|:---:|
| userName | 学号/登录账号  |
| password | 密码  |
| realName  | 姓名  |
| userId  | 用户Id  |
| classNme | 课堂名  |
| siteId  | 课堂站点ID  |
| assignName | 任务名   |
| assignId  | 任务ID    |

