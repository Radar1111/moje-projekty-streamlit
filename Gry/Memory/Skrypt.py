import streamlit as st
import random
import time

# 1. Konfiguracja strony
st.set_page_config(page_title="Gra Memory Emoji", layout="centered")
st.title("Gra Memory z Emoji")
st.write("Znajdź wszystkie 8 par! Kliknij kartę, aby ją odsłonić.")

# 2. Definicja zestawu
EMOJI_LIST = ["🦁", "🦊", "🐸", "🦄", "🐼", "🐙", "🐝", "🦖"]
TOTAL_PAIRS = len(EMOJI_LIST)

# 3. Inicjalizacja stanu sesji
if "cards" not in st.session_state:
    shuffled_cards = EMOJI_LIST * 2
    random.shuffle(shuffled_cards)

    st.session_state.cards = shuffled_cards
    st.session_state.revealed = [False] * 16
    st.session_state.matched = [False] * 16
    st.session_state.selected_indices = []
    st.session_state.moves = 0


# Funkcja restartu gry
def restart_gry():
    shuffled_cards = EMOJI_LIST * 2
    random.shuffle(shuffled_cards)
    st.session_state.cards = shuffled_cards
    st.session_state.revealed = [False] * 16
    st.session_state.matched = [False] * 16
    st.session_state.selected_indices = []
    st.session_state.moves = 0


# 4. Logika obsługi kliknięć
def card_clicked(idx):
    # Ignoruj kliknięcie w kartę już sparowaną lub odkrytą
    if st.session_state.matched[idx] or st.session_state.revealed[idx]:
        return

    # Odkryj klikniętą kartę i dodaj do listy
    st.session_state.revealed[idx] = True
    st.session_state.selected_indices.append(idx)


# 5. Sprawdzenie dopasowania po wybraniu dwóch kart
if len(st.session_state.selected_indices) == 2:
    st.session_state.moves += 1
    idx1, idx2 = st.session_state.selected_indices

    if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
        # Znaleziono parę – oznacz jako dopasowane na stałe
        st.session_state.matched[idx1] = True
        st.session_state.matched[idx2] = True
        st.session_state.selected_indices = []
        st.rerun()
    # USUNĘLIŚMY stąd time.sleep i ukrywanie kart!

# NOWY BLOK: Logika czyszczenia niedopasowanej pary przy KOLEJNYM ruchu
# Jeśli w stanie sesji wiszą 2 karty, a gracz kliknie trzecią,
# najpierw automatycznie zakrywamy poprzednie dwie.
if len(st.session_state.selected_indices) > 2:
    # Pobieramy indeksy dwóch pierwszych (starych) kart
    idx1, idx2 = st.session_state.selected_indices[0], st.session_state.selected_indices[1]
    st.session_state.revealed[idx1] = False
    st.session_state.revealed[idx2] = False
    # Zostawiamy w pamięci tylko tę trzecią, najnowszą kartę
    st.session_state.selected_indices = [st.session_state.selected_indices[2]]
    st.rerun()


# 6. Statystyki gry
col_stats1, col_stats2 = st.columns(2)
with col_stats1:
    st.metric("Liczba wykonanych ruchów", st.session_state.moves)
with col_stats2:
    pairs_found = sum(st.session_state.matched) // 2
    st.metric("Znaleziono pary", f"{pairs_found} / {TOTAL_PAIRS}")

# 7. Siatka kart 4 x 4
for row in range(4):
    cols = st.columns([1, 1, 1, 1], gap="small")
    for col in range(4):
        idx = row * 4 + col

        # Etykieta karty
        if st.session_state.revealed[idx] or st.session_state.matched[idx]:
            label = st.session_state.cards[idx]
        else:
            label = "❓"

        # Wyłączenie przycisku gdy już dopasowana lub tymczasowo odkryta
        is_disabled = st.session_state.matched[idx] or st.session_state.revealed[idx]

        # Karta jako przycisk
        cols[col].button(
            label,
            key=f"card_{idx}",
            on_click=card_clicked,
            args=(idx,),
            disabled=is_disabled,
            use_container_width=True,
        )

# 8. Warunek wygranej
if all(st.session_state.matched):
    st.balloons()
    st.success("Gratulacje! Udało Ci się znaleźć wszystkie pary!")

# 9. Przycisk restartu
st.write("---")
st.button("Zagraj od nowa", on_click=restart_gry, type="primary")

st.divider()
st.caption("Relaks po nauce")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
