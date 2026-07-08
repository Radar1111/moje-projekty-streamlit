import streamlit as st
import random

st.set_page_config(page_title="Szkolny Konwerter", page_icon="🎓")

# DANE 
# Odległość: baza to Milimetry (mm)
# Masa: baza to Gramy (g)
# Czas: baza to Sekundy (s)
# Pole powierzchni: baza to Milimetry kwadratowe (mm2)
data = {
    "Odległość 📏": {
        "Kilometry (km)": 1000000,
        "Metry (m)": 1000,
        "Decymetry (dm)": 100,
        "Centymetry (cm)": 10,
        "Milimetry (mm)": 1
    },
    "Pole powierzchni 📐": {
        "Kilometry kwadratowe (km²)": 1000000000000,
        "Hektary (ha)": 10000000000,
        "Ary (a)": 100000000,
        "Metry kwadratowe (m²)": 1000000,
        "Centymetry kwadratowe (cm²)": 100
    },
    "Masa ⚖️": {
        "Tony (t)": 1000000,
        "Kilogramy (kg)": 1000,
        "Dekagramy (dag)": 10,
        "Gramy (g)": 1
    },
    "Czas ⏰": {
        "Doba": 86400,
        "Godzina": 3600,
        "Minuta (min)": 60,
        "Sekunda (s)": 1
    }
}

# WSKAZÓWKI
wskazowki = {
    "Odległość 📏": "Pamiętaj: 1 km = 1000 m, a 1 cm = 10 mm. Przesuwaj przecinek w prawo przy mnożeniu!",
    "Pole powierzchni 📐": "Uważaj! Przy jednostkach kwadratowych zer przybywa dwa razy szybciej! 1 m² = 10 000 cm². Pamiętaj też: 1 ar to kwadrat 10m x 10m (100 m²), a 1 hektar to kwadrat 100m x 100m (10 000 m²).",
    "Masa ⚖️": "Ważne: 1 kg to 100 dag, a 1 dag to 10 g. Tona to aż 1000 kilogramów!",
    "Czas ⏰": "Uwaga! Czas przeliczamy przez 60 (minuty, sekundy), a nie przez 100!"
}

st.title("🎓 Super Konwerter Jednostek")

# SEKCJA KONWERTERA
kategoria = st.selectbox("Wybierz co chcesz zmierzyć:", list(data.keys()))

col1, col2 = st.columns(2)
with col1:
    # Format "%.4f" zapobiega ucinaniu widoku przez Streamlit i blokuje notację naukową (E)
    wartosc = st.number_input("Wpisz liczbę:", value=1.0, min_value=0.0, format="%.4f", step=0.0001)
    jednostki = list(data[kategoria].keys())
    z_jednostki = st.selectbox("Z:", jednostki)
with col2:
    na_jednostke = st.selectbox("Na:", jednostki)

# Logika konwersji
bazowa = wartosc * data[kategoria][z_jednostki]
wynik = bazowa / data[kategoria][na_jednostke]

# Bezpieczne formatowanie
wartosc_formatowana = f"{wartosc:.10f}".rstrip('0').rstrip('.') if '.' in f"{wartosc:.10f}" else f"{wartosc}"
wynik_formatowany = f"{wynik:.10f}".rstrip('0').rstrip('.') if '.' in f"{wynik:.10f}" else f"{wynik}"

# Zabezpieczenie na wypadek, gdyby po usunięciu zer nic nie zostało (np. dla liczby 0)
if wartosc_formatowana == "": wartosc_formatowana = "0"
if wynik_formatowany == "": wynik_formatowany = "0"

st.success(f"Wynik: **{wartosc_formatowana} {z_jednostki}** to dokładnie **{wynik_formatowany} {na_jednostke}**")

# Wyświetlanie wskazówki
st.info(f"💡 **Wskazówka:** {wskazowki[kategoria]}")

st.divider()

# PROSTY TEST
st.subheader("🧠 Szybki Quiz: Sprawdź się!")

if 'pytanie' not in st.session_state:
    st.session_state.pytanie = "Ile metrów ma 1 kilometr?"
    st.session_state.poprawna = "1000"
    st.session_state.odpowiedz_klucz = 0  # Do czyszczenia pola tekstowego

st.write(f"**Pytanie:** {st.session_state.pytanie}")

# Klucz dynamiczny
odpowiedz = st.text_input("Twoja odpowiedź (wpisz samą liczbę):", key=f"quiz_ans_{st.session_state.odpowiedz_klucz}")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    sprawdz = st.button("Sprawdź!")
with col_btn2:
    nowe_pytanie = st.button("Nowe pytanie 🔁")

if sprawdz:
    # .strip() usuwa przypadkowe spacje wpisane przez ucznia na klawiaturze
    if odpowiedz.strip() == st.session_state.poprawna:
        st.balloons()
        st.success("Brawo! Świetnie Ci idzie! 🎉")
    else:
        st.error("Spróbuj jeszcze raz! Podpowiedź: przeczytaj uważnie ściągawkę poniżej.")

if nowe_pytanie:
    pytania = [
        ("Ile centymetrów ma 1 metr?", "100"),
        ("Ile milimetrów ma 1 centymetr?", "10"),
        ("Ile metrów ma 1 kilometr?", "1000"),
        ("Ile metrów kwadratowych ma 1 ar?", "100"),
        ("Ile arów ma 1 hektar?", "100"),
        ("Ile metrów kwadratowych ma 1 hektar?", "10000"),
        ("Ile centymetrów kwadratowych ma 1 metr kwadratowy?", "10000"),
        ("Ile minut ma jedna godzina?", "60"),
        ("Ile godzin ma doba?", "24"),
        ("Ile minut ma kwadrans?", "15"),
        ("Ile gramów ma 1 dekagram?", "10"),
        ("Ile dekagramów ma 1 kilogram?", "100"),
        ("Ile kilogramów ma 1 tona?", "1000")
    ]
    p, o = random.choice(pytania)
    # Zapobiegamy wylosowaniu tego samego pytania dwa razy z rzędu
    while p == st.session_state.pytanie:
        p, o = random.choice(pytania)

    st.session_state.pytanie = p
    st.session_state.poprawna = o
    st.session_state.odpowiedz_klucz += 1  # Zmiana klucza automatycznie czyści pole tekstowe
    st.rerun()

st.divider()

# ŚCIĄGA
with st.expander("📝 Otwórz ściągę z jednostkami (do zeszytu!)"):
    st.write("Warto zapamiętać te zasady. Możesz je przepisać do zeszytu!")

    tab1, tab1_5, tab2, tab3 = st.tabs(["📏 Odległość", "📐 Pole powierzchni", "⚖️ Masa", "⏰ Czas"])

    with tab1:
        st.markdown("""
        - **1 km** = 1000 m
        - **1 m** = 100 cm = 10 dm
        - **1 dm** = 10 cm
        - **1 cm** = 10 mm
        """)

    with tab1_5:
        st.markdown("""
        - **1 cm²** = 100 mm²
        - **1 m²** = 10 000 cm²
        - **1 ar (a)** = 100 m² *(kwadrat o boku 10m x 10m)*
        - **1 hektar (ha)** = 100 a = 10 000 m² *(kwadrat o boku 100m x 100m)*
        - **1 km²** = 100 ha = 1 000 000 m²
        """)

    with tab2:
        st.markdown("""
        - **1 tona (t)** = 1000 kg
        - **1 kg** = 100 dag = 1000 g
        - **1 dag** = 10 g
        - **1 g** = 1000 mg
        """)

    with tab3:
        st.markdown("""
        - **1 doba** = 24 godziny
        - **1 godzina** = 60 minut
        - **1 minuta** = 60 sekund
        - **Kwadrans** = 15 minut
        """)

# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do matematyki")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
