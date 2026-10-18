import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(page_title="Powtórka przed Klasą 8", page_icon="🧪")

# 2. Definicja pytań (15 pytań z chemii klasy 7)
QUIZ_DATA = [
    {
        "question": "Jaki jest wzór sumaryczny wodorotlenku sodu (sody żrącej)?",
        "options": ["KOH", "NaOH", "NaCl", "Ca(OH)2"],
        "answer": "NaOH",
        "tip": "Wodorotlenki sodu zawierają kation sodu Na+ i grupę hydroksylową OH-."
    },
    {
        "question": "Która z wymienionych substancji jest mieszaniną jednorodną?",
        "options": ["Woda z piaskiem", "Woda z olejem", "Solanka (woda z solą)", "Granit"],
        "answer": "Solanka (woda z solą)",
        "tip": "Mieszanina jednorodna to taka, której składników nie widać gołym okiem ani pod lupą."
    },
    {
        "question": "Jak nazywa się przejście substancji ze stanu gazowego w stan ciekły?",
        "options": ["Kondensacja (skraplanie)", "Sublimacja", "Resublimacja", "Parowanie"],
        "answer": "Kondensacja (skraplanie)",
        "tip": "Skraplanie pary wodnej na zimnej szybie to przykład kondensacji."
    },
    {
        "question": "Która cząstka elementarna ma ładunek ujemny?",
        "options": ["Proton", "Neutron", "Elektron", "Nukleon"],
        "answer": "Elektron",
        "tip": "Elektrony krążą wokół jądra atomowego i mają ładunek ujemny."
    },
    {
        "question": "Ile wynosi maksymalna liczba elektronów na pierwszej powłoce (K)?",
        "options": ["8", "2", "18", "32"],
        "answer": "2",
        "tip": "Wzór na maksymalną liczbę elektronów to 2n², dla n=1 wynosi to 2."
    },
    {
        "question": "Wartościowość tlenu w większości związków chemicznych wynosi:",
        "options": ["I", "II", "IV", "VI"],
        "answer": "II",
        "tip": "Tlen prawie zawsze tworzy dwa wiązania chemiczne."
    },
    {
        "question": "Reakcja, w której z kilku substratów powstaje jeden produkt, to reakcja:",
        "options": ["Analizy (rozkładu)", "Wymiany", "Syntezy (łączenia)", "Spalania"],
        "answer": "Syntezy (łączenia)",
        "tip": "A + B -> AB to schemat reakcji syntezy."
    },
    {
        "question": "Jaki gaz podtrzymuje spalanie, ale sam się nie pali?",
        "options": ["Wodór", "Tlen", "Azot", "Dwutlenek węgla"],
        "answer": "Tlen",
        "tip": "Tlen jest niezbędny do procesu spalania."
    },
    {
        "question": "Odczyn roztworu o pH = 3 jest:",
        "options": ["Obojętny", "Kwasowy", "Zasadowy", "Alkaliczny"],
        "answer": "Kwasowy",
        "tip": "pH poniżej 7 oznacza odczyn kwasowy, a powyżej 7 – zasadowy."
    },
    {
        "question": "Jak zabarwi się papierek uniwersalny w roztworze kwasu?",
        "options": ["Na niebiesko", "Na zielono", "Na czerwono", "Nie zmieni barwy"],
        "answer": "Na czerwono",
        "tip": "Kwasy barwią uniwersalny papierek wskaźnikowy na odcienie czerwieni."
    },
    {
        "question": "Głównym składnikiem powietrza jest gaz o nazwie:",
        "options": ["Tlen", "Azot", "Argon", "Dwutlenek węgla"],
        "answer": "Azot",
        "tip": "Azot stanowi około 78% objętości suchego powietrza."
    },
    {
        "question": "Co to jest izotop?",
        "options": [
            "Atom tego samego pierwiastka o innej liczbie elektronów",
            "Atom tego samego pierwiastka o innej liczbie protonów",
            "Atom tego samego pierwiastka o innej liczbie neutronów",
            "Związek chemiczny o tym samym wzorze"
        ],
        "answer": "Atom tego samego pierwiastka o innej liczbie neutronów",
        "tip": "Izotopy różnią się liczbą masową (A), ale mają tę samą liczbę atomową (Z)."
    },
    {
        "question": "Który z wymienionych metali reaguje gwałtownie z zimną wodą?",
        "options": ["Miedź", "Żelazo", "Sód", "Złoto"],
        "answer": "Sód",
        "tip": "Metale alkaliczne (1. grupa) reagują z wodą bardzo energicznie, wydzielając wodór."
    },
    {
        "question": "Rozpuszczalność substancji to maksymalna liczba gramów substancji, którą można rozpuścić w:",
        "options": ["100 g rozpuszczalnika", "1 litrze wody", "10 g wody", "1000 g roztworu"],
        "answer": "100 g rozpuszczalnika",
        "tip": "Definicja rozpuszczalności odnosi się zawsze do 100 gramów rozpuszczalnika (zazwyczaj wody) w danej temperaturze."
    },
    {
        "question": "Wskaźnik fenoloftaleina w roztworze zasady (np. NaOH) zmienia barwę na:",
        "options": ["Malinową", "Żółtą", "Czerwoną", "Niebieską"],
        "answer": "Malinową",
        "tip": "Fenoloftaleina jest bezbarwna w kwasach, ale w zasadach przybiera intensywny malinowy kolor."
    }
]

# 3. Inicjalizacja stanu aplikacji (Streamlit Session State)
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_complete" not in st.session_state:
    st.session_state.quiz_complete = False
if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []


# 4. Funkcja resetująca quiz
def restart_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_complete = False
    st.session_state.wrong_answers = []


# INTERFEJS 

st.title("🧪 Quiz Diagnostyczny: Sprawdź klasę 7!")
st.write("Odpowiedz na 15 pytań, aby sprawdzić, które działy z poprzedniego roku wymagają powtórki.")

# Ekran podsumowania po zakończeniu quizu
if st.session_state.quiz_complete:
    st.success(f"### 🎉 Quiz ukończony! Twój wynik to: {st.session_state.score} / {len(QUIZ_DATA)}")

    # Procentowy próg wiedzy
    percentage = (st.session_state.score / len(QUIZ_DATA)) * 100
    if percentage >= 80:
        st.balloons()
        st.write("💪 Świetnie! Jesteś w pełni gotowy na wyzwania klasy 8!")
    elif percentage >= 50:
        st.write("👍 Dobry wynik, ale warto przejrzeć niektóre tematy przed trudniejszymi lekcjami.")
    else:
        st.error("⚠️ Sporo rzeczy uciekło z głowy. Zalecamy pełne powtórzenie materiału z klasy 7!")

    # Sekcja rekomendacji (pokazuje błędne odpowiedzi i wskazówki)
    if st.session_state.wrong_answers:
        st.write("#### 🔍 Obszary do powtórki:")
        for wa in st.session_state.wrong_answers:
            with st.expander(f"Pytanie: {wa['question']}"):
                st.write(f"❌ Twoja odpowiedź: *{wa['selected']}*")
                st.write(f"✅ Poprawna odpowiedź: **{wa['correct']}**")
                st.info(f"💡 **Wskazówka:** {wa['tip']}")

    st.button("Podejdź do quizu jeszcze raz", on_click=restart_quiz, type="primary")

# Ekran trwającego quizu
else:
    q_idx = st.session_state.current_question
    current_q = QUIZ_DATA[q_idx]

    # Pasek postępu
    progress_val = q_idx / len(QUIZ_DATA)
    st.progress(progress_val, text=f"Pytanie {q_idx + 1} z {len(QUIZ_DATA)}")

    # Wyświetlenie pytania w ładnej ramce
    st.info(f"### Pytanie {q_idx + 1}: {current_q['question']}")

    # Formularz obsługujący pojedyncze pytanie
    with st.form(key=f"question_form_{q_idx}"):
        user_choice = st.radio("Wybierz poprawną odpowiedź:", current_q["options"], index=None)
        submit_btn = st.form_submit_button("Zatwierdź odpowiedź", type="primary")

        if submit_btn:
            if user_choice is None:
                st.warning("Musisz wybrać jedną z opcji przed przejściem dalej!")
            else:
                # Sprawdzenie odpowiedzi
                if user_choice == current_q["answer"]:
                    st.session_state.score += 1
                else:
                    st.session_state.wrong_answers.append({
                        "question": current_q["question"],
                        "selected": user_choice,
                        "correct": current_q["answer"],
                        "tip": current_q["tip"]
                    })

                # Zmiana pytania na kolejne lub zakończenie quizu
                if q_idx + 1 < len(QUIZ_DATA):
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.quiz_complete = True
                    st.rerun()
