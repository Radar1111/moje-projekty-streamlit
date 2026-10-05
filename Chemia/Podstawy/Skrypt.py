import streamlit as st
import random

# Ustawienia strony
st.set_page_config(
    page_title="Chemia Klasa 7 - Podstawy",
    page_icon="🧪",
    layout="wide"
)

# Stylizacja CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        color: #2E4053;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 26px;
        color: #1F618D;
        border-bottom: 2px solid #1F618D;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .highlight-box {
        background-color: #EBF5FB;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
        margin-bottom: 15px;
    }
    .success-box {
        background-color: #EAF2F8;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧪 Mobilny Asystent Chemika – Klasa 7</div>', unsafe_allow_html=True)
st.write(
    "Witaj w aplikacji do nauki podstaw chemii! Wybierz dział z menu po lewej stronie, aby rozpocząć naukę i sprawdzić swoją wiedzę.")

# Menu boczne
st.sidebar.header("📚 Działy tematyczne")
page = st.sidebar.radio(
    "Wybierz temat:",
    [
        "1. Właściwości substancji",
        "2. Mieszaniny jednorodne i niejednorodne",
        "3. Metody rozdzielania mieszanin",
        "4. Zjawiska fizyczne a reakcje chemiczne",
        "🎓 Quiz sprawdzający"
    ]
)

# Baza pytań do quizu
questions_db = {
    "wlasciwości": [
        {"q": "Która z wymienionych cech jest właściwością chemiczną?",
         "o": ["Gęstość", "Zapach", "Palność", "Temperatura topnienia"], "a": "Palność"},
        {"q": "Jaką właściwością fizyczną charakteryzuje się większość metali?",
         "o": ["Są gazami", "Przewodzą prąd elektryczny", "Mają niską gęstość", "Są łatwopalne"],
         "a": "Przewodzą prąd elektryczny"}
    ],
    "mieszaniny": [
        {"q": "Przykładem mieszaniny jednorodnej (homogenicznej) jest:",
         "o": ["Woda z piaskiem", "Powietrze", "Sałatka warzywna", "Woda z olejem"], "a": "Powietrze"},
        {"q": "Mieszanina niejednorodna to taka, w której:", "o": ["Składników nie widać gołym okiem",
                                                                   "Składniki można rozróżnić gołym okiem lub za pomocą prostych przyrządów optycznych",
                                                                   "Składniki zawsze są gazami",
                                                                   "Składniki chemicznie się połączyły"],
         "a": "Składniki można rozróżnić gołym okiem lub za pomocą prostych przyrządów optycznych"}
    ],
    "rozdzielanie": [
        {"q": "Jaką metodą najlepiej rozdzielić mieszaninę wody i soli kuchennej?",
         "o": ["Sączenie (filtracja)", "Krystalizacja (odparowanie wody)", "Użycie rozdzielacza", "Dekantacja"],
         "a": "Krystalizacja (odparowanie wody)"},
        {"q": "Sączenie (filtrację) stosuje się do rozdzielenia:",
         "o": ["Cieczy o różnych temperaturach wrzenia", "Cieczy mieszających się ze sobą",
               "Ciała stałego nierozpuszczalnego w cieczy", "Dwóch gazów"],
         "a": "Ciała stałego nierozpuszczalnego w cieczy"}
    ],
    "zjawiska": [
        {"q": "Który proces jest zjawiskiem fizycznym?",
         "o": ["Spalanie węgla", "Kwaśnienie mleka", "Topnienie lodu", "Rdzewienie gwoździa"], "a": "Topnienie lodu"},
        {"q": "Główną cechą reakcji chemicznej jest to, że:", "o": ["Substancja zmienia tylko swój stan skupienia",
                                                                    "Powstaje nowa substancja o zupełnie innych właściwościach",
                                                                    "Składniki można łatwo rozdzielić mechanicznie",
                                                                    "Zmienia się tylko kształt substancji"],
         "a": "Powstaje nowa substancja o zupełnie innych właściwościach"}
    ]
}

# 1. Właściwości Substancji
if page == "1. Właściwości substancji":
    st.markdown('<div class="section-title">1. Właściwości fizyczne i chemiczne substancji</div>',
                unsafe_allow_html=True)

    st.write("""
    Każdą substancję możemy opisać za pomocą jej cech charakterystycznych, które nazywamy **właściwościami**. 
    Dzielimy je na dwie główne grupy:
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="highlight-box"><b>🔹 Właściwości fizyczne</b><br>Możemy je zbadać za pomocą zmysłów lub przyrządów, bez zmiany tożsamości chemicznej substancji.<ul><li>Stan skupienia (stały, ciekły, gazowy)</li><li>Barwa, połysk</li><li><b>Zapach i smak</b> (badane zmysłami)</li><li>Gęstość</li><li>Temperatura topnienia i wrzenia</li><li>Przewodnictwo elektryczne i cieplne</li><li>Rozpuszczalność w wodzie</li></ul></div>',
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<div class="highlight-box"><b>🔥 Właściwości chemiczne</b><br>Opisują zachowanie substancji w kontakcie z innymi substancjami lub energią. Wiążą się z jej reaktywnością.<ul><li>Palność (czy substancja się pali)</li><li>Toksyczność i szkodliwość</li><li>Aktywność chemiczna (np. reakcja z kwasami)</li><li>Skłonność do korozji (np. rdzewienie żelaza)</li><li>Zdolność do rozkładu pod wpływem temperatury</li></ul></div>',
            unsafe_allow_html=True)

    st.subheader("🧠 Szybki test wiedzy")
    q = questions_db["wlasciwości"][0]
    user_ans = st.radio(q["q"], q["o"], key="q1")
    if st.button("Sprawdź odpowiedź", key="b1"):
        if user_ans == q["a"]:
            st.success("Brawo! Poprawna odpowiedź.")
        else:
            st.error(f"Niestety nie. Poprawna odpowiedź to: {q['a']}")

# 2. Mieszaniny
elif page == "2. Mieszaniny jednorodne i niejednorodne":
    st.markdown('<div class="section-title">2. Mieszaniny jednorodne i niejednorodne</div>', unsafe_allow_html=True)

    st.write("""
    **Mieszanina** składa się z co najmniej dwóch różnych substancji zmieszanych ze sobą w dowolnym stosunku. 
    W mieszaninie składniki zachowują swoje właściwości.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="highlight-box"><b>🥛 Mieszaniny jednorodne (homogeniczne)</b><br>Składników nie można rozróżnić gołym okiem ani prostymi przyrządami optycznymi (np. lupą). Poukładane są na poziomie cząsteczkowym.<br><br><b>Przykłady:</b> Powietrze, solanka (woda z solą), stop metali (np. mosiądz), ocet.</div>',
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<div class="highlight-box"><b>🥗 Mieszaniny niejednorodne (heterogeniczne)</b><br>Składniki można łatwo rozróżnić gołym okiem lub za pomocą lupy/mikroskopu.<br><br><br><b>Przykłady:</b> Woda z piaskiem, sałatka, opiłki żelaza z siarką, granit, woda z olejem.</div>',
            unsafe_allow_html=True)

    st.subheader("🧠 Szybki test wiedzy")
    q = questions_db["mieszaniny"][0]
    user_ans = st.radio(q["q"], q["o"], key="q2")
    if st.button("Sprawdź odpowiedź", key="b2"):
        if user_ans == q["a"]:
            st.success("Świetnie! Masz rację.")
        else:
            st.error(f"Spróbuj ponownie. Poprawna odpowiedź to: {q['a']}")

# Metody rozdzielania
elif page == "3. Metody rozdzielania mieszanin":
    st.markdown('<div class="section-title">3. Metody rozdzielania mieszanin</div>', unsafe_allow_html=True)
    st.write(
        "Składniki mieszanin nie są ze sobą połączone chemicznie, dlatego można je rozdzielić za pomocą metod fizycznych:")

    methods = {
        "Sączenie (filtracja)": "Rozdzielanie ciała stałego nierozpuszczalnego w cieczy za pomocą sączka z bibuły (np. woda z piaskiem).",
        "Krystalizacja": "Wydzielanie kryształków substancji rozpuszczonej poprzez odparowanie rozpuszczalnika (np. uzyskiwanie soli z wody morskiej).",
        "Dekantacja": "Zlewanie cieczy znad osadu, który opadł na dno naczynia.",
        "Użycie rozdzielacza": "Stosowane do rozdzielania cieczy, które nie mieszają się ze sobą i mają różne gęstości (np. woda i olej).",
        "Destylacja": "Rozdzielanie składników mieszaniny ciekłej jednorodnej, wykorzystujące różnice w ich temperaturach wrzenia (np. woda i alkohol).",
        "Rozdzielanie mechaniczne / użycie magnesu": "Wydzielanie składników o różnych właściwościach magnetycznych (np. opiłki żelaza i siarka) lub ręczne sortowanie."
    }

    for method, desc in methods.items():
        st.markdown(f"**🔬 {method}** – {desc}")

    st.subheader("🧠 Szybki test wiedzy")
    q = questions_db["rozdzielanie"][0]
    user_ans = st.radio(q["q"], q["o"], key="q3")
    if st.button("Sprawdź odpowiedź", key="b3"):
        if user_ans == q["a"]:
            st.success("Doskonale! To prawidłowa metoda.")
        else:
            st.error(f"Błąd. Prawidłowa metoda to: {q['a']}")

# Zjawiska a reakcje
elif page == "4. Zjawiska fizyczne a reakcje chemiczne":
    st.markdown('<div class="section-title">4. Zjawiska fizyczne a reakcje chemiczne</div>', unsafe_allow_html=True)
    st.write("To jeden z najważniejszych podziałów w chemii. Decyduje o tym, czy powstaje zupełnie nowa substancja.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### 🧊 Zjawisko fizyczne')
        st.markdown(
            '<div class="highlight-box">Proces, w którym substancja zmienia swoje właściwości fizyczne (np. stan skupienia, kształt), ale <b>NIE POWSTAJE</b> nowa substancja.<br><br><b>Przykłady:</b><ul><li>Topnienie lodu, parowanie wody</li><li>Rozbicie szklanki</li><li>Mielenie pieprzu</li><li>Magnesowanie igły</li></ul></div>',
            unsafe_allow_html=True)
    with col2:
        st.markdown('### 🔥 Reakcja chemiczna')
        st.markdown(
            '<div class="highlight-box">Proces, w wyniku którego z jednych substancji (substratów) <b>POWSTAJĄ NOWE SUBSTANCJE</b> (produkty) o zupełnie innych właściwościach.<br><br><b>Przykłady:</b><ul><li>Spalanie drewna</li><li>Rdzewienie żelaza</li><li>Kwaśnienie mleka</li><li>Pieczenie ciasta</li></ul></div>',
            unsafe_allow_html=True)

    st.subheader("🧠 Szybki test wiedzy")
    q = questions_db["zjawiska"][0]
    user_ans = st.radio(q["q"], q["o"], key="q4")
    if st.button("Sprawdź odpowiedź", key="b4"):
        if user_ans == q["a"]:
            st.success("Wspaniale! Topnienie to tylko zmiana stanu skupienia.")
        else:
            st.error(f"Nieprawda. Prawidłowa odpowiedź to: {q['a']}")

    # 5. Quiz
elif page == "🎓 Quiz sprawdzający":
    st.markdown('🎓 Wielki Quiz z Chemii - Klasa 7', unsafe_allow_html=True)
    st.write("Odpowiedz na wszystkie pytania, aby sprawdzić, jak dobrze opanowałeś materiał!")

    all_questions = []
    for category in questions_db.values():
        all_questions.extend(category)

    user_choices = {}
    for i, item in enumerate(all_questions):
        st.markdown(f"Pytanie {i + 1}: {item['q']}")
        user_choices[i] = st.radio("Wybierz opcję:", item["o"], key=f"quiz_q_{i}")

    st.write("---")

    if st.button("📊 Oblicz mój wynik"):
        score = 0
        for i, item in enumerate(all_questions):
            if user_choices[i] == item["a"]:
                score += 1

        procent = (score / len(all_questions)) * 100
        st.metric(label="Twój wynik", value=f"{score} / {len(all_questions)}", delta=f"{procent:.0f}%")

        if procent == 100:
            st.balloons()
            st.success("Fenomenalnie! Jesteś mistrzem chemii siódmoklasisty! 🥇")
        elif procent >= 75:
            st.success("Bardzo dobry wynik! Masz świetne podstawy. 🥈")
        elif procent >= 50:
            st.warning("Dobrze, ale warto jeszcze raz przejrzeć materiał. 🥉")
        else:
            st.error("Musisz jeszcze trochę potrenować. Przeczytaj teorię w menu obok i spróbuj ponownie! 📚")
