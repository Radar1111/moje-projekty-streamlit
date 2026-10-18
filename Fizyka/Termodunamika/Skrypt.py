import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(
    page_title="Termodynamika - Klasa 8",
    page_icon="🔥",
    layout="wide"
)

# Tytuł i opis
st.title("🔥 Termodynamika w Klasie 8")
st.markdown("""
Witamy w interaktywnej aplikacji do nauki termodynamiki! 
Wybierz interesujący Cię temat z menu po lewej stronie, aby odkryć tajniki energii, ciepła i stanów skupienia.
""")

# Pasek boczny 
st.sidebar.header("🗺️ Menu Lekcji")
podrozdzial = st.sidebar.radio(
    "Wybierz temat:",
    [
        "1. Temperatura a Energia Wewnętrzna",
        "2. Sposoby Przepływu Ciepła",
        "3. Ciepło Właściwe (Kalkulator)",
        "4. Zmiany Stanów Skupienia",
        "5. Quiz Sprawdzający"
    ]
)

# 1: TEMPERATURA A ENERGIA WEWNĘTRZNA 
if podrozdzial == "1. Temperatura a Energia Wewnętrzna":
    st.header("🌡️ 1. Temperatura a Energia Wewnętrzna")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Co to jest Energia Wewnętrzna?")
        st.write("""
        Wszystkie ciała zbudowane są z drobin (atomów lub cząsteczek), które znajdują się w ciągłym, chaotycznym ruchu.

        **Energia wewnętrzna** to suma energii kinetycznej wszystkich drobin, z których zbudowane jest ciało, oraz energii potencjalnej związanej z ich wzajemnym oddziaływaniem.
        """)

        st.subheader("Czym jest Temperatura?")
        st.write("""
        **Temperatura** jest miarą średniej energii kinetycznej drobin tworzących dany układ. 
        * **Wyższa temperatura** = szybszy ruch cząsteczek.
        * **Niższa temperatura** = wolniejszy ruch cząsteczek.
        """)

    with col2:
        st.info(
            "💡 **Wirtualny eksperyment:** Zmień temperaturę suwakiem poniżej i zobacz, jak zachowują się cząsteczki!")
        temp_slider = st.slider("Temperatura układu (°C)", min_value=-50, max_value=150, value=20)

        if temp_slider < 0:
            st.error(
                "❄️ **Stan stały (Lód):** Cząsteczki poruszają się bardzo wolno, jedynie drgają wokół swoich położeń równowagi. Energia wewnętrzna jest niska.")
        elif 0 <= temp_slider < 100:
            st.warning(
                "💧 **Stan ciekły (Woda):** Cząsteczki poruszają się szybciej, mogą się swobodnie przemieszczać. Energia wewnętrzna wzrasta.")
        else:
            st.success(
                "💨 **Stan gazowy (Para wodna):** Cząsteczki poruszają się z ogromną prędkością, zderzając się ze sobą. Energia wewnętrzna jest bardzo wysoka!")

# 2: SPOSOBY PRZEPŁYWU CIEPŁA 
elif podrozdzial == "2. Sposoby Przepływu Ciepła":
    st.header("🔄 2. Sposoby Przepływu Ciepła")
    st.write(
        "Ciepło samorzutnie przepływa zawsze od ciała o **wyższej** temperaturze do ciała o **niższej** temperaturze. Wyróżniamy 3 główne mechanizmy:")

    tab1, tab2, tab3 = st.tabs(["🤝 Przewodnictwo", "🌪️ Konwekcja", "☀️ Promieniowanie"])

    with tab1:
        st.subheader("Przewodnictwo cieplne")
        st.write("""
        Polega na przekazywaniu energii kinetycznej zderzających się drobin bez transportu materii. Jest charakterystyczne dla **ciał stałych** (szczególnie metali).
        * **Dobrzy przewodnicy:** miedź, aluminium, żelazo.
        * **Izolatory (źli przewodnicy):** drewno, styropian, powietrze.
        """)
        st.image("https://unsplash.com", caption="Metalowy garnek szybko przewodzi ciepło do potrawy", width=400)

    with tab2:
        st.subheader("Konwekcja")
        st.write("""
        Polega na przenoszeniu ciepła wraz z **ruchem materii** (cieczy lub gazu). Wynika z różnicy gęstości – ciepła ciecz/gaz unosi się do góry (jest lżejsza), a chłodna opada na dół.
        * **Przykłady:** ogrzewanie pokoju przez kaloryfer, prądy morskie, gotowanie wody.
        """)

    with tab3:
        st.subheader("Promieniowanie")
        st.write("""
        Przekazywanie energii za pomocą fal elektromagnetycznych (promieniowanie podczerwone). **Nie wymaga obecności ośrodka** (może zachodzić w próżni).
        * **Przykłady:** Ciepło docierające ze Słońca na Ziemię, ciepło odczuwane przy ognisku.
        """)

# 3: CIEPŁO WŁAŚCIWE 
elif podrozdzial == "3. Ciepło Właściwe (Kalkulator)":
    st.header("🧮 3. Ciepło Właściwe")
    st.write("""
    **Ciepło właściwe ($c$)** to ilość ciepła potrzebna do podniesienia temperatury $1\text{ kg}$ danej substancji o $1^\circ\text{C}$ (lub $1\text{ K}$).

    Wzór na ilość dostarczonego/oddanego ciepła:
    $$Q = m \cdot c \cdot \Delta T$$
    Gdzie:
    * $Q$ – ilość ciepła [J]
    * $m$ – masa substancji [kg]
    * $c$ – ciepło właściwe [J/(kg·°C)]
    * $\Delta T$ – zmiana temperatury [°C]
    """)

    st.subheader("📊 Interaktywny Kalkulator Ciepła")

    substancje = {
        "Woda (bardzo duże ciepło właściwe!)": 4200,
        "Lód": 2100,
        "Aluminium": 900,
        "Żelazo": 450,
        "Miedź": 380
    }

    wybrana_substancja = st.selectbox("Wybierz substancję:", list(substancje.keys()))
    c = substancje[wybrana_substancja]

    m = st.number_input("Masa substancji (kg):", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
    delta_t = st.number_input("O ile stopni chcesz zmienić temperaturę (°C):", min_value=1.0, max_value=200.0,
                              value=10.0, step=1.0)

    wynik_q = m * c * delta_t

    st.metric(label=f"Potrzebne ciepło (Q) dla {wybrana_substancja}:", value=f"{wynik_q:,.2f} J")
    st.info(f"Wartość ciepła właściwego dla tej substancji wynosi: **{c} J/(kg·°C)**")

# 4: ZMIANY STANÓW SKUPIENIA 
elif podrozdzial == "4. Zmiany Stanów Skupienia":
    st.header("💧 4. Zmiany Stanów Skupienia")
    st.write("Dostarczanie lub odbieranie ciepła może prowadzić do zmiany stanu skupienia substancji:")

    st.markdown("""
    * **Topnienie:** stan stały ➡️ stan ciekły *(wymaga dostarczenia ciepła)*
    * **Krzepnięcie:** stan ciekły ➡️ stan stały *(ciepło jest oddawane)*
    * **Parowanie:** stan ciekły ➡️ stan gazowy *(wymaga dostarczenia ciepła)*
    * **Skraplanie:** stan gazowy ➡️ stan ciekły *(ciepło jest oddawane)*
    * **Sublimacja:** stan stały ➡️ stan gazowy *(wymaga dostarczenia ciepła)*
    * **Resublimacja:** stan gazowy ➡️ stan stały *(ciepło jest oddawane)*
    """)

    st.subheader("📈 Wykres zmian stanów skupienia wody")
    st.write(
        "Zauważ, że podczas samego procesu topnienia lub wrzenia, **temperatura substancji nie zmienia się**, dopóki cała substancja nie zmieni stanu skupienia!")

    # Prosty wykres pokazujący fazy ogrzewania wody
    fazy_wody = pd.DataFrame({
        "Dostarczone ciepło (oś czasu)": [1, 2, 3, 4, 5, 6, 7],
        "Temperatura (°C)": [-10, 0, 0, 50, 100, 100, 120],
        "Stan / Proces": ["Ogrzewanie lodu", "Topnienie lodu", "Topnienie lodu", "Ogrzewanie wody", "Wrzenie wody",
                          "Wrzenie wody", "Ogrzewanie pary"]
    })
    st.line_chart(data=fazy_wody, x="Dostarczone ciepło (oś czasu)", y="Temperatura (°C)")

# 5: QUIZ 
elif podrozdzial == "5. Quiz Sprawdzający":
    st.header("🧠 5. Szybki Quiz")
    st.write("Sprawdź swoją wiedzę z dzisiejszej lekcji!")

    punkty = 0

    # Pytanie 1
    q1 = st.radio(
        "1. Jak nazywa się sposób przekazywania ciepła, który nie wymaga obecności cząsteczek (może zachodzić w próżni)?",
        ["Przewodnictwo", "Konwekcja", "Promieniowanie"]
    )
    if q1 == "Promieniowanie":
        punkty += 1

    # Pytanie 2
    q2 = st.radio(
        "2. Co dzieje się z temperaturą wody podczas jej wrzenia?",
        ["Rośnie", "Maleje", "Jest stała i wynosi 100°C (przy ciśnieniu normalnym)"]
    )
    if q2 == "Jest stała i wynosi 100°C (przy ciśnieniu normalnym)":
        punkty += 1

    # Pytanie 3
    q3 = st.radio(
        "3. Przejście substancji bezpośrednio ze stanu stałego w stan gazowy to:",
        ["Sublimacja", "Resublimacja", "Skraplanie"]
    )
    if q3 == "Sublimacja":
        punkty += 1

    # Przycisk sprawdzający wynik
    if st.button("Sprawdź mój wynik! 🎯"):
        st.write(f"Twój wynik to: **{punkty} / 3**")
        if punkty == 3:
            st.balloons()
            st.success("Doskonale! Jesteś mistrzem termodynamiki! 🥇")
        elif punkty == 2:
            st.warning("Dobre rezultaty! Przejrzyj jeszcze raz materiał, w którym pojawił się błąd. 📝")
        else:
            st.error(
                "Spróbuj przeczytać lekcje jeszcze raz i podejść do quizu ponownie! Pouczysz się i na pewno pójdzie lepiej. 💪")
