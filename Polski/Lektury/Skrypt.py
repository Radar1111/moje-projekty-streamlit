import streamlit as st
import json
import os
import random
from huggingface_hub import hf_hub_download, list_repo_files


# 1. KONFIGURACJA HUGGING FACE 

REPO_ID = "Radar1111/FolderLektur" 


def pobierz_liste_lektur():
    """Pobiera listę wszystkich plików .json z repozytorium Hugging Face"""
    if "HF_TOKEN" not in st.secrets:
        st.error("❌ Brak tokenu 'HF_TOKEN' w Streamlit Secrets!")
        st.info("Dodaj token w panelu Streamlit Cloud (Settings -> Secrets) lub lokalnie w .streamlit/secrets.toml")
        return []
        
    try:
        wszystkie_pliki = list_repo_files(
            repo_id=REPO_ID, 
            repo_type="dataset", 
            token=st.secrets["HF_TOKEN"]
        )
        pliki_json = [f for f in wszystkie_pliki if f.endswith('.json')]
        return pliki_json
    except Exception as e:
        st.error(f"❌ Błąd połączenia z Hugging Face: {e}")
        st.warning(f"Sprawdź czy REPO_ID ('{REPO_ID}') jest poprawne i czy token ma odpowiednie uprawnienia.")
        return []

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


def wczytaj_json(nazwa_pliku):
    """Pobiera i wczytuje konkretny plik JSON z Hugging Face"""
    if not nazwa_pliku.endswith('.json'):
        nazwa_pliku += '.json'
    
    cached_file_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=nazwa_pliku,
        repo_type="dataset",
        token=st.secrets["HF_TOKEN"]
    )
    
    with open(cached_file_path, "r", encoding="utf-8") as f:
        return json.load(f)



# 2. USTAWIENIA STRONY I LISTOWANIE LEKTUR

st.set_page_config(page_title="Quiz Master Lektur", layout="centered")

# Pobieranie listy plików JSON bezpośrednio z Hugging Face
pliki_json = pobierz_liste_lektur()

# Jeśli wystąpił błąd lub lista jest pusta, zatrzymujemy aplikację
if not pliki_json:
    st.stop()

# Tworzenie czystych tytułów lektur (bez końcówki .json) do menu wyboru
tytuly_lektur = [f.replace(".json", "") for f in pliki_json]


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

    # Formularz: wybór i zatwierdzenie odpowiedzi
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

    # Wyświetlenie wyniku i przycisk dalej
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

wyswietl_sekcje_wsparcia()

st.divider()
st.caption("Najcierpliwszy portal do polskiego")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
