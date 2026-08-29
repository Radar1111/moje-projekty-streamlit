import streamlit as st
import json
import random
import time
import requests
# Dodano brakujący import do pobierania plików z Hugging Face
from huggingface_hub import hf_hub_download

# Konfiguracja strony Streamlit
st.set_page_config(page_title="Inteligentny Arkusz Diagnostyczny E8", layout="centered")

# Główny tytuł aplikacji
st.title("🎯 Inteligentny Arkusz Diagnostyczny")

# Podtytuł wyjaśniający źródło zadań oraz działanie systemu
st.subheader("Oparty na oficjalnych zadaniach CKE")
st.write("Rozwiąż zadania, a system przeanalizuje, które poddziały musisz jeszcze powtórzyć!")


# 1. Wczytywanie bazy danych z pliku JSON
@st.cache_data
def load_app_data():
    """Wczytuje kompletną bazę słów z prywatnego pliku JSON na Hugging Face."""
    
    REPO_ID = "Radar1111/E8" 
    FILENAME = "baza_zadan.json"
    
    try:
        # Pobieranie tokenu 
        if "HF_TOKEN" not in st.secrets:
            st.sidebar.error("Błąd: Brak klucza HF_TOKEN w zakładce Secrets Streamlita!")
            return []
            
        token = st.secrets["HF_TOKEN"]
        
        # Bezpieczne pobranie pliku z Hugging Face 
        local_file_path = hf_hub_download(
            repo_id=REPO_ID, 
            filename=FILENAME, 
            token=token,
            repo_type="dataset" 
        )
        
        # 3. Wczytanie pobranego pliku JSON
        with open(local_file_path, "r", encoding="utf-8") as f:
            words = json.load(f)
        return words

    except Exception as e:
        st.sidebar.error(f"Szczegóły błędu połączenia z HF: {e}")
        
        # POPRAWKA: Awaryjna baza danych musi być zwrócona TUTAJ, 
        # zamiast pustej listy 'return []', aby aplikacja mogła działać lokalnie bez HF.
        return [
            {
                "id_zadania": "cke_mat_01",
                "poddzial": "Działania na potęgach",
                "tresc": "Oblicz wartość wyrażenia: 2^3 * 2^2. Wynik to:",
                "opcje": ["16", "32", "64", "128"],
                "poprawna": "32",
                "punkty_max": 1,
                "wyjasnienie": "W tym zadaniu korzystamy z reguły mnożenia potęg o tych samych podstawach: $a^m \\cdot a^n = a^{m+n}$.\n\n1. Dodajemy do siebie wykładniki potęg: $3 + 2 = 5$\n2. Otrzymujemy: $2^5$\n3. Obliczamy wartość: $2 \\cdot 2 \\cdot 2 \\cdot 2 \\cdot 2 = 32$"
            },
            {
                "id_zadania": "cke_mat_04",
                "poddzial": "Procenty",
                "tresc": "Test z matematyki składa sie z 40 zadan. Poszczególne sekcje obejmują statystyka-20%, algebra-25%, planimetria-15%, stereometria-5%. Ile wynosi liczba zadań z arytmetyki?",
                "opcje": ["14", "18", "26", "35"],
                "poprawna": "14",
                "punkty_max": 1,
                "wyjasnienie": "### **Rozwiązanie krok po kroku**\n\n1. **Suma znanych podziałów procentowych:**\nZsumuj udział procentowy podanych działów matematyki:\n$20\\% + 25\\% + 15\\% + 5\\% = 65\\%$\n\n2. **Obliczenie udziału procentowego arytmetyki:**\nOdejmij uzyskany wynik od całości ($100\\%$):\n$100\\% - 65\\% = 35\\%$\n\n3. **Obliczenie liczby zadań z arytmetyki:**\nOblicz $35\\%$ z łącznej puli $40$ zadań, zamieniając procent na ułamek dziesiętny:\n$0{,}35 \\cdot 40 = 14$\n\n**Odpowiedź:** Zadania z arytmetyki stanowią $35\\%$ całości, czyli jest ich dokładnie **14**."
            }
        ]

# POPRAWKA: Zmiana nazwy funkcji na właściwą (zgodną z definicją wyżej)
baza_pelna = load_app_data()
liczba_w_bazie = len(baza_pelna)

# PANEL BOCZNY (MENU GŁÓWNE)

with st.sidebar:
    st.header("⚙️ Menu Główne")
    tryb = st.radio("Wybierz tryb pracy:", ["🏋️ Tryb Treningu", "⏱️ Wyścig z czasem"])

    st.divider()

    # Domyślna wartość dla bezpieczeństwa kodu
    ile_losowac = liczba_w_bazie

    # Warunkowy wybór liczby zadań - TYLKO dla wyścigu
    if tryb == "⏱️ Wyścig z czasem":
        st.subheader("Ustawienia Wyścigu")
        if liczba_w_bazie < 20:
            st.info(f"Baza zawiera {liczba_w_bazie} zadania. Losujemy wszystkie.")
            ile_losowac = liczba_w_bazie
        else:
            ile_losowac = st.slider(
                "Ile zadań chcesz wylosować?",
                min_value=5,
                max_value=min(25, liczba_w_bazie),
                value=min(10, liczba_w_bazie),
                step=5
            )

        st.divider()

    # PRZYCISK RESETU
    if st.button("🔄 Wylosuj nowy zestaw zadań", use_container_width=True):
        if "wyścig_zestaw" in st.session_state:
            del st.session_state["wyścig_zestaw"]
        if "czas_startu" in st.session_state:
            del st.session_state["czas_startu"]
        if "trening_zestaw" in st.session_state:
            del st.session_state["trening_zestaw"]
        st.rerun()


# OBSŁUGA SEKCJI WYBORU I LOSOWANIA (Zarządzanie stanem - Session State)

if tryb == "🏋️ Tryb Treningu":
    if "trening_zestaw" not in st.session_state:
        ile_do_treningu = min(20, liczba_w_bazie)
        st.session_state["trening_zestaw"] = random.sample(baza_pelna, ile_do_treningu)

    zadania_do_wyswietlenia = st.session_state["trening_zestaw"]
    pozostalo = 999999

else:
    if "wyścig_zestaw" not in st.session_state:
        st.session_state["wyścig_zestaw"] = random.sample(baza_pelna, ile_losowac)
        st.session_state["czas_startu"] = time.time()

    zadania_do_wyswietlenia = st.session_state["wyścig_zestaw"]


    # PŁYNNY PASEK CZASU BEZ MRUGANIA
    # Tworzymy izolowany fragment kodu, który odświeża tylko pasek, nie ruszając zadań
    @st.fragment(run_every="1s")
    def wyswietl_pasek_czasu():
        czas_na_wyscig = ile_losowac * 90
        minelo = time.time() - st.session_state["czas_startu"]
        pozostalo_sekund = max(0, czas_na_wyscig - minelo)

        procent_czasu = pozostalo_sekund / czas_na_wyscig

        minuty = int(pozostalo_sekund // 60)
        sekundy = int(pozostalo_sekund % 60)

        if pozostalo_sekund > 0:
            st.write(f"⏱️ Pozostały czas: **{minuty:02d}:{sekundy:02d}**")
            st.progress(procent_czasu)
        else:
            st.error("🚨 Czas minął! Kliknij przycisk na dole, aby zapisać dotychczasowe odpowiedzi.")


    # Wywołujemy nasz płynny pasek czasu na górze strony
    wyswietl_pasek_czasu()
    pozostalo = 1  # Wartość techniczna dla silnika analizy


# 2. TWORZENIE FORMULARZA Z ZADANIAMI

with st.form("arkusz_egzaminacyjny"):
    odpowiedzi_ucznia = {}

    # Wyświetlanie zadań jedno po drugim
    for i, zadanie in enumerate(zadania_do_wyswietlenia, 1):
        id_z = str(zadanie.get("id_zadania", f"zadanie_{i}"))

        st.markdown(f"### Zadanie {i} ({zadanie['poddzial']})")
        st.write(zadanie["tresc"])

        wybor = st.radio(
            "Wybierz odpowiedź:",
            options=zadanie["opcje"],
            key=f"radio_{id_z}",
            index=None,
            horizontal=True
        )
        odpowiedzi_ucznia[id_z] = wybor
        st.markdown("---")

    zatwierdz = st.form_submit_button("Zakończ egzamin i pobierz analizę 📊")


# 3. SILNIK ANALITYCZNY & WYJAŚNIENIA (Uruchamia się po zatwierdzeniu lub upływie czasu)

# Wymuszamy zatwierdzenie, jeśli skończył się czas w trybie wyścigu
if tryb == "⏱️ Wyścig z czasem" and pozostalo <= 0:
    zatwierdz = True

if zatwierdz:
    st.header("📋 Wyniki Twojej Analizy")

    analiza_poddzialow = {}
    ogolne_punkty_ucznia = 0
    ogolne_punkty_max = 0

    for i, zadanie in enumerate(zadania_do_wyswietlenia, 1):
        id_z = str(zadanie.get("id_zadania", f"zadanie_{i}"))

        surowy_poddzial = zadanie.get("poddzial", "Inne")
        if isinstance(surowy_poddzial, list):
            poddzial = str(surowy_poddzial[0]) if surowy_poddzial else "Inne"
        else:
            poddzial = str(surowy_poddzial)

        odpowiedz = odpowiedzi_ucznia.get(id_z)

        if poddzial not in analiza_poddzialow:
            analiza_poddzialow[poddzial] = {"zdobyte": 0, "max": 0}

        p_max = int(zadanie.get("punkty_max", 1))
        punkty_za_zadanie = p_max if odpowiedz == zadanie["poprawna"] else 0

        analiza_poddzialow[poddzial]["zdobyte"] += punkty_za_zadanie
        analiza_poddzialow[poddzial]["max"] += p_max

        ogolne_punkty_ucznia += punkty_za_zadanie
        ogolne_punkty_max += p_max

    procent_ogolny = (ogolne_punkty_ucznia / ogolne_punkty_max * 100) if ogolne_punkty_max > 0 else 0

    st.metric(label="Twój ogólny wynik:",
              value=f"{ogolne_punkty_ucznia} / {ogolne_punkty_max} pkt ({procent_ogolny:.0f}%)")

    st.subheader("🔍 Szczegółowy stan Twojej wiedzy z poddziałów:")

    for idx, (poddzial, dane) in enumerate(analiza_poddzialow.items()):
        procent_poddzialu = (dane["zdobyte"] / dane["max"] * 100) if dane["max"] > 0 else 0

        if procent_poddzialu >= 75:
            status_emoji = "🟢"
            komunikat = "Świetnie! Ten temat masz opanowany. Pracuj tak dalej."
        elif 50 <= procent_poddzialu < 75:
            status_emoji = "🟡"
            komunikat = "Znasz podstawy, ale robisz drobne błędy. Przejrzyj wzory i zrób kilka zadań utrwalających."
        else:
            status_emoji = "🔴"
            komunikat = "🚨 Musisz to poduczyć! Masz spore luki w tym temacie. Zacznij naukę od teorii i prostych przykładów."

        with st.expander(f"{status_emoji} {poddzial} — {procent_poddzialu:.0f}% ({dane['zdobyte']}/{dane['max']} pkt)",
                         key=f"exp_poddzial_{idx}"):
            st.write(komunikat)
            st.progress(procent_poddzialu / 100)

    st.markdown("---")
    st.subheader("📝 Przegląd zadań i wyjaśnienia krok po kroku")
    st.write("Przeanalizuj swoje odpowiedzi. Kliknij na zadanie, aby zobaczyć pełne rozwiązanie.")

    for i, zadanie in enumerate(zadania_do_wyswietlenia, 1):
        id_z = str(zadanie.get("id_zadania", f"zadanie_{i}"))

        surowy_poddzial = zadanie.get("poddzial", "Inne")
        poddzial_tekst = str(surowy_poddzial[0]) if isinstance(surowy_poddzial, list) and surowy_poddzial else str(
            surowy_poddzial)

        wybrana_odp = odpowiedzi_ucznia.get(id_z)
        czy_poprawna = (wybrana_odp == zadanie["poprawna"])

        if wybrana_odp is None:
            zadanie_status = "⚪ Brak odpowiedzi"
        elif czy_poprawna:
            zadanie_status = "✅ Dobrze"
        else:
            zadanie_status = f"❌ Źle (Wybrano: {wybrana_odp})"

        with st.expander(f"Zadanie {i}: {poddzial_tekst} — {zadanie_status}", key=f"exp_zadanie_{id_z}"):
            st.markdown(f"**Treść zadania:** {zadanie['tresc']}")
            st.markdown(f"Poprawna odpowiedź: **{zadanie['poprawna']}**")

            if wybrana_odp is None:
                st.info("Pominięto to zadanie podczas testu.")
            elif czy_poprawna:
                st.success("Twoja odpowiedź jest poprawna!")
            else:
                st.error(f"Twoja odpowiedź: {wybrana_odp}. Poprawna odpowiedź: {zadanie['poprawna']}")

            if "wyjasnienie" in zadanie:
                st.markdown("#### Wyjaśnienie:")
                tekst_wyjasnienia = zadanie["wyjasnienie"].replace("\\n", "\n")

                st.markdown(tekst_wyjasnienia)
            else:st.warning("Brak przygotowanego wyjaśnienia dla tego zadania w bazie JSON.")

st.divider()
st.write(
    "**Nota prawna:** Wszystkie zawarte w aplikacji arkusze egzaminacyjne oraz "
    "klucze odpowiedzi są materiałami publicznymi, pochodzącymi z oficjalnych "
    "zasobów Centralnej Komisji Egzaminacyjnej (CKE). Twórca aplikacji nie rości "
    "sobie żadnych praw autorskich do tych materiałów. "
    "Materiały zostały użyte wyłącznie w celach edukacyjnych. "
    "Aplikacja ma charakter prywatny, jest rozwijana niezależnie i nie jest "
    "w żaden sposób powiązana, autoryzowana ani sponsorowana przez CKE."
    "Logotypy oraz nazwy własne CKE zostały użyte wyłącznie w celach informacyjnych."
)
