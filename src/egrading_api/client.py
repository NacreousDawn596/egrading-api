import requests
import urllib3
import re
import ast
from g4f.client import Client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Student:
    def __init__(self, email: str, password: str, login=True) -> None:
        self.email = email
        self.password = password
        self.gpt_client = Client()
        if login:
            data, cookies = self.login_data("https://egrading.ensam-umi.ac.ma/api/auth/login")
            print(data)
            self.accessToken = data.json()['accessToken']
            self.refreshToken = cookies['refreshToken']
        
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
    
    def listExams(self, exam_id: str) -> dict:
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

    def answerQuestionsUsingChatGPT(self, questions: list, model: str = "gpt-4") -> dict:
        def chunked(lst, n):
            n = max(1, n)
            k, m = divmod(len(lst), n)
            return [
                lst[i*(k+1) if i < m else i*k + m : (i+1)*(k+1) if i < m else (i+1)*k + m]
                for i in range(n)
                if lst[i*(k+1) if i < m else i*k + m : (i+1)*(k+1) if i < m else (i+1)*k + m]
            ]

        # ✅ Dynamic chunking
        n_chunks = 2 if len(questions) > 2 else 1
        chunks = chunked(questions, n_chunks)

        all_answers = []

        for chunk in chunks:
            prompt = (
                "You are given a list of MCQ questions. "
                "Some questions may have MULTIPLE correct answers. "
                "For each question, return ONLY a Python dict mapping question numbers "
                "(Q1, Q2, ...) to a LIST of 1-based indices of the correct answers. "
                "If only one answer is correct, still return it as a list. "
                "DO NOT wrap the output in markdown or code blocks. "
                "Output ONLY the raw dict.\n\n"
            )

            for i, q in enumerate(chunk, 1):
                prompt += (
                    f"Q{i}:\n{q['description']}\n"
                    "Choices:\n" +
                    "\n".join([f"{j+1}. {choice}" for j, choice in enumerate(q['choices'])]) +
                    "\n\n"
                )

            response = self.gpt_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                web_search=False
            )

            content = response.choices[0].message.content.strip()

            # ✅ STRIP ```python ... ``` SAFELY
            content = re.sub(r"^```(?:python)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)

            try:
                parsed = ast.literal_eval(content)

                if isinstance(parsed, dict):
                    normalized = {}
                    for k, v in parsed.items():
                        if isinstance(v, list):
                            normalized[k] = v
                        else:
                            normalized[k] = [v]  # ✅ force list

                    all_answers.append(normalized)

            except Exception as e:
                print("Invalid model output, skipped:", content)
                print("Error:", e)

        # ✅ GLOBAL RE-INDEXING → Q1 ... Q10 ... Qn (NO REPEATS)
        merged = {}
        idx = 1

        for d in all_answers:
            for k in sorted(d.keys(), key=lambda x: int(x[1:])):
                merged[f"Q{idx}"] = d[k]
                idx += 1

        return merged
