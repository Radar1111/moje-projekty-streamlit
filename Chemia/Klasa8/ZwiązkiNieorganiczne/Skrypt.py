import streamlit as st

# Konfiguracja strony
st.set_page_config(
    page_title="Chemia Klasa 8 - Związki Nieorganiczne",
    page_icon="🧪",
    layout="wide"
)

# Tytuł
st.title("🧪 Interaktywna Chemia - Klasa 8")
st.markdown("""
Witaj w aplikacji wspierającej naukę chemii! Znajdziesz tu najważniejsze zagadnienia dotyczące 
**tlenków, wodorków, wodorotlenków, kwasów oraz dysocjacji elektrolitycznej**.
""")

# Pasek boczny
st.sidebar.header("🗺️ Menu Lekcji")
temat = st.sidebar.radio(
    "Wybierz zagadnienie:",
    [
        "1. Tlenki i Wodorki",
        "2. Wodorotlenki (NaOH, KOH, Ca(OH)2)",
        "3. Kwasy Tlenowe i Beztlenowe",
        "4. Wskaźniki i Odczyn pH",
        "5. Dysocjacja Elektrolityczna",
        "6. Quiz Chemiczny"
    ]
)

# 1: TLENKI I WODORKI 
if temat == "1. Tlenki i Wodorki":
    st.header("🧱 1. Tlenki i Wodorki")

    tab1, tab2 = st.tabs(["🔹 Tlenki", "🔹 Wodorki"])

    with tab1:
        st.subheader("Tlenki")
        st.write("""
        **Tlenki** to związki chemiczne tlenu z innymi pierwiastkami (metalami lub niemetalami). 
        Ogólny wzór: **$E_nO_m$**

        * **Przykłady tlenków metali:** $CaO$ (tlenek wapnia), $Fe_2O_3$ (tlenek żelaza(III))
        * **Przykłady tlenków niemetali:** $CO_2$ (tlenek węgla(IV)), $SO_3$ (tlenek siarki(VI))

        **Otrzymywanie:** Najprostszą metodą jest bezpośrednia synteza (spalanie pierwiastka w tlenie):
        
        $$2Mg + O_2 \\rightarrow 2MgO$$, 
        
        $$S + O_2 \\rightarrow SO_2$$
        
        📊 **Stan skupienia tlenków (w temperaturze pokojowej):**
        * **Stałe:** Większość tlenków metali (np. tlenek wapnia $CaO$, tlenek żelaza(III) $Fe_2O_3$, tlenek magnezu $MgO$).
        * **Gazowe:** Wiele tlenków niemetali (np. tlenek węgla(IV) $CO_2$, tlenek siarki(IV) $SO_2$).
        * **Ciekłe:** Najpopularniejszym tlenkiem w stanie ciekłym jest woda, czyli tlenek wodoru ($H_2O$).

        🧪 **Charakter chemiczny tlenków (Reakcje z wodą):**
        * **Tlenki zasadowe** – reagują z wodą, tworząc wodorotlenki (zasady). Są to głównie tlenki aktywnych metali (z 1. i 2. grupy układu okresowego, oprócz berylu).
        
        $$CaO + H_2O \\rightarrow Ca(OH)_2$$
        * **Tlenki kwasowe** (bezwodniki kwasowe) – reagują z wodą, tworząc kwasy tlenowe. Są to głównie tlenki niemetali.
        
        $$CO_2 + H_2O \\rightarrow H_2CO_3$$
        * **Tlenki obojętne** – nie reagują z wodą, nie tworzą kwasów ani zasad (np. tlenek węgla(II) $CO$, tlenek azotu(II) $NO$).
        """)

    with tab2:
        st.subheader("Wodorki")
        st.write("""
        **Wodorki** to związki chemiczne wodoru z innymi pierwiastkami (metalami lub niemetalami). 
        Ogólny wzór wodorków niemetali (grup 16-17) zapisujemy stawiając wodór na początku, np. **$H_nX$**, a grup 14-15 oraz metali stawiając wodór na końcu, np. **$EH_n$**. we wszystkich tych związkach **wodór ma zawsze wartościowość I**.

        * **Wodorki metali (grupy 1 i 2):** To związki o charakterze stałym.
            * $NaH$ – wodorek sodu
            * $CaH_2$ – wodorek wapnia

        * **Wodorki niemetali (grupy 14–17):** W temperaturze pokojowej są zazwyczaj gazami. Bardzo często posiadają popularne nazwy zwyczajowe, które musisz znać:
            * $HCl$ – chlorowodór (wodorek chloru)
            * $H_2S$ – siarkowodór (wodorek siarki)
            * $NH_3$ – amoniak (wodorek azotu)
            * $CH_4$ – metan (wodorek węgla)
            * $H_2O$ – woda (wodorek tlenu – choć rzadko się go tak nazywa!)

        💡 **Ważne dla ósmoklasisty:** 
        Gazy takie jak chlorowodór ($HCl$) czy siarkowodór ($H_2S$) doskonale rozpuszczają się w wodzie. Ich wodne roztwory to bardzo ważne kwasy beztlenowe: **kwas solny** oraz **kwas siarkowodorowy**! z kolei roztwór amoniaku ($NH_3$) w wodzie wykazuje odczyn zasadowy (woda amoniakalna).
        """)

# 2: WODOROTLENKI 
elif temat == "2. Wodorotlenki (NaOH, KOH, Ca(OH)2)":
    st.header("🧼 2. Wodorotlenki i Zasady")
    st.write("""
    **Wodorotlenki** to związki zbudowane z kationów metalu i anionów wodorotlenkowych. 
    Ogólny wzór: **$M(OH)_n$** (gdzie *n* to wartościowość metalu).
    **Zasady** to wodorotlenki dobrze rozpuszczalne w wodzie.
    """)

    wodorotlenek = st.selectbox("Wybierz wodorotlenek, aby poznać szczegóły:", ["NaOH", "KOH", "Ca(OH)2"])

    if wodorotlenek == "NaOH":
        st.subheader("🧪 Wodorotlenek sodu ($NaOH$) — Soda żrący")
        st.write("""
        * **Otrzymywanie:** Reakcja aktywnego metalu lub jego tlenku z wodą:
          
          $$2Na + 2H_2O \\rightarrow 2NaOH + H_2\\uparrow$$
          
          $$Na_2O + H_2O \\rightarrow 2NaOH$$
        * **Właściwości:** Ciało stałe, białe, higroskopijne (pochłania wilgoć z powietrza), doskonale rozpuszcza się w wodzie wydzielając ciepło (proces egzoenergetyczny), żrący.
        * **Zastosowanie:** Produkcja mydła, środków czyszczących (np. do rur "Kret"), papieru, szkła.
        """)
    elif wodorotlenek == "KOH":
        st.subheader("🧪 Wodorotlenek potasu ($KOH$) — Potaż żrący")
        st.write("""
        * **Otrzymywanie:** 
          
          $$2K + 2H_2O \\rightarrow 2KOH + H_2\\uparrow$$
          
          $$K_2O + H_2O \\rightarrow 2KOH$$
        * **Właściwości:** Białe ciało stałe, silnie higroskopijne, działa bardzo żrąco na skórę, świetnie rozpuszcza się w wodzie.
        * **Zastosowanie:** Produkcja mydeł w płynie (szarych), akumulatorów, preparatów do osuszania gazów.
        """)
    elif wodorotlenek == "Ca(OH)2":
        st.subheader("🧪 Wodorotlenek wapnia ($Ca(OH)_2$) — Wapno gaszone")
        st.write("""
        * **Otrzymywanie (Gaszenie wapna palonego):** 
          
          $$CaO + H_2O \\rightarrow Ca(OH)_2$$
        * **Właściwości:** Biały proszek, trudno rozpuszczalny w wodzie. Jego klarowny roztwór wodny to **woda wapienna** (mętnieje pod wpływem $CO_2$).
        * **Zastosowanie:** W budownictwie (składnik zaprawy murarskiej), w rolnictwie (bielenie drzewek, odkwaszanie gleb), cukrownictwo.
        """)

# 3: KWASY 
elif temat == "3. Kwasy Tlenowe i Beztlenowe":
    st.header("🍋 3. Kwasy")
    st.write("Kwasy zbudowane są z atomów wodoru i reszty kwasowej. Ogólny wzór: **$H_nR$**")

    kwas = st.selectbox("Wybierz kwas:", ["HCl (beztlenowy)", "HNO3 (tlenowy)", "H2SO4 (tlenowy)"])

    if kwas == "HCl (beztlenowy)":
        st.subheader("🧪 Kwas chlorowodorowy / solny ($HCl$)")
        st.write("""
        * **Otrzymywanie:** Najpierw otrzymuje się gazowy chlorowodór poprzez syntezę pierwiastków, a następnie rozpuszcza się go w wodzie:
          
          $$H_2 + Cl_2 \\rightarrow 2HCl_{(g)}$$
          
          $$HCl_{(g)} \\xrightarrow{H_2O} HCl_{(aq)}$$
        * **Właściwości:** Ciecz bezbarwna (stężony dymi na powietrzu), cięższy od wody, żrący, składnik soku żołądkowego.
        * **Zastosowanie:** Przemysł chemiczny, oczyszczanie powierzchni metali, produkcja barwników.
        """)
    elif kwas == "HNO3 (tlenowy)":
        st.subheader("🧪 Kwas azotowy(V) ($HNO_3$)")
        st.write("""
        * **Otrzymywanie:** W przemyśle przez katalityczne utlenianie amoniaku (metoda Ostwalda) i reakcję powstałego tlenku azotu(IV) z wodą i tlenem.
        * **Właściwości:** Bezbarwna ciecz, silne właściwości utleniające. Pod wpływem światła żółknie. **Powoduje żółknięcie białek (reakcja ksantoproteinowa)!**
        * **Zastosowanie:** Produkcja nawozów sztucznych (saletry), materiałów wybuchowych (TNT, nitrogliceryna), paliw rakietowych.
        """)
    elif kwas == "H2SO4 (tlenowy)":
        st.subheader("🧪 Kwas siarkowy(VI) ($H_2SO_4$) — Krew przemysłu")
        st.write("""
        * **Otrzymywanie:** Wieloetapowe: spalanie siarki do $SO_2$, utlenianie do $SO_3$, a następnie reakcja $SO_3$ z kwasem siarkowym i wodą.
          
          $$SO_3 + H_2O \\rightarrow H_2SO_4$$
        * **Właściwości:** Oleista, bezbarwna ciecz, znacznie cięższa od wody. **Silnie higroskopijny** (zwęgla substancje organiczne, wyciągając z nich wodę!).
        * **⚠️ PAMIĘTAJ CHEMIE MŁODY: WLEWAJ ZAWSZE KWAS DO WODY!** (Inaczej woda gwałtownie zawrze i pryśnie).
        * **Zastosowanie:** Akumulatory samochodowe, produkcja nawozów, środków piorących, sztucznych włókien.
        """)

# 4: WSKAŹNIKI I PH 
elif temat == "4. Wskaźniki i Odczyn pH":
    st.header("🌈 4. Wskaźniki kwasowo-zasadowe i pH")
    st.write("""
    **Skala pH** (od 0 do 14) określa stopień kwasowości lub zasadowości roztworu:
    * **pH < 7:** odczyn **kwasowy** (nadmiar jonów $H^+$)
    * **pH = 7:** odczyn **obojętny**
    * **pH > 7:** odczyn **zasadowy** (nadmiar jonów $OH^-$)
    """)

    st.subheader("🎛️ Symulator Wskaźników")
    st.info("Przesuń suwak pH, aby sprawdzić, jak zmieni się barwa najpopularniejszych wskaźników!")

    ph = st.slider("Wybierz wartość pH:", min_value=0.0, max_value=14.0, value=7.0, step=0.5)

    if ph < 7:
        odczyn = "KWASOWY 🍋"
        oranż = "🔴 Czerwony"
        fenolo = "⚪ Bezbarwny"
        lakmus = "🔴 Czerwony"
        uniwersalny = "🔴 Czerwony / Pomarańczowy"
    elif ph == 7:
        odczyn = "OBOJĘTNY 💧"
        oranż = "🟠 Pomarańczowy"
        fenolo = "⚪ Bezbarwny"
        lakmus = "🟪 Fioletowy"
        uniwersalny = "🟢 Zielony"
    else:
        odczyn = "ZASADOWY 🧼"
        oranż = "🟡 Żółty"
        fenolo = "🌸 Malinowy"
        lakmus = "🔵 Niebieski"
        uniwersalny = "🔵 Niebieski / Fioletowy"

    st.metric(label="Określony odczyn roztworu:", value=odczyn)

    # Wyświetlenie barw 
    dane_wskaznikow = {
        "Wskaźnik": ["Oranż metylowy", "Fenoloftaleina", "Papierek lakmusowy", "Uniwersalny papierek wskaźnikowy"],
        "Barwa w tym pH": [oranż, fenolo, lakmus, uniwersalny]
    }
    st.table(dane_wskaznikow)

#  5: DYSOCJACJA ELEKTROLITYCZNA 
elif temat == "5. Dysocjacja Elektrolityczna":
    st.header("⚡ 5. Dysocjacja Elektrolityczna")
    st.write("""
    **Dysocjacja elektrolityczna** to proces rozpadu elektrolitów (kwasów, zasad, soli) na jony pod wpływem cząsteczek wody.
    * **Kationy** — jony o ładunku dodatnim ($+$)
    * **Aniony** — jony o ładunku ujemnym ($-$)

    * **Kwasy** dysocjują na kationy wodoru ($H^+$) i aniony reszty kwasowej.
    * **Zasady** dysocjują na kationy metalu i aniony wodorotlenkowe ($OH^-$).
    """)

    st.subheader("⚙️ Interaktywny Generator Równań")
    wybierz_dysocjacje = st.selectbox("Wybierz substancję do zdysocjowania:",
                                      ["HCl", "H2SO4", "HNO3", "NaOH", "KOH", "Ca(OH)2"])

    rownania = {
        "HCl": "$$HCl \\xrightarrow{H_2O} H^+ + Cl^-$$",
        "H2SO4": "$$H_2SO_4 \\xrightarrow{H_2O} 2H^+ + SO_4^{2-}$$",
        "HNO3": "$$HNO_3 \\xrightarrow{H_2O} H^+ + NO_3^-$$",
        "NaOH": "$$NaOH \\xrightarrow{H_2O} Na^+ + OH^-$$",
        "KOH": "$$KOH \\xrightarrow{H_2O} K^+ + OH^-$$",
        "Ca(OH)2": "$$Ca(OH)_2 \\xrightarrow{H_2O} Ca^{2+} + 2OH^-$$"
    }

    st.markdown("**Równanie reakcji dysocjacji:**")
    st.markdown(rownania[wybierz_dysocjacje])

# 6: QUIZ CHEMICZNY 
elif temat == "6. Quiz Chemiczny":
    st.header("🧠 6. Szybki Test Wiedzy")
    st.write("Sprawdź, ile zapamiętałeś z materiału dla klasy 8!")

    # Pytanie 1
    q1 = st.radio(
        "1. Jaką barwę przyjmuje fenoloftaleina w roztworze o odczynie zasadowym ($pH > 7$)?",
        ["Bezbarwna", "Malinowa", "Żółta"]
    )

    # Pytanie 2
    q2 = st.radio(
        "2. Który kwas powoduje żółknięcie białek (reakcja ksantoproteinowa)?",
        ["Kwas solny ($HCl$)", "Kwas siarkowy(VI) ($H_2SO_4$)", "Kwas azotowy(V) ($HNO_3$)"]
    )

    # Pytanie 3
    q3 = st.radio(
        "3. Na jakie jony dysocjują wszystkie zasady?",
        ["Kationy wodoru ($H^+$)", "Aniony wodorotlenkowe ($OH^-$)", "Aniony reszty kwasowej"]
    )

    # Pytanie 4 (Tlenki / Charakter chemiczny)
    q4 = st.radio(
        "4. Który z podanych tlenków reaguje z wodą, tworząc kwas (jest tlenkiem kwasowym)?",
        ["$CO_2$ (tlenek węgla(IV))", "$CaO$ (tlenek wapnia)", "$CO$ (tlenek węgla(II))"]
    )

    # Pytanie 5 (Wodorki / Kwasy beztlenowe)
    q5 = st.radio(
        "5. Gazowy chlorowodór ($HCl_{(g)}$) po rozpuszczeniu w wodzie tworzy kwas o nazwie zwyczajowej:",
        ["Kwas siarkowodorowy", "Kwas solny", "Kwas azotowy"]
    )

    # Pytanie 6 (Właściwości wodorotlenków)
    q6 = st.radio(
        "6. Substancja, która silnie pochłania wilgoć z otoczenia (np. stały $NaOH$), ma właściwości:",
        ["Egzoenergetyczne", "Utleniające", "Higroskopijne"]
    )

    # Pytanie 7 (Bezpieczeństwo)
    q7 = st.radio(
        "7. Jaka jest poprawna i bezpieczna metoda rozcieńczania stężonego kwas siarkowego(VI)?",
        ["Wlewanie wody do kwasu", "Wlewanie kwasu do wody", "Kolejność nie ma znaczenia"]
    )

    # Pytanie 8 (Dysocjacja / Jony)
    q8 = st.radio(
        "8. Ile kationów wodoru ($H^+$) powstanie podczas pełnej dysocjacji jednej cząsteczki $H_2SO_4$?",
        ["1 kation", "2 kationy", "4 kationy"]
    )

    # Pytanie 9 (Reakcje identyfikacyjne)
    q9 = st.radio(
        "9. Klarowna woda wapienna (roztwór $Ca(OH)_2$) mętnieje pod wpływem gazu o wzorze:",
        ["$O_2$", "$H_2$", "$CO_2$"]
    )

    # Zliczanie punktów i sprawdzanie wyniku po kliknięciu przycisku
    if st.button("Sprawdź wynik! 🎯"):
        punkty = 0

        # Sprawdzanie poprawności
        if q1 == "Malinowa": punkty += 1
        if q2 == "Kwas azotowy(V) ($HNO_3$)": punkty += 1
        if q3 == "Aniony wodorotlenkowe ($OH^-$)": punkty += 1
        if q4 == "$CO_2$ (tlenek węgla(IV))": punkty += 1
        if q5 == "Kwas solny": punkty += 1
        if q6 == "Higroskopijne": punkty += 1
        if q7 == "Wlewanie kwasu do wody": punkty += 1
        if q8 == "2 kationy": punkty += 1
        if q9 == "$CO_2$": punkty += 1

        st.write(f"Twój wynik: **{punkty} / 9**")

        # Progi punktowe dostosowane do 9 pytań
        if punkty == 9:
            st.balloons()
            st.success("Wspaniale! Klasa 8 z chemii opanowana śpiewająco! Pełna pula punktów! 🥇")
        elif punkty >= 6:
            st.warning(f"Dobry wynik! ({punkty}/9). Przejrzyj jeszcze raz tematy, w których pojawiły się błędy. 📚")
        else:
            st.error("Wróć do teorii w menu, powtórz materiał i spróbuj ponownie! Dasz radę! 💪")
