import streamlit as st
import json
import os
import random
from huggingface_hub import hf_hub_download

# 1. KONFIGURACJA HUGGING FACE
REPO_ID = "Radar1111/FolderLektur" 


HF_TOKEN = st.secrets["HF_TOKEN"]


def wczytaj_json(nazwa_pliku):
    # Dodajemy .json jeśli nazwa go nie posiada
    if not nazwa_pliku.endswith('.json'):
        nazwa_pliku += '.json'
    
    # Pobieramy plik z prywatnego repozytorium Hugging Face
    cached_file_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=nazwa_pliku,
        repo_type="dataset",
        token=HF_TOKEN
    )
    
    # Wczytujemy pobrany plik JSON
    with open(cached_file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 2. USTAWIENIA STRONY
st.set_page_config(page_title="Quiz Master Lektur", layout="centered")

# Sprawdzenie czy folder istnieje (bez automatycznego tworzenia)
if not os.path.exists(SCIEZKA_LEKTUR):
    st.error(f"❌ Nie znaleziono folderu: '{NAZWA_FOLDERU}'")
    st.info(f"Stwórz folder o tej nazwie w: {BASE_DIR}")
    st.stop()

# Pobieranie listy plików JSON
pliki_json = [f for f in os.listdir(SCIEZKA_LEKTUR) if f.endswith(".json")]
tytuly_lektur = [f.replace(".json", "") for f in pliki_json]

if not tytuly_lektur:
    st.warning(f"Folder '{NAZWA_FOLDERU}' jest pusty. Wrzuć tam pliki .json")
    st.stop()

# 3. MODYFIKACJA W PANELU BOCZNYM
with st.sidebar:
    st.title("📚 Biblioteka Lektur")
    tytuly_lektur.sort()

    st.markdown("---")
    st.write("🔍 **Wyszukaj lekturę:**")
    wybrany_tytul = st.selectbox(
        "Zacznij wpisywać nazwę...",
        options=tytuly_lektur,
        index=0
    )

    st.divider()

    # Wybór długości quizu dopasowany do ucznia
    st.write("🎯 **Ustawienia quizu:**")
    liczba_pytan = st.selectbox(
        "Ile pytań chcesz wylosować?",
        options=[5, 10, 15, 20],
        index=1,  # Domyślnie zaznaczone 10 pytań
        help="Wybierz, jak długi ma być Twój quiz"
    )

# 4. LOGIKA QUIZU
if (
        "aktualna_lektura" not in st.session_state
        or st.session_state.aktualna_lektura != wybrany_tytul
        or st.session_state.get("wybrana_liczba_pytan") != liczba_pytan
):
    dane = wczytaj_json(wybrany_tytul)
    wszystkie_pytania = dane["pytania"]

    # Mieszamy bazę pytań
    random.shuffle(wszystkie_pytania)

    # Bierzemy tylko tyle pytań, ile wybrał uczeń
    st.session_state.pytania = wszystkie_pytania[:liczba_pytan]

    # Resetowanie stanów quizu
    st.session_state.numer_pytania = 0
    st.session_state.wynik = 0
    st.session_state.zakonczono = False
    st.session_state.aktualna_lektura = wybrany_tytul
    st.session_state.wybrana_liczba_pytan = liczba_pytan

    # Czyszczenie starych odpowiedzi z poprzedniej sesji
    for klucz in list(st.session_state.keys()):
        if klucz.startswith("odpowiedziane_") or klucz.startswith("wybor_"):
            del st.session_state[klucz]

# 5. WYŚWIETLANIE PYTAŃ
st.title(f"📖 Quiz: {wybrany_tytul}")

if not st.session_state.zakonczono:
    nr = st.session_state.numer_pytania
    p = st.session_state.pytania[nr]

    # Pasek postępu
    postep = nr / len(st.session_state.pytania)
    st.progress(postep, text=f"Pytanie {nr + 1} z {len(st.session_state.pytania)}")

    st.markdown(f"### {p['pytanie']}")

    # Mapowanie opcji
    opcje_do_wyboru = {f"A: {p['A']}": "A", f"B: {p['B']}": "B", f"C: {p['C']}": "C"}
    if "D" in p and p["D"]:
        opcje_do_wyboru[f"D: {p['D']}"] = "D"

    # Zmienna pomocnicza do blokowania radia po odpowiedzi
    czy_odpowiedziano = f"odpowiedziane_{nr}_{wybrany_tytul}" in st.session_state

    # 1. FORMULARZ wybór i zatwierdzenie odpowiedzi
    with st.form(key=f"form_{nr}_{wybrany_tytul}"):
        wybrana_etykieta = st.radio("Zaznacz odpowiedź:", list(opcje_do_wyboru.keys()), disabled=czy_odpowiedziano)
        zatwierdz = st.form_submit_button("Sprawdź odpowiedź", disabled=czy_odpowiedziano)

        if zatwierdz and not czy_odpowiedziano:
            wybrana_litera = opcje_do_wyboru[wybrana_etykieta]
            poprawna_litera = p["poprawna"]
            st.session_state[f"odpowiedziane_{nr}_{wybrany_tytul}"] = True
            st.session_state[f"wybor_{nr}"] = wybrana_litera

            if wybrana_litera == poprawna_litera:
                st.session_state.wynik += 1
            st.rerun()

    # 2. Wyświetla wynik i przycisk dalej
    if czy_odpowiedziano:
        wybrana_litera = st.session_state[f"wybor_{nr}"]
        poprawna_litera = p["poprawna"]

        if wybrana_litera == poprawna_litera:
            st.success(f"✨ Poprawnie! Odpowiedź {poprawna_litera}: {p[poprawna_litera]}")
        else:
            st.error(f"❌ Błąd! Twoja odpowiedź to {wybrana_litera}. Poprawna odpowiedź to {poprawna_litera}: {p[poprawna_litera]}")

        if st.button("Następne pytanie ➔"):
            if nr + 1 < len(st.session_state.pytania):
                st.session_state.numer_pytania += 1
            else:
                st.session_state.zakonczono = True
            st.rerun()

else:
    # 6. EKRAN KOŃCOWY
    st.balloons()
    st.success("🎉 Gratulacje! Quiz zakończony.")

    c1, c2 = st.columns(2)
    c1.metric("Wynik", f"{st.session_state.wynik} / {len(st.session_state.pytania)}")
    skutecznosc = int((st.session_state.wynik / len(st.session_state.pytania)) * 100)
    c2.metric("Skuteczność", f"{skutecznosc}%")

    if st.button("🔄 Zagraj jeszcze raz"):
        st.session_state.aktualna_lektura = None
        st.rerun()

st.divider()
st.caption("Najcierpliwszy portal do polskiego")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")


# 2. USTAWIENIA STRONY
st.set_page_config(page_title="Quiz Master Lektur", layout="centered")

# Sprawdzenie czy folder istnieje (bez automatycznego tworzenia)
if not os.path.exists(SCIEZKA_LEKTUR):
    st.error(f"❌ Nie znaleziono folderu: '{NAZWA_FOLDERU}'")
    st.info(f"Stwórz folder o tej nazwie w: {BASE_DIR}")
    st.stop()

# Pobieranie listy plików JSON
pliki_json = [f for f in os.listdir(SCIEZKA_LEKTUR) if f.endswith(".json")]
tytuly_lektur = [f.replace(".json", "") for f in pliki_json]

if not tytuly_lektur:
    st.warning(f"Folder '{NAZWA_FOLDERU}' jest pusty. Wrzuć tam pliki .json")
    st.stop()

# 3. MODYFIKACJA W PANELU BOCZNYM
with st.sidebar:
    st.title("📚 Biblioteka Lektur")
    tytuly_lektur.sort()

    st.markdown("---")
    st.write("🔍 **Wyszukaj lekturę:**")
    wybrany_tytul = st.selectbox(
        "Zacznij wpisywać nazwę...",
        options=tytuly_lektur,
        index=0
    )

    st.divider()

    # Wybór długości quizu dopasowany do ucznia
    st.write("🎯 **Ustawienia quizu:**")
    liczba_pytan = st.selectbox(
        "Ile pytań chcesz wylosować?",
        options=[5, 10, 15, 20],
        index=1,  # Domyślnie zaznaczone 10 pytań
        help="Wybierz, jak długi ma być Twój quiz"
    )

# 4. LOGIKA QUIZU
if (
        "aktualna_lektura" not in st.session_state
        or st.session_state.aktualna_lektura != wybrany_tytul
        or st.session_state.get("wybrana_liczba_pytan") != liczba_pytan
):
    dane = wczytaj_json(wybrany_tytul)
    wszystkie_pytania = dane["pytania"]

    # Mieszamy bazę pytań
    random.shuffle(wszystkie_pytania)

    # Bierzemy tylko tyle pytań, ile wybrał uczeń
    st.session_state.pytania = wszystkie_pytania[:liczba_pytan]

    # Resetowanie stanów quizu
    st.session_state.numer_pytania = 0
    st.session_state.wynik = 0
    st.session_state.zakonczono = False
    st.session_state.aktualna_lektura = wybrany_tytul
    st.session_state.wybrana_liczba_pytan = liczba_pytan

    # Czyszczenie starych odpowiedzi z poprzedniej sesji
    for klucz in list(st.session_state.keys()):
        if klucz.startswith("odpowiedziane_") or klucz.startswith("wybor_"):
            del st.session_state[klucz]

# 5. WYŚWIETLANIE PYTAŃ
st.title(f"📖 Quiz: {wybrany_tytul}")

if not st.session_state.zakonczono:
    nr = st.session_state.numer_pytania
    p = st.session_state.pytania[nr]

    # Pasek postępu
    postep = nr / len(st.session_state.pytania)
    st.progress(postep, text=f"Pytanie {nr + 1} z {len(st.session_state.pytania)}")

    st.markdown(f"### {p['pytanie']}")

    # Mapowanie opcji
    opcje_do_wyboru = {f"A: {p['A']}": "A", f"B: {p['B']}": "B", f"C: {p['C']}": "C"}
    if "D" in p and p["D"]:
        opcje_do_wyboru[f"D: {p['D']}"] = "D"

    # Zmienna pomocnicza do blokowania radia po odpowiedzi
    czy_odpowiedziano = f"odpowiedziane_{nr}_{wybrany_tytul}" in st.session_state

    # 1. FORMULARZ wybór i zatwierdzenie odpowiedzi
    with st.form(key=f"form_{nr}_{wybrany_tytul}"):
        wybrana_etykieta = st.radio("Zaznacz odpowiedź:", list(opcje_do_wyboru.keys()), disabled=czy_odpowiedziano)
        zatwierdz = st.form_submit_button("Sprawdź odpowiedź", disabled=czy_odpowiedziano)

        if zatwierdz and not czy_odpowiedziano:
            wybrana_litera = opcje_do_wyboru[wybrana_etykieta]
            poprawna_litera = p["poprawna"]
            st.session_state[f"odpowiedziane_{nr}_{wybrany_tytul}"] = True
            st.session_state[f"wybor_{nr}"] = wybrana_litera

            if wybrana_litera == poprawna_litera:
                st.session_state.wynik += 1
            st.rerun()

    # 2. Wyświetla wynik i przycisk dalej
    if czy_odpowiedziano:
        wybrana_litera = st.session_state[f"wybor_{nr}"]
        poprawna_litera = p["poprawna"]

        if wybrana_litera == poprawna_litera:
            st.success(f"✨ Poprawnie! Odpowiedź {poprawna_litera}: {p[poprawna_litera]}")
        else:
            st.error(f"❌ Błąd! Twoja odpowiedź to {wybrana_litera}. Poprawna odpowiedź to {poprawna_litera}: {p[poprawna_litera]}")

        if st.button("Następne pytanie ➔"):
            if nr + 1 < len(st.session_state.pytania):
                st.session_state.numer_pytania += 1
            else:
                st.session_state.zakonczono = True
            st.rerun()

else:
    # 6. EKRAN KOŃCOWY
    st.balloons()
    st.success("🎉 Gratulacje! Quiz zakończony.")

    c1, c2 = st.columns(2)
    c1.metric("Wynik", f"{st.session_state.wynik} / {len(st.session_state.pytania)}")
    skutecznosc = int((st.session_state.wynik / len(st.session_state.pytania)) * 100)
    c2.metric("Skuteczność", f"{skutecznosc}%")

    if st.button("🔄 Zagraj jeszcze raz"):
        st.session_state.aktualna_lektura = None
        st.rerun()

st.divider()
st.caption("Najcierpliwszy portal do polskiego")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
