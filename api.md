# API文档

## 登录
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/login/ |POST  |  None  |

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
    'msg': String,          //登录结果信息
    'cookie':String,
    'token': String,
    'userName': String,     //用户学号
    'realName': String,     //用户姓名
}
```

### Status Code
```
200 成功
400 参数不全
401 用户名或密码错误
```

## 获取课堂列表
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/course/list/ |GET  |  cookie, token  |

### Post Data
None

### Return Data
```
{
    "msg": String,
    "cookie": String,
    "total": Int,
    "courseList": [
            {
                "courseName": String,
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
|/api/course/{siteId: string}/assignment/list/ |GET  |  cookie, token  |

### Post Data
None

### Return Data
```
{
    "msg": String,
    "cookie": String,
    "siteId": String,
    "total": Int,
    "data": [
        {
            "status": Int,      //未提交：0，待批阅：1，已驳回：2，已批阅：3
            "assignName": Int,
            "beginTime": Int,
            "endTime": String,
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
|/api/assignment/{siteId: string}/{assignId: string}/info/ |GET |  cookie, token  |

### Post Data
None
### Return Data
```
{
    "msg": String,
    "cookie": String,
    "siteId": String,
    "assignId": String,
    "courseName": String,                //课堂（科目）名
    "assignName": String,               //任务（作业）名
    "status": Int,                      //未提交：0，待批阅：1，已驳回：2，已批阅：3
    "beginTime": Int,
    "endTime": Int,
    "content": String,                  //作业要求，颁布的作业
    "pointNum": Int,                    //已批阅数
    "commitNum": Int,                   //已提交数
    "isGroup": Int,                     //分组作业：1，个人作业：0
    "groupNum": Int,                    //小组数
    "studentNum": Int,                  //学生数
    "groupPoint": Int,                  //小组得分
    "personalPoint": Int,               //个人得分
    "feedback": String,                 //作业反馈
    "assignAttachmentNum": Int,         //作业要求的附件数
    "assignAttachment": [
                {
                    "id": String,
                    "name": String,
                    "ext": String,      //附件格式
                    'sourceUrl': string //资源地址
                }
    ],
    "submitAttachmentNum": Int,         //提交的附件数
    "submitAttachment": [
              {
                    "id": String,
                    "name": String,
                    "ext": String,
                    "uploadTime": Int,
                    "sourceUrl": string //资源地址
              }
    ],
    "submitContent": String,            //作业内容，提交的作业
}
```
### Status Code
```
200 成功
400 参数不全
401 身份认证错误
404 未找到
```

## 获取任务列表
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/assignment/list/ |GET  |  cookie, token  |

### Post Data
None
### Return Data
```
{
    "msg": String,
    "cookie": String,
    "total": Int,
    "assignList": [
        {
            "siteId": String,
            "status": Int,
            "courseName": String,
            "assignName": String,
            "teacher": String,
            "beginTime": Int,
            "endTime": Int,
            "assignId": String,
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

## 个人信息
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/userInfo/ |GET  |  token  |

### Post Data
None

### Return Data
```
{
    "msg": String,
    "realName": String,     //姓名
    "userName": String,     //学号
    "email": String,
}
```
### Status Code
```
200 成功
400 参数不全
401 身份认证错误
```

## 弹窗提醒&获取未提交任务
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/notice/getAssignments/ | GET  |  cookie, token  |

### Post Data
None

### Return Data
```
{
    "msg": String,
    "cookie": String,
    "realName": String,
    "userName": String,
    "total": Int,           //未提交总数
    "data": [
        {
            "courseName": String,
            "assignName": String,
            "teacher": String,
            "siteId": String,
            "assignId": String,
            "beginTime": Int,
            "endTime": Int,
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

## 搜索
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/search/ |GET  |  cookie, token  |
### URL Params
```
keyword: String
```
### Post Data
None
### Return Data
```
{
    "msg": String,
    "cookie": String,
    "total": Int,
    "courseData": [                 #课程名中含有关键字
        {
            "courseName": String,
            "siteId": String,
        }
    ],
    "assignData": [                 #作业名中含有关键字
        {
            "assignId": String,
            "siteId": String,
            "assignName": String,
            "courseName": String,
        }
    ],
    "contentData": [                #作业内容中含有关键字
        {
            "assignId": String,
            "siteId": String,
            "assignName": String,
            "courseName": String,
        }
    ]
}
```
### Status Code
```
200 成功
400 请求参数不全
401 身份认证错误
404 未找到
```

## 修改邮箱
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/modify/ |PUT  |  token，verifyCodeToken  |
### Post Data
```
{
    "email": String,
    "verifyCode": int
}
```
### Return Data
```
{
    "msg": String
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
```
## 发送邮箱验证码
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/modify/sendVerifyCode/ |POST  |  token  |
### Post Data
```
{
    "email": String,
}
```
### Return Data
```
{
    "msg": String,
    "verifyCodeToken": String
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
404 用户不存在
```

## 邮件提醒启用状态更改
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/isSend/modify/ |POST  |  token  |
### Post Data
None

### Return Data
```
{
    "msg": String,
    "isSend": Boolean
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
404 用户不存在
```

## 添加时间节点
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/noticeTime/add/ |POST  |  token  |
### Post Data
```
{
    "noticeTime": int,
}
```

### Return Data
```
{
    "msg": String,
    "noticeTimeId": String,
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
404 用户不存在
```

## 获取全部时间节点及邮箱通知设置
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/noticeConfig/get/ |GET  |  token  |
### Post Data
None

### Return Data
```
{
    "msg": String,
    "isSend": Boolean,              //true为开启
    "noticeTimeList": [{
        "noticeTime": Int,
        "noticeTimeId": String,
        "noticeTimeStatus": Int,    //开启：1，关闭：0
        },
    ]
    "total": Int,
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
404 未找到
```

## 修改时间节点
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/noticeTime/{noticeTimeId: String}/modify/ | PUT  | token  |
### Post Data
```
{
    "noticeTime": Int,
}
```

### Return Data
```
{
    "msg": String,
    "noticeTimeId": String,
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
404 未找到
```
## 改变时间节点启用状态
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/noticeTime/{noticeTimeId: String}/changeStatus/ | PUT  | token  |
### Post data
None

### Return Data
```
{
    "msg": String,
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
404 未找到
```
## 移除时间节点
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/mail/noticeTime/delete/ | DELETE  | token  |
### Post Data
```
{
    "noticeTimeId": String
}
```
### Return Data
```
{
    "msg": String,
    "statusMessage": String
}
```
### Status Code
```
200 成功
400 请求错误
401 身份认证错误
404 未找到
```

## <center> 名词规范表 </center>
|关键字|表意|
|:---:|:---:|
| userName | 学号/登录账号  |
| password | 密码  |
| realName  | 姓名  |
| userId  | 用户Id  |
| course  | 课堂    |
| courseNme | 课堂名  |
| siteId  | 课堂站点ID  |
| assignName | 任务名   |
| assignId  | 任务ID    |