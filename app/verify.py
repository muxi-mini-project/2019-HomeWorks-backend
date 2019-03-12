import requests

def verify_siteId(siteId, userId):
    url = 'http://spoc.ccnu.edu.cn/studentHomepage/getMySite'
    payload = {
            'userId': userId,
            'termCode': '201901',
            'pageNum': 1,
            'pageSize': 30,
            }
    r = requests.post(url, json=payload)
    total = r.json().get('data').get('total')
    data = r.json().get('data').get('list')
    for i in range(total):
        aim_siteId = data[i].get('siteId')
        if siteId == aim_siteId:
            return True
    return False
