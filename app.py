import streamlit as st
import requests

# ВАША ссылка Google Apps Script (Web App)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzP6BWsOot6hoZm5YI7UZPks7unAlpZ8w7IJ_gLSYL8ktRrm1IwxpM9CRxgghS-8cPJ/exec"

st.set_page_config(page_title="Idea.bkz", layout="centered")

st.title("Idea.bkz")
st.subheader("Интеллектуальная платформа обратной связи")
st.caption("Биология, 7 класс")

st.markdown("---")

st.info("Заполните форму и нажмите «Отправить». Ответ сохранится в таблице учителя.")

with st.form("student_form"):
    name = st.text_input("ФИО ученика", placeholder="Например: Айдана С.")
    klass = st.text_input("Класс", placeholder="Например: 7А")

    st.markdown("### Задание")
    q1 = st.text_area("1) Ваш ответ на вопрос 1", height=120)
    q2 = st.text_area("2) Ваш ответ на вопрос 2", height=120)

    submitted = st.form_submit_button("Отправить ✅")

if submitted:
    if not name.strip() or not klass.strip() or not q1.strip() or not q2.strip():
        st.error("Пожалуйста, заполните все поля.")
    else:
        payload = {
            "name": name.strip(),
            "klass": klass.strip(),
            "q1": q1.strip(),
            "q2": q2.strip(),
        }

        try:
            r = requests.post(SCRIPT_URL, json=payload, timeout=20)
            # иногда GAS отвечает текстом — это нормально
            if r.status_code == 200:
                st.success("Готово! Ответ отправлен учителю и сохранён.")
                st.balloons()
            else:
                st.error(f"Не удалось отправить (код {r.status_code}). Попробуйте ещё раз.")
                st.text(r.text[:500])
        except Exception as e:
            st.error("Ошибка соединения. Проверьте интернет и попробуйте ещё раз.")
            st.text(str(e))
