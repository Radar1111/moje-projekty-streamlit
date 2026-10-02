import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components
from huggingface_hub import hf_hub_download

# Ustawienia strony
st.set_page_config(page_title="E8 Angielski - Generator Diagnozy", layout="wide", page_icon="🇬🇧")


HF_TOKEN = os.environ.get("HF_TOKEN")

REPO_ID = "Radar1111/AngielskiE8" 

@st.cache_data
def load_json_from_hf(file_name):
    """Pobiera i ładuje plik JSON z prywatnego repozytorium Hugging Face"""
    try:
        path = hf_hub_download(
            repo_id=REPO_ID,
            filename=file_name,
            repo_type="dataset",
            token=HF_TOKEN
        )
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Nie udało się pobrać pliku `{file_name}` z Hugging Face. Szczegóły: {e}")
        return []

@st.cache_data
def get_audio_path_from_hf(audio_name):
    """Pobiera plik MP3 z HF i wyświetla na ekranie status pobierania"""
    if not audio_name:
        st.warning("⚠️ Funkcja nie otrzymała nazwy pliku audio z bazy JSON!")
        return None
    try:
        path = hf_hub_download(
            repo_id=REPO_ID,
            filename=audio_name,
            repo_type="dataset",
            token=HF_TOKEN
        )
        
        # 🟢 TEST: Informacja wizualna na stronie, że plik istnieje i został pobrany
        if path and os.path.exists(path):
            st.success(f"✅ Sukces! Plik `{audio_name}` został pobrany z HF i zapisany na serwerze pod ścieżką: {path}")
        return path
        
    except Exception as e:
        # 🔴 TEST: Wyświetlenie dokładnego błędu, jeśli pobieranie się nie powiodło
        st.error(f"❌ Błąd pobierania pliku `{audio_name}` z Hugging Face. Szczegóły błędu: {e}")
        return None


quiz_questions = load_json_from_hf("diagnoza.json")
reading_data = load_json_from_hf("teksty.json")
listening_data = load_json_from_hf("sluchanie.json")


def render_cke_audio(audio_path, unique_id):
    # Domyślny, zapasowy link do nagrania, jeśli plik na HF zniknie
    audio_url = "https://soundhelix.com"

    # 1. GENEROWANIE BEZPIECZNEGO LINKU DO PRYWATNEGO REPOZYTORIUM HF
    if audio_path:
        # Wyciągamy czystą nazwę pliku z pobranej ścieżki (np. sluchanie_1.mp3.mp3)
        nazwa_pliku = os.path.basename(audio_path)
        
        # Tworzymy bezpośredni link WWW, doklejając Twój token. 
        # Przeglądarka bez problemu poradzi sobie ze strumieniowaniem z tego adresu URL!
        audio_url = f"https://huggingface.co{REPO_ID}/resolve/main/audio/{nazwa_pliku}?download=true&token={HF_TOKEN}"
    else:
        st.caption("ℹ️ Ładowanie pliku audio z chmury Hugging Face...")

    # Zliczanie odsłuchów w st.session_state
    state_key = f"listen_count_{unique_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0

    current_count = st.session_state[state_key]

    if current_count >= 2:
        st.error("🚫 Wykorzystałeś limit 2 odsłuchów wymagany na prawdziwym egzaminie CKE!")
        return

    # Komunikaty o dostępnych próbach
    if current_count == 0:
        st.info("🎵 Dostępne odtworzenia nagrania: 2/2")
    elif current_count == 1:
        st.warning("⚠️ Dostępne odtworzenia nagrania: 1/2 (Ostatnia szansa)")

    # Guzik aktywujący odtwarzacz
    if st.button("▶️ Uruchom nagranie (Zlicza odsłuch)", key=f"btn_{unique_id}"):
        st.session_state[state_key] += 1
        st.rerun()

    # Wyświetlenie zabezpieczonego odtwarzacza HTML po kliknięciu przycisku
    if current_count > 0:
        html_code = f"""
        <style>
          /* Blokujemy oszukiwanie: ukrywamy oś czasu, czas trwania i pobieranie */
          audio::-internal-media-controls-download-button,
          audio::-webkit-media-controls-timeline,
          audio::-webkit-media-controls-current-time-display,
          audio::-webkit-media-controls-time-remaining-display {{
            display: none !important;
          }}
          .player-box {{
            font-family: sans-serif;
            padding: 12px;
            background-color: #f0f2f6;
            border-radius: 8px;
            text-align: center;
            max-width: 400px;
            margin-bottom: 15px;
            border: 1px solid #d1d5db;
          }}
          .custom-play-btn {{
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
          }}
          .custom-play-btn:hover {{
            background-color: #e04141;
          }}
        </style>
        <div class="player-box">
          <p style="margin: 0 0 10px 0; color: #31333F; font-weight: bold; font-size: 14px;">
            Odtwarzacz Egzaminacyjny CKE (Odsłuch {current_count}/2):
          </p>
          <!-- audio z id, załadowane z bezpiecznego URL -->
          <audio id="audio_{unique_id}" src="{audio_url}" controlsList="nodownload" style="width: 100%; max-width: 300px;"></audio>
          <div style="margin-top: 8px;">
            <button class="custom-play-btn" onclick="document.getElementById('audio_{unique_id}').play()">🎵 Włącz dźwięk</button>
          </div>
        </div>
        """
        # Wysokość 140 pozwala na ładne wyświetlenie ramki i przycisku włączenia dźwięku
        components.html(html_code, height=140)

# Panel boczny
st.sidebar.title("🎯 E8 English Diagnostic")
st.sidebar.markdown("Wybierz sekcję egzaminu do ćwiczenia:")
menu = st.sidebar.radio(
    "Nawigacja:",
    ["Strona Główna & Info", "🤖 Szybki Quiz Diagnostyczny", "📚 Czytanie (Teksty ~200 słów)",
     "🎧 Słuchanie (ElevenLabs Player)"]
)

st.sidebar.info("Aplikacja wspiera przygotowanie do Egzaminu Ósmoklasisty z języka angielskiego.")

# Strona główna
if menu == "Strona Główna & Info":
    st.title("🇬🇧 Kompleksowy Panel Diagnostyczny E8")
    st.markdown("""
    Witaj w aplikacji wspierającej przygotowania do **Egzaminu Ósmoklasisty z języka angielskiego**! 
    Narzędzie zostało stworzone w oparciu o aktualne wymagania i wytyczne **Centralnej Komisji Egzaminacyjnej (CKE)**.

    ### 📋 Co znajdziesz w aplikacji?
    * **Quiz Diagnostyczny:** Sprawdź szybko swoją wiedzę z gramatyki, struktur oraz kluczowych funkcji językowych.
    * **Rozumienie Tekstów Pisanych:** Trzy pełnowymiarowe teksty (ok. 200 słów każdy) o zróżnicowanej tematyce (np. świat zwierząt, e-mail do kolegi, zakupy) wraz z zadaniami zamkniętymi.
    * **Rozumienie ze Słuchu:** Trzy nagrania zoptymalizowane pod kątem naturalnie brzmiącego lektora AI, uzupełnione o zadania otwarte (uzupełnianie luk) oraz systemową blokadę liczby odtworzeń (zgodnie z realnym egzaminem).
    """)

    # Małe podsumowanie struktury
    col1, col2, col3 = st.columns(3)
    col1.metric("Czas trwania egzaminu", "90 minut")
    col2.metric("Liczba części w arkuszu", "5 sekcji")
    col3.metric("Długość wypracowania", "50-120 słów")

# Quiz - Diagnoza
elif menu == "🤖 Szybki Quiz Diagnostyczny":
    st.title("🤖 Szybki Quiz Diagnostyczny (Gramatyka i Funkcje)")
    st.write(
        "Wybierz poprawne odpowiedzi. System natychmiast zweryfikuje Twój wybór i poda wyjaśnienie."
    )

    # Wczytanie pytań z zewnętrznego pliku JSON
    questions = quiz_questions

    if questions:
        # Dynamiczne renderowanie każdego pytania z pliku JSON
        for item in questions:
            # Unikalny klucz dla st.radio jest wymagany, generujemy go na podstawie ID pytania
            unique_key = f"quiz_q_{item['id']}"

            user_choice = st.radio(
                label=item["question"],
                options=item["options"],
                index=None,
                key=unique_key,
            )

            # Weryfikacja odpowiedzi użytkownika
            if user_choice:
                if user_choice == item["correct"]:
                    st.success(item["success_msg"])
                else:
                    st.error(item["error_msg"])

            st.markdown("---")

# Czytanie ze zrozumieniem
elif menu == "📚 Czytanie (Teksty ~200 słów)":
    st.title("📚 Rozumienie Tekstów Pisanych")

    # Wczytanie danych z JSON
    all_texts = reading_data

    if all_texts:
        
        menu_options = [text_item["title_menu"] for text_item in all_texts]
        tekst_wybor = st.selectbox("Wybierz tekst do analizy:", menu_options)

        
        selected_text_data = next(
            (t for t in all_texts if t["title_menu"] == tekst_wybor), None
        )

        if selected_text_data:
            st.subheader(selected_text_data["title_text"])
            st.info(selected_text_data["content"])

            
            with st.form(key=f"form_{selected_text_data['id']}"):
                user_answers = {}

                
                for q in selected_text_data["questions"]:
                    # Zapisujemy odpowiedź użytkownika w słowniku pod kluczem ID pytania
                    user_answers[q["q_id"]] = st.radio(
                        label=q["question"],
                        options=q["options"],
                        index=None,
                        key=f"radio_{selected_text_data['id']}_{q['q_id']}",
                    )

                
                submit_button = st.form_submit_button("Sprawdź odpowiedzi")

                if submit_button:
                    
                    if any(ans is None for ans in user_answers.values()):
                        st.warning(
                            "⚠️ Proszę odpowiedzieć na wszystkie pytania przed sprawdzeniem."
                        )
                    else:
                        
                        all_correct = True
                        for q in selected_text_data["questions"]:
                            if user_answers[q["q_id"]] != q["correct"]:
                                all_correct = False
                                break

                        
                        if all_correct:
                            st.success(selected_text_data["success_msg"])
                        else:
                            st.error(selected_text_data["error_msg"])

# SŁUCHANIE (ELEVENLABS MULTI-PLAYER)
elif menu == "🎧 Słuchanie (ElevenLabs Player)":
    st.title("🎧 Rozumienie ze Słuchu (Zadania Otwarte CKE)")
    st.write(
        "Wklej poniższe teksty do ElevenLabs, pobierz pliki MP3 i umieść w folderze `audio/` aplikacji."
    )

    # Wczytanie zadań słuchowych z JSON
    all_listening_tasks = listening_data

    st.write("### 🔍 TEST BAZY SŁUCHANIA:")
    st.write(all_listening_tasks)

    if all_listening_tasks:
       
        listening_options = [task["title_menu"] for task in all_listening_tasks]
        # Wybór zadania przez użytkownika
        sluchanie_wybor = st.selectbox(
            "Wybierz zadanie ze słuchu:", listening_options
        )

        # Wyszukanie wybranego zadania w bazie danych
        selected_task = next(
            (t for t in all_listening_tasks if t["title_menu"] == sluchanie_wybor),
            None,
        )

        # Poniższa linia 'if' musi zaczynać się od dokładnie 8 spacji:
        if selected_task:
            st.markdown("**Tekst dla ElevenLabs:**")
            st.code(selected_task["elevenlabs_script"])

            # Pobieramy czystą nazwę pliku z bazy JSON
            nazwa_pliku_mp3 = selected_task.get("audio_file") or selected_task.get("audio_path")
            
            # Wywołujemy pobieranie z Hugging Face
            sciezka_na_serwerze = get_audio_path_from_hf(nazwa_pliku_mp3)

            # Przekazujemy ściągniętą ścieżkę do odtwarzacza CKE
            render_cke_audio(sciezka_na_serwerze, selected_task["id"])


            with st.form(key=f"form_listen_{selected_task['id']}"):
                st.write("Uzupełnij luki po angielsku zgodnie z nagraniem:")
                user_inputs = {}



                
                for gap in selected_task["gaps"]:
                    user_inputs[gap["gap_id"]] = st.text_input(
                        label=gap["label"],
                        placeholder=gap["placeholder"],
                        key=f"input_{selected_task['id']}_{gap['gap_id']}",
                    )

               
                submit_button = st.form_submit_button("Zatwierdź odpowiedzi")

                if submit_button:
                    
                    if any(
                        val.strip() == "" for val in user_inputs.values()
                    ):
                        st.warning("⚠️ Proszę uzupełnić wszystkie luki.")
                    else:
                        all_gaps_correct = True

                       
                        for gap in selected_task["gaps"]:
                            user_answer = (
                                user_inputs[gap["gap_id"]].strip().lower()
                            )
                            
                            if (
                                user_answer
                                not in gap["accepted_answers"]
                            ):
                                all_gaps_correct = False
                                break

                        # Komunikat końcowy
                        if all_gaps_correct:
                            st.success(selected_task["success_msg"])
                        else:
                            st.error(selected_task["error_msg"])

st.markdown("---")
st.caption(
    "Aplikacja o charakterze edukacyjnym. Audio generated via ElevenLabs."
)
