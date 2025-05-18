import os, random, re, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def get_slug_from_filename(filename):
    match = re.match(r"^\d+-(.+)\.(cpp|py|java|.*)$", filename)
    if not match:
        return None
    raw_title = match.group(1)
    return re.sub(r"([a-z])([A-Z])", r"\1-\2", raw_title).lower()

def get_random_solution_file(root="leetcode-solutions"):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.endswith(".cpp"):
                files.append(os.path.join(dirpath, file))
    return random.choice(files)

# Load credentials from environment variables
username = os.environ['LEETCODE_USERNAME']
password = os.environ['LEETCODE_PASSWORD']

# Setup headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

try:
    # Pick random solution
    file_path = get_random_solution_file()
    filename = os.path.basename(file_path)
    slug = get_slug_from_filename(filename)
    if not slug:
        raise Exception("Invalid filename format")
    url = f"https://leetcode.com/problems/{slug}/"

    with open(file_path, "r") as f:
        code = f.read()

    # Log in
    driver.get("https://leetcode.com/accounts/login/")
    time.sleep(3)
    driver.find_element(By.ID, "id_login").send_keys(username)
    driver.find_element(By.ID, "id_password").send_keys(password)
    driver.find_element(By.ID, "id_password").send_keys(Keys.RETURN)
    time.sleep(5)

    # Go to problem page
    driver.get(url)
    time.sleep(5)

    # Select C++
    driver.find_element(By.CLASS_NAME, "ant-select-selector").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[text()='C++']").click()
    time.sleep(3)

    # Paste code
    editor = driver.find_element(By.CLASS_NAME, "monaco-editor")
    editor.click()
    editor.send_keys(Keys.CONTROL + "a")
    editor.send_keys(Keys.DELETE)
    for line in code.split("\n"):
        editor.send_keys(line)
        editor.send_keys(Keys.ENTER)

    # Submit
    submit = driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")
    submit.click()
    time.sleep(5)
    print(f"✅ Submitted: {url}")
finally:
    driver.quit()
