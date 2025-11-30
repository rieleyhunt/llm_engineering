import os
from dotenv import load_dotenv

from openai import OpenAI
import requests
from bs4 import BeautifulSoup

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
OLLAMA_BASE_URL = "http://localhost:11434/v1"
openai = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

# Define the headers and website to scrape here
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def scrape_website(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def anaylze_content(content):
    messages = [
        {"role": "system", "content": "you are a website analyzer. You are going to take in text content from a website and provide a long detailed summary to the user"},
        {"role": "user", "content": content}
    ]
    response = openai.chat.completions.create(
        messages=messages,
        model="llama3.2"
    )
    return response.choices[0].message.content


content = scrape_website("https://finobe.com")
print(anaylze_content(content))

