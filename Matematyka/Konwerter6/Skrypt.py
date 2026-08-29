import streamlit as st

# konfiguracja strony
st.set_page_config(page_title="Kalkulator Jednostek - Klasa 6", page_icon="📐")

st.title("📐 Szkolny Konwerter Jednostek - Klasa 6")
st.write("Wygodna aplikacja do nauki zamiany jednostek objętości, pojemności oraz pól powierzchni.")

# Funkcja pomocnicza do ładnego formatowania liczb po polsku
def formatuj_pl(wartosc, miejsca_po_przecinku=4):
    # Dynamicznie obcinamy zbędne zera na końcu dla czytelności dzieci
    format_str = f":,.{miejsca_po_przecinku}f"
    tekst = f"{{{format_str}}}".format(wartosc)
    # Zamiana formatu US (1,000.50) na PL (1 000,50)
    return tekst.replace(",", " TEMP ").replace(".", ",").replace(" TEMP ", " ")

# Sekcja Objętość i pojemność
st.header("💧 1. Objętość i Pojemność")

col1, col2 = st.columns(2)
with col1:
    wartosc_obj = st.number_input("Wpisz wartość do zmiany:", value=1.0, step=1.0, key="obj_val")
with col2:
    jednostka_obj = st.selectbox(
        "Wybierz jednostkę wyjściową:",
        ["l (litr)", "ml (mililitr)", "m³ (metr sześcienny)", "dm³ (decymetr sześcienny)",
         "cm³ (centymetr sześcienny)"],
        key="obj_unit"
    )

# Przeliczanie jednostek na litry - Bazowe
w_litrach = 0.0
if jednostka_obj == "l (litr)":
    w_litrach = wartosc_obj
elif jednostka_obj == "ml (mililitr)":
    w_litrach = wartosc_obj / 1000
elif jednostka_obj == "m³ (metr sześcienny)":
    w_litrach = wartosc_obj * 1000
elif jednostka_obj == "dm³ (decymetr sześcienny)":
    w_litrach = wartosc_obj
elif jednostka_obj == "cm³ (centymetr sześcienny)":
    w_litrach = wartosc_obj / 1000

# Wyświetlenie wynikow dla objętości
st.subheader("Wyniki zamiany:")
wynik_obj_tekst = f"""
* **{formatuj_pl(w_litrach * 1000, 2)}** ml
* **{formatuj_pl(w_litrach, 4)}** l
* **{formatuj_pl(w_litrach, 4)}** dm³
* **{formatuj_pl(w_litrach * 1000, 2)}** cm³
* **{formatuj_pl(w_litrach / 1000, 6)}** m³
"""
st.info(wynik_obj_tekst)

# Sekcja Pole Powierzchni
st.divider()
st.header("2. Pole Powierzchni")

col3, col4 = st.columns(2)
with col3:
    wartosc_pole = st.number_input("Wpisz wartość do zmiany:", value=1.0, step=1.0, key="pole_val")
with col4:
    jednostka_pole = st.selectbox(
        "Wybierz jednostkę wyjściową:",
        ["mm²", "cm²", "dm²", "m²", "a (ar)", "ha (hektar)"],
        key="pole_unit"
    )

# Baza to metry kwadratowe
w_metrach_kw = 0.0
if jednostka_pole == "mm²":
    w_metrach_kw = wartosc_pole / 1000000
elif jednostka_pole == "cm²":
    w_metrach_kw = wartosc_pole / 10000
elif jednostka_pole == "dm²":
    w_metrach_kw = wartosc_pole / 100
elif jednostka_pole == "m²":
    w_metrach_kw = wartosc_pole
elif jednostka_pole == "a (ar)":
    w_metrach_kw = wartosc_pole * 100
elif jednostka_pole == "ha (hektar)":
    w_metrach_kw = wartosc_pole * 10000

# Wyświetlanie wyników (precyzja do 8 miejsc dla ha i arów przy małych wartościach)
wynik_pole_tekst = f"""
* **{formatuj_pl(w_metrach_kw * 1000000, 2)}** mm²
* **{formatuj_pl(w_metrach_kw * 10000, 2)}** cm²
* **{formatuj_pl(w_metrach_kw * 100, 2)}** dm²
* **{formatuj_pl(w_metrach_kw, 4)}** m²
* **{formatuj_pl(w_metrach_kw / 100, 6)}** a (ary)
* **{formatuj_pl(w_metrach_kw / 10000, 8)}** ha (hektary)
"""
st.info(wynik_pole_tekst)

# Sekcja Ściąga
st.divider()
st.header("📝 Ściąga dla szóstoklasisty")

st.markdown(r"""
### 💧 Objętość i pojemność - pamiętaj !
* **$1\text{ l} = 1\text{ dm}^3$** (Karton mleka to kostka o boku 10 cm)
* **$1\text{ ml} = 1\text{ cm}^3$** (Mała kostka o boku 1 cm)
* **$1\text{ m}^3 = 1000\text{ l}$** (Wielki zbiornik wody)
""")

st.markdown("### 🔲 Pole powierzchni - pamiętaj!")
st.markdown("""
Gdy zamieniasz jednostki pola, **mnożysz zależności długości przez same siebie** 
(np. skoro $1\\text{ m} = 100\\text{ cm}$, to $1\\text{ m}^2 = 100 \\times 100 = 10\\ 000\\text{ cm}^2$).
""")

st.markdown(r"""
* $1\text{ cm}^2 = 100\text{ mm}^2$
* $1\text{ dm}^2 = 100\text{ cm}^2$
* $1\text{ m}^2 = 100\text{ dm}^2 = 10\ 000\text{ cm}^2$
* $1\text{ a (ar)} = 100\text{ m}^2$ *(Kwadrat o boku 10 m x 10 m)*
* $1\text{ ha (hektar)} = 100\text{ a} = 10\ 000\text{ m}^2$ *(Kwadrat o boku 100 m x 100 m)*
""")
