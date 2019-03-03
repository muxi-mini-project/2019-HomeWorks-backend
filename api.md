# API文档

## 登录
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/login/|POST  |  None  |

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
    'userInfo': {                       //用户信息，失败则无此关键字
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
|/api/class |POST  |  cookie(string)  |

### Post Data
```
{
    "userId": String
}
```

### Return Data
```
{
    'cookie': String
    'sum': Int
    'classList': [
            {
                "className": String,
                "assign": Int,
                "teacher": String
            },{
                ...
            }, ...
    ]
}
```
### Status Code
```
200 成功
```

## 获取任务列表
|URL        |Method|header|
|:--:       |:--:  |:--:  |
|/api/assignment|POST  |  cookie(string)  |

### Post Data
```
{
    'userId': string
}
```
### Return Data
```
{
    'cookie': String,
    'assignList': ...
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
