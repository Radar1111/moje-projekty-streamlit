import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(page_title="Diagnoza z Fizyki - Klasa 7", page_icon="⚡")

# 2. Definicja 15 pytań z fizyki dla klasy 7
PHYSICS_QUIZ_DATA = [
    {
        "question": "Samochód porusza się z prędkością 72 km/h. Ile to metrów na sekundę (m/s)?",
        "options": ["7,2 m/s", "20 m/s", "36 m/s", "200 m/s"],
        "answer": "20 m/s",
        "tip": "Aby zamienić km/h na m/s, należy wartość podzielić przez 3,6 (ponieważ 72 / 3,6 = 20)."
    },
    {
        "question": "Które z poniższych zjawisk jest przykładem zjawiska fizycznego, a nie reakcji chemicznej?",
        "options": ["Spalanie drewna", "Topnienie lodu", "Rdzewienie żelaza", "Kwaśnienie mleka"],
        "answer": "Topnienie lodu",
        "tip": "W zjawisku fizycznym substancja zmienia stan skupienia lub kształt, ale nie powstaje nowa substancja."
    },
    {
        "question": "Kostka z metalu o masie 270 g ma objętość 100 cm³. Jaka jest gęstość tego metalu?",
        "options": ["0,37 g/cm³", "2,7 g/cm³", "27 g/cm³", "27000 g/cm³"],
        "answer": "2,7 g/cm³",
        "tip": "Wzór na gęstość to d = m / V. Podstawiając dane: 270 g / 100 cm³ = 2,7 g/cm³ (to gęstość aluminium)."
    },
    {
        "question": "Na ciało działają dwie siły o tym samym kierunku, ale przeciwnych zwrotach: F1 = 10 N w prawo i F2 = 4 N w lewo. Ile wynosi siła wypadkowa?",
        "options": ["14 N w prawo", "6 N w lewo", "6 N w prawo", "0 N"],
        "answer": "6 N w prawo",
        "tip": "Gdy siły mają przeciwne zwroty, ich wartości odejmujemy (10 N - 4 N = 6 N). Zwrot wypada w stronę większej siły."
    },
    {
        "question": "Która zasada dynamiki Newtona wyjaśnia, dlaczego pasażerowie lecą do przodu podczas gwałtownego hamowania autobusu?",
        "options": ["Pierwsza zasada (zasada bezwładności)", "Druga zasada (F = m * a)",
                    "Trzecia zasada (akcja-reakcja)", "Czwarta zasada"],
        "answer": "Pierwsza zasada (zasada bezwładności)",
        "tip": "Bezwładność to właściwość ciała polegająca na dążeniu do zachowania swojego stanu ruchu lub spoczynku."
    },
    {
        "question": "Jak zmieni się ciśnienie wywierane na podłogę, jeśli człowiek stanie na jednej nodze zamiast na dwóch?",
        "options": ["Zmniejszy się dwukrotnie", "Nie zmieni się", "Wzrośnie dwukrotnie", "Wzrośnie czterokrotnie"],
        "answer": "Wzrośnie dwukrotnie",
        "tip": "Wzór na ciśnienie to p = F / S. Zmniejszając powierzchnię (S) dwukrotnie, ciśnienie (p) rośnie dwukrotnie."
    },
    {
        "question": "O czym mówi Prawo Pascala?",
        "options": [
            "Na ciało zanurzone w cieczy działa siła wyporu",
            "Ciśnienie zewnętrzne przenosi się w cieczach i gazach równomiernie we wszystkich kierunkach",
            "Im głębiej, tym większe jest ciśnienie hydrostatyczne",
            "Ciało porusza się ruchem przyspieszonym pod wpływem stałej siły"
        ],
        "answer": "Ciśnienie zewnętrzne przenosi się w cieczach i gazach równomiernie we wszystkich kierunkach",
        "tip": "Prawo Pascala jest podstawą działania m.in. hamulców hydraulicznych i podnośników."
    },
    {
        "question": "Drewniany klockek pływa częściowo zanurzony w wodzie. Co możesz powiedzieć o sile wyporu (Fw) i sile ciężkości (Fc)?",
        "options": ["Fw > Fc", "Fw < Fc", "Fw = Fc", "Siła wyporu nie działa na ciała pływające"],
        "answer": "Fw = Fc",
        "tip": "Gdy ciało pływa (nie tonie i nie wypływa dalej), siła wyporu i siła ciężkości równoważą się."
    },
    {
        "question": "Uczeń podniósł plecak o masie 5 kg na wysokość 2 metrów. Jaką pracę mechaniczną wykonał? (Przyjmij g = 10 m/s²)",
        "options": ["10 J", "2,5 J", "50 J", "100 J"],
        "answer": "100 J",
        "tip": "Praca W = F * s. Najpierw liczymy siłę ciężkości plecaka: F = m * g = 5 kg * 10 m/s² = 50 N. Następnie W = 50 N * 2 m = 100 J."
    },
    {
        "question": "W jakim czasie urządzenie o mocy 200 W wykona pracę 600 J?",
        "options": ["3 sekundy", "1200 sekund", "0,33 sekundy", "30 sekund"],
        "answer": "3 sekundy",
        "tip": "Wzór na moc to P = W / t. Po przekształceniu czas wynosi t = W / P, czyli 600 J / 200 W = 3 s."
    },
    {
        "question": "Kamień rzucono pionowo w górę. Co dzieje się z jego energią podczas wznoszenia (pomijając opory powietrza)?",
        "options": [
            "Energia kinetyczna rośnie, a potencjalna maleje",
            "Energia kinetyczna maleje, a potencjalna rośnie",
            "Obie energie rosną",
            "Obie energie maleją"
        ],
        "answer": "Energia kinetyczna maleje, a potencjalna rośnie",
        "tip": "Kamień zwalnia (spada energia kinetyczna) i leci wyżej (rośnie energia potencjalna ciężkości)."
    },
    {
        "question": "Zero bezwzględne (0 Kelvinów) w skali Celsjusza wynosi w przybliżeniu:",
        "options": ["0 °C", "-100 °C", "-273 °C", "100 °C"],
        "answer": "-273 °C",
        "tip": "0 K to najniższa możliwa temperatura w przyrodzie, odpowiada ona -273,15 °C."
    },
    {
        "question": "Przekazywanie energii cieplnej, które polega na ruchu cieplejszych warstw cieczy lub gazu ku górze, to:",
        "options": ["Przewodnictwo cieplne", "Konwekcja", "Promieniowanie", "Sublimacja"],
        "answer": "Konwekcja",
        "tip": "Konwekcja to unoszenie ciepła, widoczne np. nad kaloryferem lub podczas gotowania wody."
    },
    {
        "question": "Co to jest ciepło właściwe substancji?",
        "options": [
            "Ilość ciepła potrzebna do stopienia 1 kg substancji",
            "Temperatura, w której substancja zaczyna wrzeć",
            "Ilość ciepła potrzebna do ogrzania 1 kg substancji o 1 stopień (1 °C lub 1 K)",
            "Ilość energii oddawana podczas skraplania"
        ],
        "answer": "Ilość ciepła potrzebna do ogrzania 1 kg substancji o 1 stopień (1 °C lub 1 K)",
        "tip": "Woda ma bardzo wysokie ciepło właściwe (ok. 4200 J/(kg*°C)), przez co długo się nagrzewa i długo stygnie."
    },
    {
        "question": "Jak nazywa się bezpośrednie przejście substancji ze stanu stałego w stan gazowy?",
        "options": ["Resublimacja", "Parowanie", "Sublimacja", "Kondensacja"],
        "answer": "Sublimacja",
        "tip": "Przykładem sublimacji jest ulatnianie się suchego lodu lub znikanie zamarzniętego prania na mrozie."
    }
]

# 3. Inicjalizacja Session State dla fizyki
if "phys_current_question" not in st.session_state:
    st.session_state.phys_current_question = 0
if "phys_score" not in st.session_state:
    st.session_state.phys_score = 0
if "phys_quiz_complete" not in st.session_state:
    st.session_state.phys_quiz_complete = False
if "phys_wrong_answers" not in st.session_state:
    st.session_state.phys_wrong_answers = []


# 4. Funkcja resetu
def restart_phys_quiz():
    st.session_state.phys_current_question = 0
    st.session_state.phys_score = 0
    st.session_state.phys_quiz_complete = False
    st.session_state.phys_wrong_answers = []


# INTERFEJS 

st.title("⚡ Quiz Diagnostyczny: Fizyka Klasa 7")
st.write("Rozwiąż test, aby sprawdzić, czy pamiętasz mechanikę, hydrostatykę i ciepło przed klasą 8!")

# Ekran podsumowania
if st.session_state.phys_quiz_complete:
    st.success(f"### 📊 Diagnoza zakończona! Wynik: {st.session_state.phys_score} / {len(PHYSICS_QUIZ_DATA)}")

    percentage = (st.session_state.score_phys / len(PHYSICS_QUIZ_DATA)) * 100 if "score_phys" in st.session_state else (
                                                                                                                                   st.session_state.phys_score / len(
                                                                                                                               PHYSICS_QUIZ_DATA)) * 100

    if percentage >= 80:
        st.balloons()
        st.write(
            "🚀 Genialnie! Świetnie radzisz sobie z jednostkami i wzorami. Klasa 8 z prądem i optyką będzie prosta!")
    elif percentage >= 50:
        st.write(
            "⚖️ Masz dobre podstawy, ale uważaj na zadania obliczeniowe. Warto powtórzyć wzory na pracę i ciśnienie.")
    else:
        st.error(
            "📉 Fizyka z klasy 7 wymaga powtórzenia. Bez opanowania pojęcia siły i ruchu trudno będzie zrozumieć elektromagnesy czy fale w klasie 8.")

    # Rekomendacje
    if st.session_state.phys_wrong_answers:
        st.write("#### 🔍 Co warto powtórzyć?")
        for wa in st.session_state.phys_wrong_answers:
            with st.expander(f"Zadanie: {wa['question']}"):
                st.write(f"❌ Wybrałeś: *{wa['selected']}*")
                st.write(f"✅ Poprawna odpowiedź: **{wa['correct']}**")
                st.info(f"💡 **Wyjaśnienie:** {wa['tip']}")

    st.button("Spróbuj ponownie", on_click=restart_phys_quiz, type="primary")

# Ekran pytań
else:
    q_idx = st.session_state.phys_current_question
    current_q = PHYSICS_QUIZ_DATA[q_idx]

    # Progress bar
    st.progress(q_idx / len(PHYSICS_QUIZ_DATA), text=f"Zadanie {q_idx + 1} z {len(PHYSICS_QUIZ_DATA)}")

    st.warning(f"### Zadanie {q_idx + 1}: {current_q['question']}")

    with st.form(key=f"phys_form_{q_idx}"):
        user_choice = st.radio("Wybierz odpowiedź:", current_q["options"], index=None)
        submit_btn = st.form_submit_button("Zapisz i przejdź dalej", type="primary")

        if submit_btn:
            if user_choice is None:
                st.error("Wybierz odpowiedź przed kliknięciem przycisku!")
            else:
                # Sprawdzanie
                if user_choice == current_q["answer"]:
                    st.session_state.phys_score += 1
                else:
                    st.session_state.phys_wrong_answers.append({
                        "question": current_q["question"],
                        "selected": user_choice,
                        "correct": current_q["answer"],
                        "tip": current_q["tip"]
                    })

                # Sterowanie pytaniami
                if q_idx + 1 < len(PHYSICS_QUIZ_DATA):
                    st.session_state.phys_current_question += 1
                    st.rerun()
                else:
                    st.session_state.phys_quiz_complete = True
                    st.rerun()
