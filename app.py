import streamlit as st
import requests

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRbvRnuvqkKx80kaYTT9f5G1ba8G97zq9qITe3MTJ0Z-Gmj9FO_tuBg1COQ-0Oy-dL/exec"

st.set_page_config(page_title="Idea.bkz", layout="centered")

st.title("Idea.bkz")
st.subheader("Платформа заданий и обратной связи (7 класс)")

# ===== ДАННЫЕ УЧЕНИКА =====
name = st.text_input("ФИО ученика")
klass = st.text_input("Класс (например: 7A)")

# ===== КНОПКИ РАЗДЕЛОВ =====
col1, col2 = st.columns(2)
show_test = col1.button("Открыть ТЕСТ")
show_open = col2.button("Открыть ОТКРЫТЫЕ ВОПРОСЫ")

# ===== ТЕСТ =====
if show_test:
    st.header("Раздел: ТЕСТ (10 баллов)")

    answers = []
    correct = ["Почки","Нефрон","Моча","Кровь","Почки","Почки","Мочеточник","Мочевой пузырь","Мочеиспускание","Почки"]

    questions = [
        ("Главный орган выделения:", ["Печень","Почки","Лёгкие"]),
        ("Структурная единица почки:", ["Нефрон","Альвеола","Нейрон"]),
        ("Что выводится из организма:", ["Моча","Слюна","Желчь"]),
        ("Из чего образуется моча:", ["Кровь","Лимфа","Плазма"]),
        ("Парный орган выделения:", ["Почки","Печень","Сердце"]),
        ("Где образуется моча:", ["Почки","Мочевой пузырь","Мочеточник"]),
        ("Путь мочи из почек:", ["Мочеточник","Артерия","Вена"]),
        ("Где накапливается моча:", ["Мочевой пузырь","Почка","Уретра"]),
        ("Выведение мочи:", ["Мочеиспускание","Фильтрация","Диффузия"]),
        ("Главная функция почек:", ["Почки","Лёгкие","Печень"])
    ]

    score = 0
    for i, q in enumerate(questions):
        ans = st.radio(q[0], q[1], key=i)
        if ans == correct[i]:
            score += 1

    if st.button("Отправить ТЕСТ"):
        r = requests.post(SCRIPT_URL, json={
            "action":"submit_test",
            "name":name,
            "class":klass,
            "score":score
        })
        st.success(f"Готово! Балл: {score}/10")
        st.info(r.json()["comment"])

# ===== ОТКРЫТЫЕ =====
if show_open:
    st.header("Раздел: ОТКРЫТЫЕ ВОПРОСЫ (10 баллов)")

    q_open = [
        "Назови 3 правила сохранения здоровья нервной системы.",
        "Почему важен сон?",
        "Роль нервной системы.",
        "Что вредно для нервной системы?",
        "Пример стрессовой ситуации."
    ]

    answers = []
    for i, q in enumerate(q_open):
        text = st.text_area(q)
        points = 2 if len(text.split()) >= 3 else 1
        answers.append({"points":points})

    if st.button("Отправить ОТКРЫТЫЕ"):
        r = requests.post(SCRIPT_URL, json={
            "action":"submit_open",
            "name":name,
            "class":klass,
            "answers":answers
        })
        st.success(f"Готово! Балл: {r.json()['score']}/10")
        st.info(r.json()["comment"])

# ===== КОММЕНТАРИЙ =====
st.divider()
if st.button("Показать комментарий учителя"):
    r = requests.post(SCRIPT_URL, json={
        "action":"get_teacher_comment",
        "name":name,
        "class":klass
    })
    st.info(r.json()["comment"])
