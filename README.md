# IntervalScribe AI

IntervalScribe AI is a productivity tool that automatically captures, OCRs, and summarizes your on-screen work at regular intervals. It helps you keep a detailed, time-stamped log of your daily activities, making it easy to review, summarize, and document your work sessions.

## Features
- Automatic screen capture at user-defined intervals
- Optical Character Recognition (OCR) to extract text from screenshots
- Real-time activity logging and summarization
- Summarize your day with a single click
- Customizable interval, logging, and display options
- Modern, clean UI built with CustomTkinter

## Technologies Used
- **Python 3**: Core programming language
- **CustomTkinter**: Modern Python GUI framework for the desktop interface
- **pytesseract**: Python wrapper for Tesseract OCR engine
- **Tesseract OCR**: Open-source OCR engine (must be installed separately)
- **python-dotenv**: For environment variable management
- **Google Gemini AI (via google-generativeai)**: Provides advanced natural language processing to generate human-like summaries of your activities

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/IntervalScribeAI.git
cd IntervalScribeAI
```

### 2. Install Python Dependencies
It is recommended to use a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
If `requirements.txt` is missing, install manually:
```sh
pip install customtkinter pytesseract python-dotenv google-generativeai
```

### 3. Install Tesseract OCR
- **Windows:** Download and install from [UB Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS:** `brew install tesseract`
- **Linux:** `sudo apt-get install tesseract-ocr`

Make sure Tesseract is in your system PATH. Test with:
```sh
tesseract --version
```

### 4. Set Up Google Gemini API Key
- Sign up for access and obtain your Gemini API key from Google.
- Create a `.env` file in the project root with the following content:
  ```
  GEMINI_API_KEY=your_api_key_here
  ```

### 5. Run the Application
```sh
python __main__.py
```

## Usage
- Set your desired interval and options in the GUI.
- Click **Start** to begin automatic screen capture and logging.
- Click **Stop** to pause.
- Use **Clear** to reset the log area.
- Click **Summarize Day** for a summary of your activities.

