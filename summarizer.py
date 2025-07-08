import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=GEMINI_API_KEY)

def summarize_text(text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "You are a helpful assistant that summarizes what the user is doing based on text seen on their screen, dont make assumptions on what they are working on, just summarize the text to explain what they are doing. "
            "Imagine you are filling out a time report for the user and need to say what you did during the day, don't use specific info, just do a broad summary of what they were working on. "
            "The user is a software engineer and is working on a project for a software contracting company. "
            "Don't speak in first person, just bullet point the tasks they were working on. "
            "Summarize the following screen text:\n" + text
        )
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"[Error generating summary: {e}]"

def summarize_day(bullets):
    if not bullets:
        return "No bullets accumulated for the day yet."
    bullets_text = '\n'.join(bullets)
    prompt = (
        "You are a helpful assistant. Summarize the following list of work log bullet points into a concise summary of the day, grouping similar tasks and avoiding repetition. Do not use first person.\n"
        "Bullets:\n" + bullets_text
    )
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"[Error generating day summary: {e}]"

def extract_bullets(summary):
    bullets = []
    for line in summary.splitlines():
        line = line.strip()
        if line.startswith(('*', '-', '•')):
            bullets.append(line)
    return bullets 