import streamlit as st
import random

# Inicjalizacja stanu gry
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None


def check_winner(board):
    # Pełna lista 8 wygrywających układów (indeksy od 0 do 8)
    win_conditions = [ [0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                        [0, 4, 8], [2, 4, 6]
                        ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != "":
            return board[condition[0]]
    if "" not in board:
        return "Remis"
    return None


def bot_move():
    # Pobieramy aktualną planszę i wolne miejsca
    board = st.session_state.board
    empty_cells = [i for i, cell in enumerate(board) if cell == ""]

    # Jeśli brak wolnych miejsc lub gra skończona, nic nie rób
    if not empty_cells or st.session_state.winner:
        return

    # Lista układów wygrywających
    win_conditions = [ [0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                        [0, 4, 8], [2, 4, 6]
                        ]

    # Czy bot moze wygrac w tym ruchu
    for cond in win_conditions:
        # Zliczamy ile "O", ile "X" i ile pustych pól jest w danej linii
        line_values = [board[cond[0]], board[cond[1]], board[cond[2]]]
        if line_values.count("O") == 2 and line_values.count("") == 1:
            # Znajdź ten jeden pusty indeks w linii i postaw tam "O"
            for idx in cond:
                if board[idx] == "":
                    board[idx] = "O"
                    zakoncz_ruch_bota()
                    return

    # Czy blokować gracza X
    for cond in win_conditions:
        line_values = [board[cond[0]], board[cond[1]], board[cond[2]]]
        if line_values.count("X") == 2 and line_values.count("") == 1:
            # Gracz ma 2 znaki! Blokujemy puste pole w tej linii
            for idx in cond:
                if board[idx] == "":
                    board[idx] = "O"
                    zakoncz_ruch_bota()
                    return

    # Wybież losowe pole
    bot_index = random.choice(empty_cells)
    board[bot_index] = "O"
    zakoncz_ruch_bota()


def zakoncz_ruch_bota():
    """Pomocnicza funkcja do sprawdzenia stanu gry po ruchu bota"""
    winner = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
    else:
        st.session_state.current_player = "X"


def make_move(index):

    if st.session_state.board[index] == "" and not st.session_state.winner:
        # Ruch gracza X
        st.session_state.board[index] = "X"

        # Sprawdź czy gracz X wygrał
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
        else:
            # Jeśli X nie wygrał, kolej na bota
            st.session_state.current_player = "O"
            bot_move()


def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None


# Intefrejs
st.title("⭕ Kółko i Krzyżyk ❌")

if st.session_state.winner:
    if st.session_state.winner == "Remis":
        st.info("🤝 Remis!")
    else:
        st.success(f"🏆 Wygrywa: {st.session_state.winner}!")
else:
    st.write(f"Kolej gracza: **{st.session_state.current_player}** (Gra jako X)")


# STYLE CSS (Na PC i Telefon)
st.markdown("""
    <style>
    /* 1. Blokujemy automatyczne łamanie wierszy kolumn na telefonie i PC */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
        max-width: 330px !important; /* Lekko zwężone dla lepszego kształtu */
        margin: 0 auto !important; /* Środkuje każdy wiersz na ekranie */
    }

    /* 2. Zmuszamy każdą kolumnę w rzędzie do równej szerokości */
    div[data-testid="stHorizontalBlock"] > div {
        width: 33.33% !important;
        min-width: 0 !important;
    }

    /* 3. Stylizujemy same przyciski gry na IDEALNE KWADRATY */
    div[data-testid="stButton"] button {
        font-size: 36px !important;        /* Wielkie i czytelne litery */
        font-weight: 900 !important;       /* Grube ikony */

        /* KLUCZOWA ZMIANA: Wymusza idealne proporcje kwadratu 1:1 */
        aspect-ratio: 1 / 1 !important;    
        width: 100% !important;            
        height: auto !important;           /* Wyłączamy sztywną wysokość */

        border-radius: 12px !important;     /* Zaokrąglone brzegi */
        background-color: #f0f2f6 !important;
        color: #31333F !important;
        border: 2px solid #e0e4ec !important;

        /* Wyśrodkowanie tekstu wewnątrz idealnego kwadratu */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0px !important;
    }

    /* Zmiana koloru ramki po najechaniu myszką */
    div[data-testid="stButton"] button:hover {
        border-color: #ff4b4b !important;
    }
    </style>
""", unsafe_allow_html=True)


# Generujemy 3 rzędy, a w każdym po 3 kolumny
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        cell_value = st.session_state.board[index]

        button_label = cell_value if cell_value != "" else " "
        button_disabled = cell_value != "" or st.session_state.winner is not None

        # Wyświetlamy przyciski w kolumnach
        with cols[col]:
            if st.button(button_label, key=f"cell_{index}", disabled=button_disabled):
                make_move(index)
                st.rerun()

st.write("")  # Odstęp

# Przycisk restartu
col_l, col_btn, col_r = st.columns([1, 2, 1])
with col_btn:
    if st.button("🔄 Zagraj od nowa", use_container_width=True):
        reset_game()
        st.rerun()

st.divider()
st.caption("Relaks po nauce")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
