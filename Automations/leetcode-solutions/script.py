import requests
import os
import time
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import openai

# === Configuration ===
SAVE_DIR = "Leetcode"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# === Problem Numbers to Process ===
PROBLEM_NUMBERS = [118,136,191,773,509,2109,3396,2290,2924,268,1550,3342,1455,2554,215,2900,258,852,1760,75,24,21,2097,1975,2257,169,2825,100]

# === Helper Functions ===
def get_slug_title_difficulty(problem_number):
    metadata = requests.get("https://leetcode.com/api/problems/all/").json()
    for question in metadata['stat_status_pairs']:
        if question['stat']['frontend_question_id'] == problem_number:
            slug = question['stat']['question__title_slug']
            title = question['stat']['question__title']
            difficulty_level = question['difficulty']['level']
            difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
            difficulty = difficulty_map.get(difficulty_level, "Unknown")
            return slug, title, difficulty
    return None, None, None

def get_cpp_snippet(slug):
    graphql_url = "https://leetcode.com/graphql"
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            content
            codeSnippets {
                lang
                code
            }
        }
    }
    """
    response = requests.post(graphql_url, json={
        "query": query,
        "variables": {"titleSlug": slug}
    })

    data = response.json()
    question_data = data.get("data", {}).get("question", None)
    if not question_data:
        print("❌ Could not fetch question data (possibly premium):", slug)
        return None, None

    snippets = question_data.get("codeSnippets", [])
    if not snippets:
        print("❌ No code snippets found for:", slug)
        return None, None

    cpp_snippet = next((s['code'] for s in snippets if s['lang'] == 'C++'), None)
    if not cpp_snippet:
        print(f"❌ No C++ snippet found for problem: {slug}")
        return None, None

    content = question_data.get("content", "")
    return cpp_snippet, content

def generate_cpp_solution_with_openai(problem_number, problem_title, snippet):
    prompt = (
        f"Problem #{problem_number}: {problem_title}\n"
        f"Below is a C++ code snippet. Complete it to form a full solution.\n"
        f"Only respond with the final C++ code, no explanations or comments.\n\n"
        f"{snippet}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000,
        )
        code = response["choices"][0]["message"]["content"].strip()

        # Remove markdown markers if present
        if code.startswith("```cpp") or code.startswith("```c++"):
            code = code.split('\n', 1)[1]
        if code.endswith("```"):
            code = code.rsplit("```", 1)[0]

        return code.strip()
    except Exception as e:
        print("❌ OpenAI API error:", e)
        return "// OpenAI API error."

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in "-_ " else "" for c in name).replace(" ", "")

def save_solution(problem_number, problem_title, solution_code, difficulty):
    sanitized_title = sanitize_filename(problem_title)
    file_name = f"{problem_number}-{sanitized_title}.cpp"
    dir_path = Path(SAVE_DIR) / difficulty
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"// Problem {problem_number}: {problem_title}\n")
        f.write(f"// https://leetcode.com/problems/{sanitized_title.lower()}/\n\n")
        f.write(solution_code)
    print(f"✅ Saved solution to {file_path}")

# === Main Flow ===
def main():
    for i, problem_number in enumerate(PROBLEM_NUMBERS):
        print(f"\n🚀 Processing Problem #{problem_number} ({i + 1}/{len(PROBLEM_NUMBERS)})")

        slug, title, difficulty = get_slug_title_difficulty(problem_number)
        if not slug:
            print("❌ Problem number not found.")
            continue

        snippet, content = get_cpp_snippet(slug)
        if not snippet or not content:
            print("⚠️ Skipping due to missing snippet or content (possibly premium).")
            continue

        ai_solution = generate_cpp_solution_with_openai(problem_number, title, snippet)
        if not ai_solution.strip() or ai_solution.startswith("// OpenAI API error"):
            print("⚠️ Skipping due to empty or invalid AI response.")
            continue

        save_solution(problem_number, title, ai_solution, difficulty)

        if i < len(PROBLEM_NUMBERS) - 1:
            print("⏳ Waiting 10 seconds before next problem...")
            time.sleep(10)

if __name__ == "__main__":
    main()
