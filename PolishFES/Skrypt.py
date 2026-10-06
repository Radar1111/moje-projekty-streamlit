import streamlit as st
from gtts import gTTS
import io
import json
import random


from huggingface_hub import hf_hub_download

@st.cache_data
def load_vocabulary():
    """
    Ładuje bazę słówek. Najpierw próbuje pobrać aktualny plik z Hugging Face,
    a w przypadku błędu lub braku tokenu, wczytuje plik lokalny lub bazę awaryjną.
    """
    repo_id = "Radar1111/PolishFES"
    filename = "phrases.json"  
    
    hf_token = st.secrets.get("HF_TOKEN")
    
    # 1. PRÓBA: Pobranie z Hugging Face (jeśli jest token)
    if hf_token:
        try:
            local_file_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                repo_type="dataset",
                token=hf_token
            )
            with open(local_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Nie udało się pobrać danych z Hugging Face ({e}). Przełączam na tryb lokalny.")
    else:
        st.warning("Brak HF_TOKEN w Streamlit Secrets. Uruchamiam z pliku lokalnego.")

    # 2. PRÓBA: Wczytanie z lokalnego pliku (fallback)
    try:
        with open("phrases.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # 3. OSTATECZNOŚĆ: Całkowicie awaryjna baza w kodzie
        return [
            {
                "polish": "Dzień dobry", 
                "meaning": "Good morning", 
                "phonetic": "Jean DOH-bree", 
                "category": "Phrases"
            }
        ]



def wyswietl_sekcje_wsparcia():
    # Inicjalizacja sesji
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"


    st.divider()


    with st.expander("🍩 Strefa Wspierania"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"


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

full_vocab = load_vocabulary()

# Interfejf użytkownia
st.title("🇵🇱 Learn Polish App")

# Menu dropdown
category_choice = st.selectbox(
    "Choose what you want to learn today:",
    options=["All Material", "Words Only", "Phrases Only"],
    key="category_selector"
)

# Filtrowanie bazy na podstawie wyboru użytkownika
if category_choice == "Words Only":
    vocab = [w for w in full_vocab if w.get("category") == "Words"]
elif category_choice == "Phrases Only":
    vocab = [w for w in full_vocab if w.get("category") == "Phrases"]
else:
    vocab = full_vocab

# Resetowanie stanów przy zmianie kategorii
if "last_category" not in st.session_state:
    st.session_state.last_category = category_choice

if st.session_state.last_category != category_choice:
    st.session_state.fc_index = 0
    st.session_state.fc_flipped = False
    st.session_state.current_word = None
    st.session_state.last_category = category_choice

# Inicjalizacja Stanu
if "fc_index" not in st.session_state:
    st.session_state.fc_index = 0
if "fc_flipped" not in st.session_state:
    st.session_state.fc_flipped = False

if "score" not in st.session_state:
    st.session_state.score = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "options" not in st.session_state:
    st.session_state.options = []
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "quiz_feedback" not in st.session_state:
    st.session_state.quiz_feedback = ""


# Funkcja pomocnicza do gTTS 
def generate_audio(text):
    tts = gTTS(text=text, lang='pl')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


# Funkcja losująca do quizu 
def next_quiz_question():
    st.session_state.current_word = random.choice(vocab)
    correct_ans = st.session_state.current_word["meaning"]

    # Podpowiedzi ABCD losujemy tylko z aktualnie wybranej kategorii
    other_words = [w["meaning"] for w in vocab if w["meaning"] != correct_ans]
    wrong_answers = random.sample(other_words, min(3, len(other_words)))

    options = wrong_answers + [correct_ans]
    random.shuffle(options)
    st.session_state.options = options
    st.session_state.quiz_answered = False
    st.session_state.quiz_feedback = ""



if st.session_state.current_word is None or st.session_state.current_word not in vocab:
    next_quiz_question()


tab1, tab2 = st.tabs(["📇 Flashcards (Study Mode)", "📝 Quiz ABCD (Test Mode)"])


# FISZKI

with tab1:
    st.subheader("Flashcards Mode")

    current_fc = vocab[st.session_state.fc_index]

    with st.container(border=True):
        st.write(f"### 🇵🇱 Polish: **{current_fc['polish']}**")

        fc_audio = generate_audio(current_fc['polish'])
        st.audio(fc_audio, format="audio/mp3")

        if st.session_state.fc_flipped:
            st.divider()
            st.write(f"### 🇬🇧 English: **{current_fc['meaning']}**")
            st.markdown(f"💡 *Pronunciation:* `{current_fc['phonetic']}`")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Flip Card", key="flip_btn", use_container_width=True):
            st.session_state.fc_flipped = not st.session_state.fc_flipped
            st.rerun()
    with col2:
        if st.button("➡️ Next Card", key="next_fc_btn", use_container_width=True):
            st.session_state.fc_index = (st.session_state.fc_index + 1) % len(vocab)
            st.session_state.fc_flipped = False
            st.rerun()
    with col3:
        if st.button("🔀 Shuffle List", key="shuffle_fc_btn", use_container_width=True):
            random.shuffle(vocab)
            st.session_state.fc_index = 0
            st.session_state.fc_flipped = False
            st.rerun()

    st.caption(f"Card {st.session_state.fc_index + 1} of {len(vocab)}")


# QUIZ ABCD

with tab2:
    st.subheader("Quiz Mode")
    st.write(f"**Score:** {st.session_state.score} / {st.session_state.total_questions}")

    q_pl = st.session_state.current_word["polish"]
    q_en = st.session_state.current_word["meaning"]
    q_pho = st.session_state.current_word["phonetic"]

    quiz_audio = generate_audio(q_pl)
    st.audio(quiz_audio, format="audio/mp3")
    st.info(f"Word/Phrase in Polish: **{q_pl}**")

    st.write("### ❓ What does it mean?")

    with st.form(key="quiz_form"):
        user_choice = st.radio(
            "Select one option:",
            options=st.session_state.options,
            disabled=st.session_state.quiz_answered,
            key="quiz_radio"
        )
        submit_button = st.form_submit_button(label="Check Answer")

    if submit_button and not st.session_state.quiz_answered:
        st.session_state.total_questions += 1
        st.session_state.quiz_answered = True
        if user_choice == q_en:
            st.session_state.quiz_feedback = "correct"
            st.session_state.score += 1
        else:
            st.session_state.quiz_feedback = "incorrect"
        st.rerun()

    if st.session_state.quiz_answered:
        if st.session_state.quiz_feedback == "correct":
            st.success("🎉 **Correct! Well done.**")
        else:
            st.error(f"❌ **Incorrect.** The correct answer was: **{q_en}**")

        st.markdown(f"💡 **How to pronounce it:** `{q_pho}`")

        if st.button("Next Word ➡️", type="primary", key="next_quiz_btn"):
            next_quiz_question()
            st.rerun()

wyswietl_sekcje_wsparcia()


# --- DOPISEK O WERSJI BETA ---
st.caption("---")
st.caption("🤖 Powered by Google Text-to-Speech (gTTS). For testing purposes only.")
st.caption(
    "🤖 *Note: This is a Beta version using a basic voice for testing. Realistic AI voices from ElevenLabs are coming soon!*")

# STOPKA
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
