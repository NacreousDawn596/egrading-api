import urllib3
from g4f.client import Client
from .auth import AuthMixin
from .exams import ExamsMixin
from .ai import AIMixin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Student(AuthMixin, ExamsMixin, AIMixin):
    def __init__(self, email: str, password: str, login=True) -> None:
        self.email = email
        self.password = password
        self.gpt_client = Client()
        if login:
            data, cookies = self.login_data("https://egrading.ensam-umi.ac.ma/api/auth/login")
            print(data)
            self.accessToken = data.json()['accessToken']
            self.refreshToken = cookies['refreshToken']
