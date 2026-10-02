import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
import json
import os
from PIL import Image
from huggingface_hub import hf_hub_download 

st.set_page_config(page_title="Darmowa Nauka Języków", layout="centered")
st.title("Otwarte Płótno do Nauki Języków Trudnych 🏮")
st.subheader("Całkowicie darmowa aplikacja edukacyjna")

@st.cache_data
def load_quiz_data():
    # Pamiętaj, aby podać pełną ścieżkę do datasetu, np. "Radar1111/NazwaDatasetu"
    repo_id = "Radar1111/TrudnePisz" 
    filename = "baza_znakow.json"
    
    hf_token = st.secrets.get("HF_TOKEN")
    if not hf_token:
        st.error("Brak tokenu HF_TOKEN w konfiguracji Streamlit Secrets!")
        return []
        
    try:
        # Pobranie pliku z Hugging Face przez oficjalną bibliotekę
        local_file_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",
            token=hf_token
        )
        
        # Wczytanie i zwrócenie danych
        with open(local_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except Exception as e:
        st.error(f"Nie udało się pobrać bazy danych z Hugging Face: {e}")
        return []

if not pelna_baza:
    st.error("Nie znaleziono pliku baza_znakow.json lub plik jest pusty! Upewnij się, że plik znajduje się w tym samym folderze co skrypt.")
    st.stop()

# Wybór języka
jezyk = st.radio("Wybierz język do nauki:", ["Chiński", "Arabski", "Hindi (Indie)"], horizontal=True)


if "Chiński" in jezyk:
    klucz_jezyka = "Chiński"
elif "Arabski" in jezyk:
    klucz_jezyka = "Arabski"
else:
    klucz_jezyka = "Hindi"


aktywna_baza = pelna_baza.get(klucz_jezyka, {})

if not aktywna_baza:
    st.warning(f"Brak danych dla języka: {jezyk} w pliku JSON. Wybierz inny język lub uzupełnij bazę.")
    st.stop()

# Wybór znaku
wybrany_znak = st.selectbox("Wybierz znak/literę do ćwiczenia:", list(aktywna_baza.keys()))

# Generowanie wzorca
def generuj_wzorzec(linie_znaku, czy_arabski=False):
    img = np.ones((300, 300), dtype=np.uint8) * 255
    for linia in linie_znaku:
        if czy_arabski:
            # Lustrzane odbicie dla arabski osi X (300 - x), aby pismo biegło od prawej do lewej
            start = (300 - linia["start"][0], linia["start"][1])
            end = (300 - linia["end"][0], linia["end"][1])
        else:
            # Dla Chińskiego i Hindi zostaje standardowo
            start = tuple(linia["start"])
            end = tuple(linia["end"])

        cv2.line(img, start, end, 0, 16)  # Grubość 16
    return img

# Bezpieczne generowanie wzorca dla wybranego znaku
linie_znaku = aktywna_baza.get(wybrany_znak, [])
jest_arabski = (klucz_jezyka == "Arabski")
wzorzec = generuj_wzorzec(aktywna_baza.get(wybrany_znak, []), czy_arabski=jest_arabski)

# Tworzymy  podkład do wyświetlenia jako tło płótna (efekt "ghost")
wzorzec_tlo = np.where(wzorzec == 0, 220, 255).astype(np.uint8)
img_tlo = Image.fromarray(wzorzec_tlo).convert("RGB")

st.markdown("---")
st.write(f"**Narysuj znak poniżej (wzorzec wyświetla się jako jasnoszary ślad):**")

# Płótno
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=12,
    stroke_color="#000000",
    background_image=img_tlo,
    height=300,
    width=300,
    drawing_mode="freedraw",
    key=f"canvas_{wybrany_znak}",
    return_image_data=True
)
# Inicjalizacja stanu
if "sprawdzone" not in st.session_state:
    st.session_state.sprawdzone = False

if st.button("Sprawdź wynik 🔍", use_container_width=True):
    st.session_state.sprawdzone = True

if st.session_state.sprawdzone and canvas_result.image_data is not None:
    user_rgba = canvas_result.image_data

    # 1. Wyciągamy kanał ALFA (indeks 3).
    # Tam, gdzie użytkownik rysował, alfa > 0. Puste tło ma alfa == 0.
    user_alpha = user_rgba[:, :, 3]

    # 2. Tworzymy maskę rysunku użytkownika: rysunek to białe piksele (255), tło to czarne (0)
    _, user_binary = cv2.threshold(user_alpha, 10, 255, cv2.THRESH_BINARY)

    # 3. Dopasowanie wielkości (Zabezpieczenie)
    # Upewnij się, że wzorzec ma dokładnie te same wymiary co canvas
    if wzorzec.shape[:2] != user_binary.shape[:2]:
        wzorzec = cv2.resize(wzorzec, (user_binary.shape[1], user_binary.shape[0]))

    # 4. Zakładamy, że Twój obiekt 'wzorzec' ma czarne linie na białym tle (klasyczna kolorowanka).
    # Jeśli wzorzec to czarne linie, odwracamy go, by linie były BIAŁE (255)
    if len(wzorzec.shape) == 3:  # jeśli wzorzec jest w BGR/RGB
        wzorzec_gray = cv2.cvtColor(wzorzec, cv2.COLOR_BGR2GRAY)
        _, wzorzec_bin = cv2.threshold(wzorzec_gray, 200, 255, cv2.THRESH_BINARY_INV)
    else:
        # Jeśli wzorzec jest już czarno-biały (np. czarny znak na białym tle)
        _, wzorzec_bin = cv2.threshold(wzorzec, 200, 255, cv2.THRESH_BINARY_INV)

    # 5. Obliczamy iloczyn (nakładanie się białych linii wzorca i białych linii użytkownika)
    iloczyn = cv2.bitwise_and(wzorzec_bin, user_binary)

    # 6. Zliczanie pikseli o wartości 255 (białych)
    suma_wzorca = np.sum(wzorzec_bin == 255)
    suma_wspolna = np.sum(iloczyn == 255)

    if suma_wzorca > 0:
        procent = (suma_wspolna / suma_wzorca) * 100
        st.metric(label="Dokładność pokrycia linii wzorcowych", value=f"{procent:.1f}%")

        if procent > 75:
            st.success("Doskonale! Znak odwzorowany perfekcyjnie. 🎉")
        elif procent > 40:
            st.warning("Dobrze, ale możesz pisać dokładniej po szarych liniach. ✍️")
        else:
            st.error("Zbyt małe pokrycie. Spróbuj pisać dokładnie po śladzie!")

    st.session_state.sprawdzone = False
