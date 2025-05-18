# LeetCode Auto Submitter

Automate daily submission of your solved LeetCode problems from your GitHub solutions repository to maintain your streak — **without opening your laptop!**

---

## Features

- Picks a **random problem** from your stored solutions.
- Automatically logs in to LeetCode.
- Navigates to the problem page.
- Pastes your existing solution code.
- Submits the solution.
- Runs headlessly on **GitHub Actions** every day (or on demand).

---

## Prerequisites

- You need **two GitHub repositories**:
  1. `leetcode-automation` — contains this automation code.
  2. `leetcode-solutions` — your personal repo with solved LeetCode code files.

- Solutions in `leetcode-solutions` should be named with this format:
<problem_number>-<ProblemName>.cpp
Example: `199-BinaryTreeRightSideView.cpp`

---

## Setup

### 1. Clone or fork this repo (leetcode-automation).

### 2. Prepare your `leetcode-solutions` repo with your code files.

### 3. Configure GitHub Secrets in `leetcode-automation` repo:

- `LEETCODE_USERNAME`: Your LeetCode username or email.
- `LEETCODE_PASSWORD`: Your LeetCode password.

---

## How It Works

- The GitHub Actions workflow runs daily (default 4 AM UTC).
- It checks out both repos.
- Picks a random `.cpp` solution from `leetcode-solutions`.
- Extracts the problem slug from the filename.
- Logs in to LeetCode.
- Navigates to the problem page.
- Selects C++ as the language.
- Pastes your solution.
- Submits the solution.

---

## Customize

- Change the language by modifying the script `submit_from_repo.py` (e.g., Python, Java).
- Modify the cron schedule in `.github/workflows/submit.yml`.

---

## Dependencies

- Python 3.10+
- Selenium

---

## Usage

You can trigger the workflow manually from the GitHub Actions tab or wait for the scheduled run.

---

## Troubleshooting

- Make sure your filenames follow the format exactly.
- Ensure your GitHub secrets are set correctly.
- Check the workflow logs on GitHub Actions for errors.

---

## License

MIT License © Your Name
