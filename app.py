import streamlit as st
import requests
from urllib.parse import urlencode

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxI233LLqpJV1AhaeYZsnihmsp3i_OyGGHZDUvGKzcz-Q7DRSL7zvlYDBRpdUmCaQes/exec"

st.set_page_config(page_title="Idea.bkz", layout="centered")

def get_mode() -> str:
    mode = st.query_params.get("mode", "test")
    return mode if mode in ["test", "open"] else "test"

def send_to_sheet(payload: dict) -> tuple[bool, str]:
    try:
        r = requests.post(SCRIPT_URL, json=payload, timeout=20)
        if r.status_code != 200:
            return False, f"HTTP {r.status_code}"
        js = r.json()
        if js.get("status") == "ok":
            return True, "ok"
        return False, js.get("message", "unknown error")
    except Exception as e:
        return False, str(e)

def get_teacher_comment(name: str, klass: str, section: str) -> tuple[bool, str]:
    try:
        params = {"action": "get_comment", "name": name, "klass": klass, "section": section}
        url = f"{SCRIPT_URL}?{urlencode(params)}"
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            return False, f"HTTP {r.status_code}"
        js = r.json()
        if js.get("status") != "ok":
            return False, js.get("message", "unknown error")
        if not js.get("found"):
            return True, ""  # комментария пока нет
        return True, js.get("comment", "")
    except Exception as e:
        return False, str(e)

# ---------------- ВОПРОСЫ ----------------
TEST_TOPIC = "Выделение (7 класс)"
TEST_QUESTIONS = [
    ("Главный орган выделения у человека:", ["Почки", "Печень", "Лёгкие"], "Почки"),
    ("Структурная единица почки:", ["Нефрон", "Альвеола", "Нейрон"], "Нефрон"),
    ("Где образуется первичная моча:", ["В клубочке и капсуле нефрона", "В мочеточнике", "В мочевом пузыре"], "В клубочке и капсуле нефрона"),
    ("Как называется процесс удаления конечных продуктов обмена:", ["Выделение", "Дыхание", "Питание"], "Выделение"),
    ("Какой орган выводит CO₂ и водяной пар:", ["Лёгкие", "Почки", "Кожа"], "Лёгкие"),
    ("Через кожу выделяются:", ["Пот", "Желчь", "Слюна"], "Пот"),
    ("Моча из почек поступает в:", ["Мочеточники", "Артерии", "Кишечник"], "Мочеточники"),
    ("Где накапливается моча:", ["Мочевой пузырь", "Желудок", "Сердце"], "Мочевой пузырь"),
    ("Что из перечисленного относится к продуктам обмена:", ["Мочевина", "Кислород", "Крахмал"], "Мочевина"),
    ("Какой орган участвует в обезвреживании токсинов:", ["Печень", "Поджелудочная железа", "Селезёнка"], "Печень"),
]

OPEN_TOPIC = "Нервная система (7 класс) — открытые вопросы"
OPEN_QUESTIONS = [
    "1) Что такое нервная система? Дай определение.",
    "2) Назови 2–3 функции нервной системы.",
    "3) Из каких отделов состоит ЦНС?",
    "4) Что относится к ПНС? Приведи примеры.",
    "5) Кто такая нервная клетка (нейрон)? Основная функция.",
    "6) Что такое рефлекс? Приведи пример.",
    "7) Чем отличается условный рефлекс от безусловного?",
    "8) Что такое синапс? (1–2 предложения)",
    "9) Почему спинной мозг важен для движений и рефлексов?",
    "10) Назови 3 правила сохранения здоровья нервной системы."
]

# ---------------- UI ----------------
st.title("Idea.bkz")
st.subheader("Платформа обратной связи (7 класс)")

mode = get_mode()

c1, c2 = st.columns(2)
with c1:
    st.link_button("Открыть ТЕСТ", "?mode=test")
with c2:
    st.link_button("Открыть ОТКРЫТЫЕ ВОПРОСЫ", "?mode=open")

st.markdown("---")

st.markdown("## Данные ученика")
name = st.text_input("ФИО ученика", placeholder="Например: Иванов Иван")
klass = st.text_input("Класс (например: 7А)", placeholder="Например: 7А")

st.markdown("---")

# Блок “Комментарий учителя”
if name.strip() and klass.strip():
    section_for_comment = "test" if mode == "test" else "open"
    if st.button("📩 Показать комментарий учителя"):
        ok, comment = get_teacher_comment(name.strip(), klass.strip(), section_for_comment)
        if ok:
            if comment:
                st.success(f"Комментарий учителя: {comment}")
            else:
                st.info("Комментария пока нет. Учитель добавит его после проверки.")
        else:
            st.warning(f"Не удалось получить комментарий ({comment}).")

# ---------------- РАЗДЕЛЫ ----------------
if mode == "test":
    st.markdown("## 🟦 Раздел: ТЕСТ")
    st.caption(f"Тема: {TEST_TOPIC}")

    answers = {}
    for i, (q_text, options, _) in enumerate(TEST_QUESTIONS, start=1):
        st.markdown(f"**{i}. {q_text}**")
        answers[f"q{i}"] = st.radio("", options=options, key=f"test_q{i}")

    st.markdown("---")

    if st.button("✅ Отправить ответы (ТЕСТ)"):
        if not name.strip() or not klass.strip():
            st.error("Заполни ФИО и класс.")
            st.stop()

        score = 0
        for i, (_, _, correct) in enumerate(TEST_QUESTIONS, start=1):
            if answers[f"q{i}"] == correct:
                score += 1

        payload = {
            "name": name.strip(),
            "klass": klass.strip(),
            "section": "test",
            "topic": TEST_TOPIC,
            "score": score,
            **answers
        }

        ok, msg = send_to_sheet(payload)
        if ok:
            st.success(f"Готово! Результат: {score}/10. Ответы записаны в таблицу.")
        else:
            st.warning(f"Ответ показан, но в таблицу не записался ({msg}).")

elif mode == "open":
    st.markdown("## 🟩 Раздел: ОТКРЫТЫЕ ВОПРОСЫ")
    st.caption(f"Тема: {OPEN_TOPIC}")

    answers = {}
    for i, q_text in enumerate(OPEN_QUESTIONS, start=1):
        answers[f"q{i}"] = st.text_area(q_text, placeholder="Напиши ответ...", key=f"open_q{i}", height=90)

    st.markdown("---")

    if st.button("✅ Отправить ответы (ОТКРЫТЫЕ)"):
        if not name.strip() or not klass.strip():
            st.error("Заполни ФИО и класс.")
            st.stop()

        payload = {
            "name": name.strip(),
            "klass": klass.strip(),
            "section": "open",
            "topic": OPEN_TOPIC,
            "score": "",
            **answers
        }

        ok, msg = send_to_sheet(payload)
        if ok:
            st.success("Готово! Ответы записаны в таблицу. Учитель проверит и выставит баллы.")
        else:
            st.warning(f"Ответ показан, но в таблицу не записался ({msg}).")
