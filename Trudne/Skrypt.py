import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(
    page_title="Cechy Języków Trudnych",
    page_icon="🌐",
    layout="wide",
)

# Główny nagłówek
st.title("🌐 Unikalne Cechy Trudnych Języków Świata")
st.markdown("Interaktywne podsumowanie najważniejszych zasad fonetycznych, gramatycznych i piśmienniczych omawianych języków")

# Tabela porównawcza
st.header("📊 Szybkie porównanie (w pigułce)")

data = {
    "Język": ["Chiński (Mandaryński)", "Koreański", "Japoński", "Arabski", "Hindi"],
    "Czy intonacja zmienia znaczenie?": [
        "Tak! (Aż 4 różne tony dla jednego słowa)",
        "Nie (Wpływa tylko na emocje w zdaniu)",
        "Trochę (Wyznacza melodię słowa: wysoko/nisko)",
        "Nie",
        "Nie"
    ],
    "Jak to się pisze?": [
        "Skomplikowane znaki (Hanzi)",
        "Genialne klocki z liter (Hangul)",
        "Mieszanka 3 pism (Kanji, Hiragana, Katakana)",
        "Od prawej do lewej, same spółgłoski",
        "Litery zawieszone na linii (Dewanagari)"
    ],
    "Największe zaskoczenie": [
        "Pomylisz ton i powiesz 'koń' zamiast 'mama'",
        "Końcówki słów zależą od tego, z kim rozmawiasz",
        "Przedłużenie dźwięku całkowicie zmienia słowo",
        "Słowa buduje się z paczki 3 spółgłosek",
        "Czasownik zawsze ląduje na samym końcu zdania"
    ]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)
st.write("---")

# Sekcja szczegółowe opisy
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chiński", "Koreański", "Japoński", "Arabski", "Hindi"])

with tab1:
    st.subheader("🇨🇳 Język Chiński – Język muzyczny")
    st.markdown("""
    * **Jedno słowo, cztery znaczenia:** To samo słowo (np. *ma*) wypowiedziane z inną intonacją oznacza zupełnie coś innego. Jeśli się pomylisz, zamiast „mama” powiesz... „koń”.
    * **Jak to działa w praktyce?**
        * *mā* (głos płaski i wysoki, jak u dentysty: „aaa”) = **matka**
        * *má* (głos idzie w górę, jakbyś zadawał zdziwione pytanie: „Mhm?”) = **konopie**
        * *mǎ* (głos najpierw spada, a potem idzie w górę, jak przy wahaniu: „Nooo...”) = **koń**
        * *mà* (głos gwałtownie spada, jakbyś rzucał krótki rozkaz: „Siad!”) = **karcić**
    """)

with tab2:
    st.subheader("🇰🇷 Język Koreański – Szacunek i klocki z liter")
    st.markdown("""
    * **Gramatyka pełna szacunku:** W koreańskim nie możesz po prostu powiedzieć „biorę”. Końcówka słowa całkowicie się zmienia w zależności od tego, czy rozmawiasz z młodszym kolegą, szefem w pracy, czy babcią.
    * **Genialny alfabet (Hangul):** To nie są chińskie znaki! Koreańczycy mają alfabet podobny do naszego, ale zamiast pisać litery obok siebie (l-i-s-t), zbijają je w kwadratowe „klocki-sylaby”. Co ciekawe, kształt liter (np. ㄴ czy ㄱ) naśladuje to, jak układa się Twój język w ustach podczas mówienia!
    """)

with tab3:
    st.subheader("🇯🇵 Język Japoński – Trzy pisma na raz i dłuuugie dźwięki")
    st.markdown("""
    * **Melodia zamiast akcentu:** Japończycy nie akcentują słów tak mocno jak Polacy (głośniej/ciszej). Oni zmieniają wysokość tonu. Przykładowo: słowo *hási* (wysoko-nisko) to **pałeczki**, ale *hasí* (nisko-wysoko) to **most**.
    * **Pułapka długich samogłosek (Iloczas):** Trzymanie dźwięku sekwencję dłużej całkowicie zmienia słowo. Powiesz krótko *ojisan* i witasz **wujka**. Przeciągniesz dźwięk: *ojiisan* – i nagle rozmawiasz z **dziadkiem**.
    * **Piekło piśmiennicze:** Japończycy w jednym zdaniu potrafią mieszać aż trzy systemy pisma: chińskie znaki (dla pojęć), zaokrąglone literki (do gramatyki) i kanciaste literki (do słów z importu, np. „komputer”).
    """)

with tab4:
    st.subheader("🇦🇪 Język Arabski – Matematyka i dźwięki z głębi gardła")
    st.markdown("""
    * **Słowne klocki LEGO (System rdzeni):** Wszystkie słowa buduje się z paczki trzech spółgłosek. Weźmy rdzeń **K-T-B** (związany z pisaniem). Wrzucasz między te litery różne samogłoski i masz: *kitab* (książka), *maktab* (biurko), *kataba* (on napisał). Znasz 3 litery i nagle rozumiesz 20 słów!
    * **Mówienie z głębi gardła:** Arabski ma mnóstwo dźwięków „gardłowych”. Brzmią one dla nas, jakby ktoś głęboko charczał lub próbował przeczyścić gardło.
    * **Pismo od tyłu:** Pisze się od prawej do lewej, a w gazetach czy książkach prawie w ogóle nie zapisuje się krótkich samogłosek (a, e, i, o, u) – czytelnik musi się ich domyślić z kontekstu!
    """)

with tab5:
    st.subheader("🇮🇳 Język Hindi – Wydech, podwinięty język i czasownik na końcu")
    st.markdown("""
    * **Mówienie z wydechem (Przydech):** Istnieje ogromna różnica między zwykłym „p”, a „ph”. To drugie musisz wypowiedzieć z tak silnym podmuchem powietrza z ust, żeby zdmuchnąć świeczkę.
    * **Gimnastyka języka:** Niektóre dźwięki (jak „t” czy „d”) wymagają mocnego wygięcia języka do tyłu i uderzenia nim o podniebienie. Brzmi to trochę jak u postaci z filmów z Bollywood.
    * **Wszystko na opak (Szyk SOV):** W hindi czasownik zawsze ląduje na samym końcu zdania. Zamiast powiedzieć: *„Ja piję wodę”*, powiesz: *„Ja wodę piję”*.
    """)
