"""
NocoBase Token 获取工具
使用方法：修改下方账号密码，运行即可获取 Token
"""
import requests

NOCOBASE_URL = "http://localhost:13000"
ACCOUNT = "admin@nocobase.com"
PASSWORD = "your-password-here"  # 请修改为你的密码

def get_token():
    response = requests.post(
        f"{NOCOBASE_URL}/api/auth:signIn",
        json={"account": ACCOUNT, "password": PASSWORD}
    )
    if response.status_code == 200:
        token = response.json()["data"]["token"]
        print(f"Token 获取成功：")
        print(token)
        return token
    else:
        print(f"获取失败：{response.text}")
        return None

if __name__ == "__main__":
    get_token()