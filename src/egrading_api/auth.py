import requests

class AuthMixin:
    def login_data(self, url: str) -> tuple:
        payload: dict = {
            'email': self.email,
            'password': self.password
        }
        
        headers: dict = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Referer': 'https://egrading.ensam-umi.ac.ma/auth/login',
            'Origin': 'https://egrading.ensam-umi.ac.ma'
        }
        
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return response, response.cookies.get_dict()
