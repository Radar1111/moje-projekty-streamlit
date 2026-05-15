import random
import streamlit as st

# Konfiguracja strony
st.set_page_config(
    page_title="Pro Trener Ortografii", page_icon="🏆", layout="centered"
)


# --- WCZYTYWANIE BAZY Z PLIKU TXT ---
def wczytaj_zadania(nazwa_pliku):
    zadania = {"latwy": [], "sredni": [], "trudny": []}
    try:
        with open(nazwa_pliku, "r", encoding="utf-8") as plik:
            for linia in plik:
                czesci = linia.strip().split(",")
                if len(czesci) == 3:
                    poziom, slowo, zdanie = czesci
                    poziom_clean = poziom.strip().lower()
                    if poziom_clean in zadania:
                        # Wymuszenie małych liter dla słowa zgodnie z układem w txt
                        zadania[poziom_clean].append(
                            (slowo.strip().lower(), zdanie.strip())
                        )
        return zadania
    except FileNotFoundError:
        st.error(f"❌ Błąd: Nie znaleziono pliku {nazwa_pliku}")
        return None
    except UnicodeDecodeError:
        st.error(
            "❌ Błąd kodowania: Upewnij się, że plik txt ma kodowanie UTF-8"
        )
        return None


# INICJALIZACJA STANU GRY
if "gra_uruchomiona" not in st.session_state:
    st.session_state.gra_uruchomiona = False
    st.session_state.wynik = 0
    st.session_state.zycia = 3
    st.session_state.numer_pytania = 0
    st.session_state.pytania = []
    st.session_state.feedback = None
    # Nowe zmienne do kontrolowania ekranu pokazującego poprawną odpowiedź
    st.session_state.pokazuj_wyjasnienie = False
    st.session_state.typ_bledu = None

st.title("🏆 Mistrz Ortografii")

# --- MENU GŁÓWNE ---
if not st.session_state.gra_uruchomiona:
    st.markdown("### Przygotuj się do nauki!")
    baza = wczytaj_zadania("ortografia.txt")

    if baza:
        poziom = st.selectbox(
            "Wybierz poziom trudności:", ["latwy", "sredni", "trudny"]
        )
        liczba_slow = st.selectbox("Wybierz liczbę słówek:", [5, 10, 20])

        st.warning(
            "⚠️ **Uwaga:** Ilość kropek w zdaniu nie odpowiada liczbie liter w"
            " słowie!"
        )

        if st.button("🚀 ROZPOCZNIJ GRĘ"):
            wybrane = baza[poziom]
            if wybrane:
                random.shuffle(wybrane)
                st.session_state.pytania = wybrane[:liczba_slow]
                st.session_state.gra_uruchomiona = True
                st.session_state.wynik = 0
                st.session_state.zycia = 3
                st.session_state.numer_pytania = 0
                st.session_state.poziom_nazwa = poziom
                st.session_state.feedback = None
                st.session_state.pokazuj_wyjasnienie = False
                st.rerun()
            else:
                st.error(
                    f"Poziom '{poziom}' nie zawiera żadnych słówek w pliku"
                    " txt."
                )

# --- EKRAN GRY ---
else:
    pytania = st.session_state.pytania
    idx = st.session_state.numer_pytania

    # Sprawdzenie warunków końca gry (tylko gdy nie czekamy na kliknięcie "Dalej")
    if (
        idx >= len(pytania) or st.session_state.zycia <= 0
    ) and not st.session_state.pokazuj_wyjasnienie:
        if st.session_state.zycia <= 0:
            st.snow()
            st.error(
                "💀 KONIEC GRY! Straciłeś wszystkie życia. Twój wynik:"
                f" {st.session_state.wynik} PKT"
            )
        else:
            st.balloons()
            st.success(
                f"🎊 GRATULACJE! Ukończyłeś poziom {st.session_state.poziom_nazwa}!"
            )
            st.write(
                f"Twój wynik końcowy: **{st.session_state.wynik} /"
                f" {len(pytania)}**"
            )

        if st.button("Zagraj ponownie"):
            st.session_state.gra_uruchomiona = False
            st.rerun()

    else:
        # Statystyki gry
        col1, col2, col3 = st.columns(3)
        col1.metric("⭐ Punkty (XP)", st.session_state.wynik)
        col2.metric("❤️ Życia", "❤️" * st.session_state.zycia)
        col3.metric(
            "Ostatnie",
            st.session_state.feedback if st.session_state.feedback else "-",
        )

        procent = idx / len(pytania)
        st.progress(procent)
        st.caption(f"Postęp: {idx} z {len(pytania)} zadań")

        # Pobranie aktywnego pytania
        poprawne_slowo, zdanie = pytania[idx]

        st.markdown("#### Uzupełnij luki w zdaniu:")
        ukryte_zdanie = zdanie.replace(poprawne_slowo, ".........")
        st.info(ukryte_zdanie)

        # Funkcja uruchamiana po zatwierdzeniu Enterem
        def sprawdz_odpowiedz():
            wpisane = st.session_state.wpisana_odpowiedz.strip().lower()
            poprawne = poprawne_slowo.lower()

            if wpisane == poprawne:
                st.session_state.wynik += 1
                st.session_state.feedback = "✅ Dobrze!"
                # Przy dobrej odpowiedzi od razu idziemy do kolejnego słowa
                st.session_state.numer_pytania += 1
            else:
                # --- LOGIKA BŁĘDU CZĘŚCIOWEGO (ó zamiast o) ---
                if poprawne.replace("ó", "o") == wpisane:
                    st.session_state.feedback = "⚠️ Blisko! (błąd ó/o)"
                    st.session_state.typ_bledu = "blisko"
                    st.session_state.pokazuj_wyjasnienie = True
                else:
                    # Całkowicie niepoprawna odpowiedź
                    st.session_state.zycia -= 1
                    st.session_state.feedback = "❌ Błąd"
                    st.session_state.typ_bledu = "zle"
                    st.session_state.pokazuj_wyjasnienie = True

        # TRYB 1: Wyświetlanie ekranu blokady z wyjaśnieniem błędu
        if st.session_state.pokazuj_wyjasnienie:
            if st.session_state.typ_bledu == "blisko":
                st.warning(
                    f"Prawie dobrze! Pamiętaj, że słowo **'{poprawne_slowo}'**"
                    " piszemy przez **ó**."
                )
            else:
                st.error(
                    "Niestety to zła odpowiedź. Poprawne słowo to:"
                    f" **{poprawne_slowo}**"
                )

            # Pełne zdanie z pogrubionym prawidłowym słowem w celach edukacyjnych
            zdanie_wyjasnione = zdanie.replace(
                poprawne_slowo, f"**{poprawne_slowo}**"
            )
            st.markdown(f"Poprawne zdanie: {zdanie_wyjasnione}")

            # Przycisk przejścia dalej resetuje stan blokady
            if st.button("Dalej ➡️"):
                st.session_state.pokazuj_wyjasnienie = False
                st.session_state.numer_pytania += 1
                st.rerun()

        # TRYB 2: Normalne wpisywanie odpowiedzi (gdy nie ma błędu)
        else:
            st.text_input(
                "Wpisz brakujące słowo:",
                key="wpisana_odpowiedz",
                on_change=sprawdz_odpowiedz,
            )

# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do ortografii - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
