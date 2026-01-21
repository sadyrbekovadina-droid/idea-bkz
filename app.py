import streamlit as st
import requests
from datetime import datetime

# =============================
# 1) ВСТАВЬ СВОЮ ССЫЛКУ APPS SCRIPT
# =============================
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRbvRnuvqkKx80kaYTT9f5G1ba8G97zq9qITe3MTJ0Z-Gmj9FO_tuBg1COQ-0Oy-dL/exec"

APP_TITLE = "Idea.bkz"
APP_SUBTITLE = "Платформа заданий и обратной связи (7 класс)"

st.set_page_config(page_title=APP_TITLE, layout="centered")

# =============================
# 2) ВОПРОСЫ (их легко менять)
# =============================

TEST_TITLE = "ТЕСТ: Нервная система (10 вопросов = 10 баллов)"

TEST_QUESTIONS = [
    {
        "id": "t1",
        "q": "1) Какая система органов управляет работой всего организма?",
        "options": ["Кровеносная", "Нервная", "Пищеварительная"],
        "answer": "Нервная",
    },
    {
        "id": "t2",
        "q": "2) Основная структурная и функциональная единица нервной системы:",
        "options": ["Нейрон", "Нефрон", "Альвеола"],
        "answer": "Нейрон",
    },
    {
        "id": "t3",
        "q": "3) Как называется отдел головного мозга, отвечающий за координацию движений?",
        "options": ["Мозжечок", "Продолговатый мозг", "Гипофиз"],
        "answer": "Мозжечок",
    },
    {
        "id": "t4",
        "q": "4) Что такое рефлекс?",
        "options": ["Ответ организма на раздражитель", "Способ питания", "Обмен веществ"],
        "answer": "Ответ организма на раздражитель",
    },
    {
        "id": "t5",
        "q": "5) По какой части нервной системы идут сигналы от рецепторов к ЦНС?",
        "options": ["Чувствительные (афферентные) нервы", "Двигательные нервы", "Только спинной мозг"],
        "answer": "Чувствительные (афферентные) нервы",
    },
    {
        "id": "t6",
        "q": "6) Центральная нервная система включает:",
        "options": ["Головной и спинной мозг", "Нервы и рецепторы", "Мышцы и кости"],
        "answer": "Головной и спинной мозг",
    },
    {
        "id": "t7",
        "q": "7) Вегетативная (автономная) нервная система регулирует:",
        "options": ["Работу внутренних органов", "Рост костей", "Размножение бактерий"],
        "answer": "Работу внутренних органов",
    },
    {
        "id": "t8",
        "q": "8) Синапс — это:",
        "options": ["Место контакта между нейронами", "Кость черепа", "Часть сердца"],
        "answer": "Место контакта между нейронами",
    },
    {
        "id": "t9",
        "q": "9) Как называется защитная оболочка нервных волокон, ускоряющая проведение импульса?",
        "options": ["Миелин", "Хлорофилл", "Гемоглобин"],
        "answer": "Миелин",
    },
    {
        "id": "t10",
        "q": "10) Что из перечисленного помогает сохранить здоровье нервной системы?",
        "options": ["Недосып и стресс", "Режим сна, отдых, движение", "Только сладкое питание"],
        "answer": "Режим сна, отдых, движение",
    },
]

OPEN_TITLE = "ОТКРЫТЫЕ ВОПРОСЫ: Нервная система (5 вопросов)"

OPEN_QUESTIONS = [
    {"id": "o1", "q": "1) Объясни своими словами, что такое рефлекс. Приведи 1 пример."},
    {"id": "o2", "q": "2) Чем отличается центральная нервная система от периферической?"},
    {"id": "o3", "q": "3) Назови 3 правила сохранения здоровья нервной системы."},
    {"id": "o4", "q": "4) Почему сон важен для нервной системы? (2–3 предложения)"},
    {"id": "o5", "q": "5) Как стресс влияет на организм? (2–3 факта)"},
]

# =============================
# 3) ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =============================

def system_comment(score_10: int) -> str:
    if score_10 >= 9:
        return "Отлично! Ты хорошо понимаешь тему."
    if score_10 >= 7:
        return "Хороший результат. Повтори слабые места и попробуй улучшить."
    if score_10 >= 5:
        return "Средний результат. Повтори теорию и сделай тренировку ещё раз."
    return "Нужно подтянуть тему: повтори конспект и обратись к учителю за помощью."

def safe_post(payload: dict) -> tuple[bool, str]:
    try:
        r = requests.post(SCRIPT_URL, json=payload, timeout=20)
        if r.status_code != 200:
            return False, f"Ошибка: HTTP {r.status_code}"
        text = r.text.strip()
        return True, text
    except Exception as e:
        return False, f"Ошибка отправки: {e}"

def safe_get(params: dict) -> tuple[bool, dict]:
    try:
        r = requests.get(SCRIPT_URL, params=params, timeout=20)
        if r.status_code != 200:
            return False, {"error": f"HTTP {r.status_code}"}
        return True, r.json()
    except Exception as e:
        return False, {"error": str(e)}

# =============================
# 4) SESSION STATE (чтобы НЕ исчезало)
# =============================
if "page" not in st.session_state:
    st.session_state.page = "home"

# чтобы не терять ФИО/класс
if "fio" not in st.session_state:
    st.session_state.fio = ""
if "klass" not in st.session_state:
    st.session_state.klass = ""

# =============================
# 5) UI: Заголовок
# =============================
st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

# =============================
# 6) Проверяем режим (учитель/ученик)
# =============================
# Учительский режим включается только если открыть ссылку так:
# https://ВАШ_САЙТ?... -> добавить ?admin=1
try:
    qp = st.query_params
    is_admin = str(qp.get("admin", "0")) == "1"
except Exception:
    is_admin = False

# =============================
# 7) ДАННЫЕ УЧЕНИКА
# =============================
st.subheader("Данные ученика")
fio = st.text_input("ФИО ученика", value=st.session_state.fio, placeholder="Например: Иванов Иван")
klass = st.text_input("Класс (например: 7А)", value=st.session_state.klass, placeholder="Например: 7А")

st.session_state.fio = fio
st.session_state.klass = klass

colA, colB = st.columns(2)
with colA:
    if st.button("Открыть ТЕСТ"):
        st.session_state.page = "test"
with colB:
    if st.button("Открыть ОТКРЫТЫЕ ВОПРОСЫ"):
        st.session_state.page = "open"

st.divider()

# =============================
# 8) Комментарий учителя (УЧЕНИК ВИДИТ ТОЛЬКО КНОПКУ "ПОКАЗАТЬ")
# =============================
st.subheader("Комментарий учителя (если он добавлен)")
st.caption("Заполни ФИО и класс → нажми кнопку. Если учитель уже написал комментарий — он появится.")

if st.button("Показать комментарий учителя"):
    if not fio.strip() or not klass.strip():
        st.warning("Сначала заполни ФИО и класс.")
    else:
        ok, data = safe_get({"action": "get_teacher_comment", "fio": fio.strip(), "klass": klass.strip()})
        if not ok:
            st.error(f"Не удалось получить комментарий: {data.get('error')}")
        else:
            comment = data.get("teacher_comment", "")
            score = data.get("teacher_score", "")
            if not comment and score == "":
                st.info("Комментарий учителя пока не добавлен.")
            else:
                if score != "":
                    st.success(f"Оценка учителя: {score}/10")
                if comment:
                    st.write(f"**Комментарий учителя:** {comment}")

st.divider()

# =============================
# 9) Учительская панель (СКРЫТА ДЛЯ УЧЕНИКА)
# =============================
if is_admin:
    st.subheader("Панель учителя (видна только по ссылке с ?admin=1)")
    st.caption("Здесь учитель может выставить итоговую оценку (0–10) и написать комментарий ученику.")

    pin = st.text_input("PIN учителя", type="password", placeholder="Пример: 1234")
    teacher_score = st.number_input("Итоговая оценка (0–10)", min_value=0, max_value=10, value=10, step=1)
    teacher_comment = st.text_area("Комментарий учителя", placeholder="Например: Хорошо справился, но повтори...")

    if st.button("Сохранить комментарий и оценку ученику"):
        if not fio.strip() or not klass.strip():
            st.warning("Сначала заполни ФИО и класс ученика.")
        else:
            payload = {
                "action": "set_teacher_comment",
                "pin": pin,
                "fio": fio.strip(),
                "klass": klass.strip(),
                "teacher_score": int(teacher_score),
                "teacher_comment": teacher_comment.strip(),
            }
            ok, msg = safe_post(payload)
            if ok:
                st.success("Сохранено.")
            else:
                st.error(f"Не сохранилось: {msg}")

    st.divider()

# =============================
# 10) Страница ТЕСТ
# =============================
if st.session_state.page == "test":
    st.header("Раздел: ТЕСТ")
    st.caption(TEST_TITLE)

    if not fio.strip() or not klass.strip():
        st.warning("Сначала заполни ФИО и класс (вверху).")
    else:
        student_answers = {}
        for item in TEST_QUESTIONS:
            student_answers[item["id"]] = st.radio(item["q"], item["options"], key=f"test_{item['id']}")

        if st.button("✅ Отправить ответы (ТЕСТ)"):
            # подсчёт баллов
            score = 0
            for item in TEST_QUESTIONS:
                if student_answers[item["id"]] == item["answer"]:
                    score += 1

            sys_comment = system_comment(score)

            # отправка в таблицу
            payload = {
                "action": "submit_test",
                "timestamp": datetime.now().isoformat(),
                "fio": fio.strip(),
                "klass": klass.strip(),
                "topic": "Нервная система — тест",
                "score_10": score,
                "system_comment": sys_comment,
                "answers": student_answers,  # все 10 ответов
            }

            ok, msg = safe_post(payload)
            if ok:
                st.success(f"Готово! Балл: {score}/10")
                st.info(f"Комментарий системы: {sys_comment}")
            else:
                st.error(f"Ответ показан, но в таблицу не записался: {msg}")

    st.divider()
    if st.button("⬅️ Назад"):
        st.session_state.page = "home"

# =============================
# 11) Страница ОТКРЫТЫЕ
# =============================
if st.session_state.page == "open":
    st.header("Раздел: ОТКРЫТЫЕ ВОПРОСЫ")
    st.caption(OPEN_TITLE)

    if not fio.strip() or not klass.strip():
        st.warning("Сначала заполни ФИО и класс (вверху).")
    else:
        open_answers = {}
        for item in OPEN_QUESTIONS:
            open_answers[item["id"]] = st.text_area(item["q"], key=f"open_{item['id']}")

        # Предварительная автооценка (простая, чтобы было честно: по заполненности)
        filled = sum(1 for v in open_answers.values() if v and v.strip())
        pre_score = min(10, int(round((filled / len(OPEN_QUESTIONS)) * 10)))
        pre_comment = system_comment(pre_score)

        if st.button("✅ Отправить ответы (ОТКРЫТЫЕ)"):
            payload = {
                "action": "submit_open",
                "timestamp": datetime.now().isoformat(),
                "fio": fio.strip(),
                "klass": klass.strip(),
                "topic": "Нервная система — открытые",
                "pre_score_10": pre_score,
                "system_comment": pre_comment,
                "answers": open_answers,  # 5 ответов
            }

            ok, msg = safe_post(payload)
            if ok:
                st.success(f"Готово! Предварительный балл: {pre_score}/10")
                st.info(f"Комментарий системы: {pre_comment} (Итог проверит учитель.)")
            else:
                st.error(f"Ответ показан, но в таблицу не записался: {msg}")

    st.divider()
    if st.button("⬅️ Назад "):
        st.session_state.page = "home"

