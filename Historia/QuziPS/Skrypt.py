import streamlit as st
import json
import os

st.set_page_config(page_title="Historia: Akcja-Reakcja!", page_icon="🚀", layout="centered")


@st.cache_data
def wczytaj_pytanie():
    if os.path.exists('pytanie.json'):
        with open('pytanie.json', "r", encoding="utf-8") as f:
            return json.load(f)
    return []


baza_pytan = wczytaj_pytanie()

# Inicjalizacja stanu sesji
if "wybrana_klasa" not in st.session_state:
    st.session_state.wybrana_klasa = None
if "wybrana_kategoria" not in st.session_state:
    st.session_state.wybrana_kategoria = "Wszystkie"
if "nr_pytania" not in st.session_state:
    st.session_state.nr_pytania = 0

if "wynik" not in st.session_state:
    st.session_state.wynik = 0
if "wybrano" not in st.session_state:
    st.session_state.wybrano = None
if "sprawdzono" not in st.session_state:
    st.session_state.sprawdzono = False

# Tytuł
st.title("🚀 Quiz Historyczny: Akcja-Reakcja!")
st.markdown("### Odczarowujemy historię! Sprawdź, czy łączysz kropki i ogarniasz przyczyny oraz skutki wydarzeń. 🏛️")
st.markdown("---")

# Ekran startowy
if st.session_state.wybrana_klasa is None:
    st.write("### 🎮 Wybierz swój poziom rozgrywki:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏰 Klasa 4 (Legendy i Początki Polski)", use_container_width=True):
            st.session_state.wybrana_klasa = 4
            st.session_state.wybrana_kategoria = "Wszystkie"
            st.rerun()
    with col2:
        if st.button("🏛️ Klasa 5 (Starożytność i Średniowiecze)", use_container_width=True):
            st.session_state.wybrana_klasa = 5
            st.session_state.wybrana_kategoria = "Wszystkie"
            st.rerun()

    st.info(
        "💡 Quiz skupia się na związkach przyczyna-skutek. Zapomnij o nudnym wkuwaniu dat, tutaj liczy się logiczne myślenie!")

else:
    # 1. Filtrowanie bazy pod wyciągnięcia dostępnych kategorii
    pytania_klasy = [p for p in baza_pytan if p["klasa"] == st.session_state.wybrana_klasa]

    # Wyciąganie unikalnych kategorii dla tej klasy
    kategorie = sorted(list(set([p.get("kategoria", "Inne") for p in pytania_klasy])))
    opcje_kategorii = ["Wszystkie"] + kategorie

    # 2. PANEL BOCZNY (Sidebar)
    with st.sidebar:
        st.header("⚙️ Filtry rozgrywki")
        st.write(f"**Poziom:** Klasa {st.session_state.wybrana_klasa}")

        # Zmiana kategorii w selectboxie resetuje postęp
        wybór_kategorii = st.selectbox(
            "Wybierz kategorię tematyczną:",
            opcje_kategorii,
            index=opcje_kategorii.index(
                st.session_state.wybrana_kategoria) if st.session_state.wybrana_kategoria in opcje_kategorii else 0
        )

        if wybór_kategorii != st.session_state.wybrana_kategoria:
            st.session_state.wybrana_kategoria = wybór_kategorii
            st.session_state.nr_pytania = 0
            st.session_state.wynik = 0
            st.session_state.sprawdzono = False
            st.session_state.wybrano = None
            # Usuwanie flag punktowych starej kategorii
            for key in list(st.session_state.keys()):
                if key.startswith("punkt_dodany_"):
                    del st.session_state[key]
            st.rerun()

        st.markdown("---")
        if st.button("🔙 Zmień klasę (Menu główne)", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # 3. Filtrowanie pytań (Klasa + Kategoria)
    if st.session_state.wybrana_kategoria == "Wszystkie":
        pytanie_filtr = pytania_klasy
    else:
        pytanie_filtr = [p for p in pytania_klasy if p.get("kategoria", "Inne") == st.session_state.wybrana_kategoria]

    # Ekran gry / Wyników
    if not pytanie_filtr:
        st.error(
            f"Błąd: Brak pytań z kategorii '{st.session_state.wybrana_kategoria}' dla Klasy {st.session_state.wybrana_klasa}!")
        if st.button("Zresetuj filtr kategorii"):
            st.session_state.wybrana_kategoria = "Wszystkie"
            st.rerun()

    elif st.session_state.nr_pytania < len(pytanie_filtr):
        # Pobranie aktualnego pytania z przefiltrowanej listy
        q = pytanie_filtr[st.session_state.nr_pytania]

        # Pasek postępu dla wybranego poziomu
        progres = (st.session_state.nr_pytania) / len(pytanie_filtr)
        st.progress(progres,
                    text=f"Kat: {st.session_state.wybrana_kategoria} | Pytanie {st.session_state.nr_pytania + 1} z {len(pytanie_filtr)}")

        st.markdown(f"### 📌 Temat: {q['temat']}")
        if "kategoria" in q:
            st.caption(f"📂 Kategoria: {q['kategoria']}")
        st.info(q['pytanie'])

        # Sprawdzamy, czy w pytaniu istnieje słowniczek i czy nie jest pusty
        if "slownik" in q and q["slownik"]:
            with st.expander("📖 Słowniczek trudnych pojęć do tego zadania"):
                for slowo, definicja in q["slownik"].items():
                    st.markdown(f"**{slowo}** – {definicja}")

        # Pobranie i zatwierdzenie odpowiedzi
        with st.form(key=f"form_{st.session_state.nr_pytania}"):
            odpowiedz = st.radio("Wybierz właściwy skutek (reakcję):", q['opcje'], index=None)
            submit = st.form_submit_button(label="Zatwierdź odpowiedź 🎯")

            if submit:
                if odpowiedz is not None:
                    st.session_state.wybrano = q['opcje'].index(odpowiedz)
                    st.session_state.sprawdzono = True
                    st.rerun()
                else:
                    st.warning("Musisz zaznaczyć jedną z opcji!")

        # Walidacja i wyświetlanie wyników
        if st.session_state.sprawdzono:
            if st.session_state.wybrano == q['poprawna']:
                st.success("🔥 Bingo! Idealny strzał, system działa bezbłędnie")
                st.write(f"💡 {q['wyjasnienie']}")

                # Bezpieczne dodawanie punktu (tylko raz na pytanie)
                if f"punkt_dodany_{st.session_state.nr_pytania}" not in st.session_state:
                    st.session_state.wynik += 1
                    st.session_state[f"punkt_dodany_{st.session_state.nr_pytania}"] = True
            else:
                st.error("Pudło! Wykryto błąd w logice systemu")
                st.write(f"Prawidłowy skutek to: **{q['opcje'][q['poprawna']]}**")
                st.write(f"💡 {q['wyjasnienie']}")

            # Przycisk "Następne pytanie" pojawia się dopiero po sprawdzeniu odpowiedzi
            if st.button("Następne pytanie ➡", use_container_width=True):
                st.session_state.nr_pytania += 1
                st.session_state.sprawdzono = False
                st.session_state.wybrano = None
                st.rerun()

    # Ekran końcowy
    else:
        st.balloons()
        st.markdown("## 🎉 Runda skończona! Gra ukończona!")

        # Zabezpieczenie przed dzieleniem przez zero
        if len(pytanie_filtr) > 0:
            procent = int((st.session_state.wynik / len(pytanie_filtr)) * 100)
        else:
            procent = 0

        st.metric(
            label=f"Twój wynik (Kategoria: {st.session_state.wybrana_kategoria}):",
            value=f"{st.session_state.wynik} / {len(pytanie_filtr)}",
            delta=f"{procent}% poprawnych odpowiedzi"
        )

        if procent == 100:
            st.success("👑 Absolutne Wow! Jesteś legendarnym strategiem")
        elif procent >= 70:
            st.info("😎 Świetny wynik! Dobrze łączysz fakty. Twoja ocena z historii właśnie skoczyła o poziom w górę!")
        else:
            st.warning("🙃 No i niefart! Zróbmy mały reboot wiedzy i spróbujmy jeszcze raz.")

        if st.button("Zagraj jeszcze raz w tę kategorię 🔄", use_container_width=True):
            st.session_state.nr_pytania = 0
            st.session_state.wynik = 0
            st.session_state.sprawdzono = False
            st.session_state.wybrano = None
            for key in list(st.session_state.keys()):
                if key.startswith("punkt_dodany_"):
                    del st.session_state[key]
            st.rerun()
