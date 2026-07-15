import random
import streamlit as st

# Konfiguracja strony
st.set_page_config(
    page_title="Quiz Ortografiiczny Żorża", page_icon="🏆", layout="centered"
)

def wyswietl_sekcje_wsparcia():
    # Inicjalizacja sesji wewnątrz funkcji (bezpieczne dla każdej strony)
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"

    # Separator odcinający treść edukacyjną
    st.divider()

    # Expander na dole strony
    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"
            
            # Użycie unikalnego klucza w widgetach zapobiega konfliktom w Streamlit
            odpowiedz_rodzica = st.number_input(pytanie, step=1, value=0, key="footer_parent_input")

            if st.button("Zatwierdź", key="footer_parent_btn", use_container_width=True):
                poprawny_wynik = st.session_state.num1 + st.session_state.num2
                if odpowiedz_rodzica == poprawny_wynik:
                    st.session_state.parent_verified = True
                    st.rerun()
                else:
                    st.error("Nieprawidłowy wynik. Spróbuj ponownie!")
        else:
            st.success("Weryfikacja pomyślna!")
            st.markdown(
                """
                **Drogi Rodzicu / Starszy Uczniu!**  
                Tworzę te aplikacje z myślą o bezpiecznym i skutecznym rozwoju oraz nauce. 
                Udostępniam je całkowicie **za darmo i bez reklam**.
                
                Utrzymanie projektów wymaga jednak realnych kosztów i setek godzin pracy. 
                Jeśli aplikacja pomogła w nauce i chcesz wesprzeć rozwój kolejnych programów 
                – możesz postawić mi wirtualną kawę. Dziękuję!
                """
            )
            st.link_button("☕ Postaw wirtualną kawę", LINK_DO_KAWY, type="primary", use_container_width=True)
            
            if st.button("Zablokuj strefę", type="secondary", use_container_width=True, key="footer_lock_btn"):
                st.session_state.parent_verified = False
                st.session_state.num1 = random.randint(5, 15)
                st.session_state.num2 = random.randint(5, 15)
                st.rerun()

            st.caption(
            "**Informacja o wsparciu:** "
            "Wszelkie wpłaty realizowane za pośrednictwem platformy BuyCoffee.to mają charakter "
            "całkowicie dobrowolnego, bezinteresownego wsparcia (darowizny) na rzecz dalszego rozwoju "
            "i utrzymania portfolio bezpłatnych aplikacji. Wpłata nie wiąże się z zakupem żadnych "
            "cyfrowych towarów, usług ani dodatkowych funkcji w aplikacji."
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

wyswietl_sekcje_wsparcia()

# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do ortografii - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
