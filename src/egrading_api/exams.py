import requests

class ExamsMixin:
    def listExams(self) -> dict:
        url: str = f"https://egrading.ensam-umi.ac.ma/api/student/exam"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https://egrading.ensam-umi.ac.ma/student/exams',
            'Authorization': f'Bearer {self.accessToken}',
        }
        cookies: dict = {
            'refreshToken': self.refreshToken
        }
        response = requests.get(url, headers=headers, cookies=cookies, verify=False)
        response.raise_for_status()
        return response.json()
    
    def getExamData(self, exam_id: str) -> dict:
        url: str = f"https://egrading.ensam-umi.ac.ma/api/student/exam/{exam_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https://egrading.ensam-umi.ac.ma/student/exam/{exam_id}',
            'Authorization': f'Bearer {self.accessToken}',
        }
        cookies: dict = {
            'refreshToken': self.refreshToken
        }
        response = requests.get(url, headers=headers, cookies=cookies, verify=False)
        response.raise_for_status()
        return response.json()
