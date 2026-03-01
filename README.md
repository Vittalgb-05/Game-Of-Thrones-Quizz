# ⚔ Game of Thrones Trivia App

## 📌 Project Overview

Game of Thrones Trivia is a web-based quiz application built with Streamlit.
It presents multiple-choice questions from a JSON question bank, tracks score in real time,
and supports custom quiz settings such as difficulty filtering and question count.

---

## 🚀 Features

- Randomized question order each game
- Multiple difficulty levels (Easy/Medium)
- Configurable number of questions
- Category and difficulty labels per question
- Instant feedback with explanations
- Real-time score tracking and final accuracy
- Session high score tracking
- One-click game restart

---

## 🛠 Technologies Used

- Python
- Streamlit
- JSON (question data store)
- `random` and `pathlib` from Python standard library

---

## 📂 Project Structure

```text
Game-Of-Thrones-Quizz/
├── GOT.py            # Streamlit application code
├── questions.json    # Quiz question bank
├── requirements.txt  # Python dependencies
└── README.md
```

---

## ▶ How to Run the Application

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run GOT.py
```

3. Open the URL shown in your terminal (typically `http://localhost:8501`).

---

## 🎯 Purpose

This project is intended for learning interactive web app development with Streamlit,
state management, and lightweight data-driven quiz design.

---

## 👨‍💻 Author

Vittal
Engineering Student
