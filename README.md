# 🎓 Egrading API Wrapper

A lightweight **Python wrapper** for the **ENSAM Egrading platform**.
It handles **authentication, exam listing, exam data retrieval**, and even **automatic MCQ solving using ChatGPT**.

Built for students who like their grades served with an API. 🚀

---

## ✨ Features

* ✅ Secure login using ENSAM credentials
* 📋 Fetch all available exams
* 📄 Get detailed data for a specific exam
* 🤖 Auto-solve MCQs using ChatGPT
* 🧠 Supports **single & multiple correct answers**
* 🍪 Automatic handling of **access & refresh tokens**
* ⚡ Fast, lightweight, and hackable

---

## 📦 Installation

> If you plan to publish it as a package:

```bash
pip install egrading-api
```

> Or clone directly:

```bash
git clone https://github.com/NacreousDawn596/egrading-api.git
cd egrading-api
pip install -r requirements.txt
```

---

## 🛠 Requirements

```bash
pip install requests urllib3 g4f
```

---

## 🚀 Quick Start

```python
from egrading_api import Student

# Initialize client
student = Student("email@ensam.ac.ma", "password")
```

✅ This automatically:

* Logs you in
* Stores `accessToken`
* Stores `refreshToken`
* Prepares the ChatGPT client

---

## 📋 List All Available Exams

```python
exams = student.listExams()
print(exams)
```

🔍 Returns:

* Exam IDs
* Subjects
* Status
* Time windows
* Metadata used to launch exams

---

## 📄 Get Full Exam Data

```python
exam_id = "123456"
exam_data = student.getExamData(exam_id)

print(exam_data)
```

✅ Includes:

* Questions
* Choices
* Exam duration
* Scoring details
* Exam configuration

---

## 🤖 Auto-Solve MCQs using ChatGPT

Once you extract the questions from the exam:

```python
questions = exam_data["questions"]

answers = student.answerQuestionsUsingChatGPT(questions)
print(answers)
```

### ✅ Output Format

```python
{
  "Q1": [2],
  "Q2": [1, 3],
  "Q3": [4]
}
```

* 🟢 Always returns **lists**
* 🟢 Supports **multiple correct answers**
* 🟢 Indexes are **1-based**

---

## 🧠 How the AI Solving Works

* Questions are split into smart chunks
* Each chunk is sent to ChatGPT
* The model is forced to return:

  * ✅ A **raw Python dictionary**
  * ✅ No markdown
  * ✅ No explanations
* Output is:

  * Parsed
  * Normalized
  * Merged into a clean final result

---

## 🔐 Authentication System

The wrapper handles:

* ✅ Access token stored in headers
* ✅ Refresh token stored in cookies
* ✅ Automatic session reuse
* ✅ No manual token handling needed

---

## ⚙️ Class Overview

### `Student(email, password, login=True)`

| Parameter  | Type   | Description        |
| ---------- | ------ | ------------------ |
| `email`    | `str`  | ENSAM email        |
| `password` | `str`  | Account password   |
| `login`    | `bool` | Auto-login on init |

---

### `listExams() → dict`

Returns all exams available to the student.

---

### `getExamData(exam_id: str) → dict`

Returns full structured exam data.

---

### `answerQuestionsUsingChatGPT(questions: list, model="gpt-4") → dict`

Auto-answers all MCQs using AI.

---

## ⚠️ Security Notes

* ❗ This project disables SSL verification (`verify=False`)
* ❗ Credentials are sent in plain requests
* ✅ Use **only for educational & personal testing**
* ✅ Never expose your password in public repos

---

## 🧪 Example Full Workflow

```python
student = Student("email@ensam.ac.ma", "password")

exams = student.listExams()
first_exam_id = exams[0]["id"]

exam_data = student.getExamData(first_exam_id)

answers = student.answerQuestionsUsingChatGPT(exam_data["questions"])

print(answers)
```

---

## 🛑 Disclaimer

This project is:

* ❌ Not affiliated with ENSAM
* ❌ Not officially supported
* ✅ Only for **educational & research purposes**

Use responsibly. Don’t speedrun your academic career into chaos 💀

---

## ❤️ Author

Made with caffeine, insomnia, and bad life choices by **Kamal** ☕
If this saved you during exam week == you owe me monster hhhhhhhh.

---