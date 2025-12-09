import re
import ast

class AIMixin:
    def answerQuestionsUsingChatGPT(self, questions: list, model: str = "gpt-4") -> dict:
        def chunked(lst, n):
            n = max(1, n)
            k, m = divmod(len(lst), n)
            return [
                lst[i*(k+1) if i < m else i*k + m : (i+1)*(k+1) if i < m else (i+1)*k + m]
                for i in range(n)
                if lst[i*(k+1) if i < m else i*k + m : (i+1)*(k+1) if i < m else (i+1)*k + m]
            ]

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
                            normalized[k] = [v]  

                    all_answers.append(normalized)

            except Exception as e:
                print("Invalid model output, skipped:", content)
                print("Error:", e)

        merged = {}
        idx = 1

        for d in all_answers:
            for k in sorted(d.keys(), key=lambda x: int(x[1:])):
                merged[f"Q{idx}"] = d[k]
                idx += 1

        return merged
