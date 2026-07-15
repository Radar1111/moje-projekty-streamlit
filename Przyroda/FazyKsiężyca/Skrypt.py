import ephem
from datetime import datetime
import streamlit as st

# Ustawienia strony
st.set_page_config(page_title="Fazy Księżyca dla Dzieci", layout="centered")

st.title("☀️ Wizualizator Faz Księżyca 🌙")
st.write("Sprawdź aktualną fazę Księżyca lub wybierz dowolną datę z kalendarza!")

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

# Wybór daty
wybrana_data = st.date_input("Wybierz datę:", datetime.now().date())

# Konwersja daty do formatu ephem
date_str = wybrana_data.strftime("%Y/%m/%d")
ephem_date = ephem.Date(date_str)
moon = ephem.Moon(ephem_date)

# Obliczenia astronomiczne
oświetlenie = round(moon.phase, 1)  # Procent oświetlenia 0-100

# Obliczanie wieku księżyca
ostatni_now = ephem.previous_new_moon(ephem_date)
wiek_księżyca = round(ephem_date - ostatni_now, 1)


# Funkcja zwracająca nazwę, ikonę oraz dedykowaną ciekawostkę dla 4. klasy
def pobierz_szczegoly_fazy(procent, wiek):
    if wiek < 1.0 or wiek > 28.5:
        return (
            "Nów (New Moon)",
            "🌑",
            "Księżyc jest teraz między Ziemią a Słońcem. Jego oświetlona strona jest odwrócona od nas, dlatego jest dla nas zupełnie niewidoczny na niebie!",
        )
    elif wiek < 6.5:
        return (
            "Młody Księżyc (Waxing Crescent)",
            "🌒",
            "Księżyc zaczyna 'rosnąć' i przypomina cieniutki rogalik. Zwróć uwagę, że świeci jego prawa strona – wygląda wtedy trochę jak brzuszek litery 'D' jak 'Dobrze, rosnę'!",
        )
    elif wiek < 8.5:
        return (
            "Pierwsza Kwadra (First Quarter)",
            "🌓",
            "Minęła już jedna czwarta całej podróży Księżyca wokół Ziemie! Widzimy dokładnie połowę jego tarczy (tę po prawej stronie).",
        )
    elif wiek < 13.5:
        return (
            "Księżyc Dąży do Pełni (Waxing Gibbous)",
            "🌔",
            "Księżyc jest już prawie cały oświetlony! Taki kształt nazywamy 'wypukłym'. Zostało tylko kilka dni do pełni.",
        )
    elif wiek < 15.5:
        return (
            "Pełnia (Full Moon)",
            "🌕",
            "Ziemia znajduje się teraz dokładnie pomiędzy Słońcem a Księżycem. Cała tarcza odbija światło słoneczne i mocno świeci przez całą noc!",
        )
    elif wiek < 21.0:
        return (
            "Księżyc ubywający (Waning Gibbous)",
            "🌖",
            "Po pełni Księżyc zaczyna powoli 'znikać'. Cień zaczyna zasłaniać go od prawej strony, a oświetlona zostaje lewa część.",
        )
    elif wiek < 23.0:
        return (
            "Trzecia kwadra (Last Quarter)",
            "🌗",
            "Księżyc przebył już trzy czwarte swojej drogi. Ponownie widzimy tylko połowę tarczy, ale tym razem świeci jej lewa strona.",
        )
    else:
        return (
            "Stary Księżyc (Waning Crescent)",
            "🌘",
            "To już ostatnie dni cyklu. Księżyc wygląda jak cieniutki rogalik i przypomina literę 'C' jak 'Cofa się' lub 'Chudnie'. Niedługo znów zacznie się nów!",
        )


nazwa_fazy, ikona, ciekawostka = pobierz_szczegoly_fazy(
    oświetlenie, wiek_księżyca
)

# Wyświetlenie wyników
st.markdown(
    f"<h1 style='text-align: center; font-size: 120px; margin-bottom: 0;'>{ikona}</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<h2 style='text-align: center; color: #4F8BF9; margin-top: 0;'>{nazwa_fazy}</h2>",
    unsafe_allow_html=True,
)

# Ramka z ciekawostką edukacyjną
st.info(f"💡 **Kosmiczna ciekawostka:** {ciekawostka}")

st.write("---")

# Statystyki
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Oświetlona część tarczy", value=f"{oświetlenie}%"
    )  # Zamiast "Ile Księżyca świeci"
with col2:
    st.metric(label="Wiek Księżyca (dni od nowiu)", value=f"{wiek_księżyca} dni")

# Ważne wyjaśnienie przyrodnicze tuż pod metrykami
st.caption(
    "⚠️ **Ważne dla młodego przyrodnika:** Księżyc nie świeci własnym światłem! "
    "To, co widzimy na niebie, to część jego powierzchni, która w tym momencie odbija światło słoneczne."
)

st.write("---")

# Informacje o najbliższych zjawiskach
st.subheader("📅 Kiedy kolejne ważne zmiany na niebie?")

nastepny_now = ephem.next_new_moon(ephem_date).datetime().strftime("%d.%m.%Y")
nastepna_pelnia = ephem.next_full_moon(ephem_date).datetime().strftime("%d.%m.%Y")

st.write(f"🌑 **Najbliższy nów:** {nastepny_now}")
st.write(f"🌕 **Najbliższa pełnia:** {nastepna_pelnia}")

wyswietl_sekcje_wsparcia()

st.divider()
st.caption("Najcierpliwszy portal do przyrody - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
