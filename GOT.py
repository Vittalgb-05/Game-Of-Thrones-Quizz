import json
import random
from pathlib import Path

import streamlit as st

DATA_FILE = Path(__file__).with_name("questions.json")


def load_questions() -> list[dict]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    required_fields = {"question", "options", "answer", "difficulty", "category", "explanation"}
    for index, question in enumerate(questions, start=1):
        missing = required_fields - question.keys()
        if missing:
            raise ValueError(f"Question {index} is missing required fields: {sorted(missing)}")
        if question["answer"] not in question["options"]:
            raise ValueError(f"Question {index} has an answer not present in options")

    return questions


ALL_QUESTIONS = load_questions()
AVAILABLE_DIFFICULTIES = sorted({q["difficulty"] for q in ALL_QUESTIONS})


def build_quiz_questions(difficulties: list[str], number_of_questions: int) -> list[dict]:
    filtered_questions = [q for q in ALL_QUESTIONS if q["difficulty"] in difficulties]
    if not filtered_questions:
        return []

    number_to_pick = min(number_of_questions, len(filtered_questions))
    return random.sample(filtered_questions, number_to_pick)


def start_new_game(difficulties: list[str], number_of_questions: int) -> None:
    st.session_state.questions = build_quiz_questions(difficulties, number_of_questions)
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.submitted = False
    st.session_state.last_selection = None
    st.session_state.game_over = len(st.session_state.questions) == 0


def initialize_state() -> None:
    if "high_score" not in st.session_state:
        st.session_state.high_score = 0

    if "questions" not in st.session_state:
        start_new_game(AVAILABLE_DIFFICULTIES, min(5, len(ALL_QUESTIONS)))


def render_sidebar() -> tuple[list[str], int]:
    with st.sidebar:
        st.header("⚙️ Quiz Settings")
        selected_difficulties = st.multiselect(
            "Difficulty",
            AVAILABLE_DIFFICULTIES,
            default=AVAILABLE_DIFFICULTIES,
        )

        max_questions = max(1, len([q for q in ALL_QUESTIONS if q["difficulty"] in selected_difficulties]))
        number_of_questions = st.slider("Number of questions", min_value=1, max_value=max_questions, value=min(5, max_questions))

        if st.button("Start New Quiz", use_container_width=True):
            start_new_game(selected_difficulties, number_of_questions)
            st.rerun()

        st.divider()
        st.metric("🏆 High score", f"{st.session_state.high_score}")

    return selected_difficulties, number_of_questions


def render_active_question() -> None:
    question_data = st.session_state.questions[st.session_state.question_index]
    total_questions = len(st.session_state.questions)
    current_question_number = st.session_state.question_index + 1

    st.progress(st.session_state.question_index / total_questions)
    st.caption(f"Question {current_question_number} of {total_questions}")
    st.caption(f"Category: {question_data['category']} • Difficulty: {question_data['difficulty']}")
    st.subheader(question_data["question"])

    selected_option = st.radio(
        "Choose your answer:",
        question_data["options"],
        key=f"question_{st.session_state.question_index}",
        disabled=st.session_state.submitted,
    )

    if not st.session_state.submitted:
        if st.button("Submit Answer", type="primary"):
            st.session_state.submitted = True
            st.session_state.last_selection = selected_option
            if selected_option == question_data["answer"]:
                st.session_state.score += 1
                st.success("Correct! 🏆")
            else:
                st.error(f"Wrong! Correct answer: {question_data['answer']}")
            st.info(question_data["explanation"])
            st.rerun()
    else:
        if st.session_state.last_selection == question_data["answer"]:
            st.success("Correct! 🏆")
        else:
            st.error(f"Wrong! Correct answer: {question_data['answer']}")
        st.info(question_data["explanation"])

        if st.button("Next Question"):
            st.session_state.question_index += 1
            st.session_state.submitted = False
            st.session_state.last_selection = None

            if st.session_state.question_index >= total_questions:
                st.session_state.game_over = True
                st.session_state.high_score = max(st.session_state.high_score, st.session_state.score)

            st.rerun()


def render_game_over() -> None:
    total_questions = len(st.session_state.questions)
    st.success(f"Game Over! 🎉 Your Score: {st.session_state.score}/{total_questions}")

    percentage = (st.session_state.score / total_questions) * 100 if total_questions else 0
    st.write(f"Accuracy: **{percentage:.0f}%**")

    if st.session_state.score == st.session_state.high_score and total_questions > 0:
        st.balloons()
        st.write("🎖️ You matched the session high score!")

    if st.button("Restart Game", type="primary"):
        start_new_game(AVAILABLE_DIFFICULTIES, min(5, len(ALL_QUESTIONS)))
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="Game of Thrones Trivia", page_icon="⚔", layout="centered")
    st.title("⚔ Game of Thrones Trivia")
    st.write("Test your Westeros knowledge with randomized questions and difficulty filters.")

    initialize_state()
    render_sidebar()

    st.write(f"Current score: **{st.session_state.score}**")

    if st.session_state.game_over:
        render_game_over()
    else:
        render_active_question()


if __name__ == "__main__":
    main()
