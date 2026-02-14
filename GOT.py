import streamlit as st
import random

# Game of Thrones Trivia Questions
QUESTIONS = [
    {
        "question": "What is the name of the white direwolf that Jon Snow finds?",
        "options": ["Nymeria", "Ghost", "Shaggydog", "Summer"],
        "answer": "Ghost"
    },
    {
        "question": "Which family's sigil is a golden lion on a crimson field?",
        "options": ["House Stark", "House Baratheon", "House Lannister", "House Targaryen"],
        "answer": "House Lannister"
    },
    {
        "question": "What title is given to the leader of the Night's Watch?",
        "options": ["King Beyond the Wall", "Lord Commander", "Master of Coin", "Hand of the King"],
        "answer": "Lord Commander"
    },
    {
        "question": "Which character is known as the 'Kingslayer'?",
        "options": ["Tyrion Lannister", "Jaime Lannister", "Jorah Mormont", "The Hound"],
        "answer": "Jaime Lannister"
    },
    {
        "question": "In which city is the Iron Throne located?",
        "options": ["Winterfell", "Casterly Rock", "King's Landing", "Dragonstone"],
        "answer": "King's Landing"
    }
]

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.questions = random.sample(QUESTIONS, len(QUESTIONS))
    st.session_state.game_over = False

st.title("⚔ Game of Thrones Trivia")

if not st.session_state.game_over:

    question_data = st.session_state.questions[st.session_state.question_index]
    st.subheader(f"Question {st.session_state.question_index + 1}")
    st.write(question_data["question"])

    selected_option = st.radio("Choose your answer:", question_data["options"])

    if st.button("Submit Answer"):
        if selected_option == question_data["answer"]:
            st.success("Correct! 🏆")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! Correct answer: {question_data['answer']}")

        st.session_state.question_index += 1

        if st.session_state.question_index >= len(st.session_state.questions):
            st.session_state.game_over = True

        st.rerun()

else:
    st.success(f"Game Over! 🎉 Your Score: {st.session_state.score}/{len(QUESTIONS)}")

    if st.button("Restart Game"):
        st.session_state.score = 0
        st.session_state.question_index = 0
        st.session_state.questions = random.sample(QUESTIONS, len(QUESTIONS))
        st.session_state.game_over = False
        st.rerun()
