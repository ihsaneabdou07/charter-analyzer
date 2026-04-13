🛡️ Project Charter Health Analyzer (NLP)
📌 Overview
This project is an AI-powered decision-support tool designed to evaluate the quality of a Project Charter. As a general engineering student at École Centrale Casablanca, I developed this tool to bridge the gap between Project Management principles (the Triple Constraint) and Natural Language Processing (NLP).

The application automatically extracts key project data and assesses the "health" of the documentation to ensure that Scope, Time, and Cost are clearly defined.

🚀 Features
Named Entity Recognition (NER): Uses spaCy to automatically detect budget figures (Cost) and deadlines (Time).

Triple Constraint Scoring: Evaluates if the three pillars of project management are present in the text.

Sentiment & Risk Analysis: Uses TextBlob to detect if the tone of the document suggests high risk or uncertainty.

Interactive Dashboard: A clean, web-based UI built with Streamlit.

🛠️ Tech Stack
Language: Python 3.x

NLP Libraries: spaCy (en_core_web_sm), TextBlob

Frontend: Streamlit

Version Control: Git & GitHub

📖 How to Use
Clone the repository:

Bash
git clone https://github.com/ihsaneabdou07/charter-analyzer.git
Install dependencies:

Bash
pip install streamlit spacy textblob
python -m spacy download en_core_web_sm
Run the application:

Bash
streamlit run app.py
Upload a .txt file containing your project description or charter.

🎓 Academic Context
This project was developed as a personal initiative to apply Software Engineering best practices (learnt during Coding Week 2026) to real-world management challenges. It serves as a prototype for more advanced AI applications in the field of Agri-Tech and Sustainable Engineering.
