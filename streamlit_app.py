import streamlit as st

st.sidebar.title('Blog categorieën')
blog_post = st.sidebar.selectbox(
    'Selecteer een onderwerp',
    ('Introductie', 'Drukte voor vluchten op verschillende luchthavens', 'Informatie over vertraging', 'Voorspellingsmodel voor vertraging', 'Vertraging in de wereld'
))

st.title('Vertragingen en drukte voor vluchten op verschillende luchthavens in 2019 en 2020')
st.write('Voor luchtvaartmaatschappijen, luchthavens en reizigers zijn vertraging en drukte twee grote struikelblokken. Het bijhouden van data van elke vlucht is cruciaal om een beter inzicht te krijgen van deze twee onderwerpen. Ons doel was om een beter beeld te creëeren van deze drukte en een voorspelling te doen over de vertraging aan de hand van verschillende factoren.')
st.write("Hiervoor is gebruik gemaakt van verschillende datasets. Hiermee zijn een aantal grafieken gecreëerd die de drukte per geselecteerde regio visualiseren. Daarnaast zijn er grafieken en kaarten gecreëerd die de vertraging op Luchthaven X visualiseren. Met behulp van de interactieve functies kunnen gebruikers eenvoudig de vertraging of drukte analyseren.")

# ======================================================================================================================================================================

if blog_post == 'Introductie':

    st.header('Inleiding')
    st.write("Dit dashboard biedt een overzicht van de vertragingen op verschillende luchthavens en een de drukte op andere geselecteerde regio's. Het doel van dit dashboard is om gebruikers te voorzien van inzichten over de vertragingen op de luchthaven. Daarnaast bieden wij een beter beeld van de connecties van Luchthaven X en alle andere luchthavens tussen 2019 en 2020.")
    st.subheader('Functies van het dashboard')
    st.markdown(
        """
        1. **Drukte voor vluchten op verschillende luchthavens**: In deze blogpost wordt de drukte op verschillende luchthavens in relatie met Luchthaven Xweergegeven per maand. U kunt hier eenvoudig wisselen tussen landen en luchthavens om de data voor specifieke luchthavens te bekijken. Ook kan er geschoven worden in het aantal maanden dat wordt gevisualiseerd.
        2. **Informatie over vertraging**: Analyseer de vertraging op verschillende luchthavens van vluchten van of naar Luchthaven X. Deze blogpost geeft een eerste indruk van de vertraging tussen de grootste vertragingen. Daarnaast kunt u verklaringen vinden voor deze enorme vertragingen.
        3. **Voorspellingsmodel voor vertraging**: Voorspel de vertraging van vluchten van of naar Luchthaven X aan de hand van verschillende factoren. U kunt hier kiezen tussen wat voor voorspellingsmodel u wilt toepassen.
        4. **Vertraging in de wereld**: Krijg een indruk van de vertraging de vluchten van of naar Luchthaven X binnen Europa en andere continenten. Deze visualisatie maakt het mogelijk om te zien welke luchthavens meer vertraging oplopen als er een vlucht is tussen hen en Luchthaven X.
        """
    )
    st.subheader('Hoe het dashboard te gebruiken')
    st.markdown(
        """
        - Selecteer een **land** en een **luchthaven** in de dropdown-menu's om de data tussen verschillende luchthavens te bekijken.
        - Gebruik de **slider** om data voor verschillende maanden te bekijken.
        - Selecteer een **voorspellingsmodel** in de dropdown-menu's om de vertraging van vluchten tussen Luchthaven X en een andere luchthaven te bekijken. Hier zal ook een accuracy score of een MSE volgen, afhankelijk van het type voorspellingsmodel.
        - Ga op een **luchthaven** staan op de kaart om meer informatie te krijgen over de vertraging van de luchthaven
        """
    )
    st.subheader('Discussie over Data Kwaliteit')
    st.write('De datasets, die in deze analyses zijn gebruikt, bevat ontbrekende waarden, wat betekent dat alle statistiek niet volledig zijn vertegenwoordigd. Dit vormt dus slechts een basis voor een nauwkeurige analyse van Luchthaven X en zijn vertraging met betrekking op andere luchthavens. Het aantal ontbrekende waarden was dusdanig laag dat deze zijn verwijderd uit de dataset.')
    st.write('Door de volledigheid en betrouwbaarheid van de data te waarborgen, zullen de inzichten die uit dit dashboard worden getrokken waarschijnlijk een goede weerspiegeling geven van een luchthaven van gemiddelde grootte in de wereld en Europa.')

# ======================================================================================================================================================================

elif blog_post == 'Drukte voor vluchten op verschillende luchthavens':
    st.header('Drukte voor vluchten op verschillende luchthavens')
    st.write('Het aantal vliegtuigen op een luchthaven blijft een belangrijke statistiek voor alle luchthavens. Hierdoor wordt de drukte bepaald, maar kan er ook gekeken worden of er nog vluchten bij kunnen. Door de gegevens van 2019 en 2020 te analyseren krijgen we een beter beeld van de drukte in deze tijd. Dit kan beleidsmakers helpen beter geïnformeerde beslissingen te nemen over roosters of andere ondwerpen.')
    st.write('Kies hieronder een land en een luchthaven en beweeg de slider om een tijdsperiode te bepalen. De grafiek zal het aantal vliegtuigen op de luchthaven weergeven die van of naar Luchthaven X zijn gevlogen.')
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px

    airports_extended_clean = pd.read_csv('airports-extended-clean.csv', sep =";")
    schedule_airports = pd.read_csv('schedule_airport.csv')

    df_merged = schedule_airports.merge(airports_extended_clean, left_on='Org/Des', right_on='ICAO', how='inner')
    df_merged = df_merged.replace('-', np.nan)

    del df_merged['DL1']
    del df_merged['IX1']
    del df_merged['DL2']
    del df_merged['IX2']
    del df_merged['Source']
    del df_merged['DST']
    del df_merged['RWC']

    df_merged['STD'] = df_merged['STD'].str.replace('/', '-')
    df_merged['STD'] = pd.to_datetime(df_merged['STD'], format='%d-%m-%Y')

    df_merged = df_merged.rename(columns={
        'STD':'Datum', 
        'FLT':'Vlucht nummer',
        'STA_STD_ltc':'Geplande aankomst',
        'ATA_ATD_ltc':'Werkelijke aankomst',
        'LSV':'Inkomend of uitgaand',
        'TAR':'Geplande gate',
        'GAT':'Werkelijke gate',
        'ACT':'Vliegtuig type',
        'Org/Des':'Bestemming/afkomst',
        'Name':'Luchthaven',
        'City':'Stad',
        'Country':'Land',
        'Timezone':'Timezone uren',
        'Tz':'Timezone continent/stad',
        'Type':'Type transport'
    })

    df_merged['Geplande aankomst'] = pd.to_datetime(df_merged['Geplande aankomst'], format='%H:%M:%S')
    df_merged['Werkelijke aankomst'] = pd.to_datetime(df_merged['Werkelijke aankomst'], format='%H:%M:%S')

    df_merged['Vertraging'] = (df_merged['Werkelijke aankomst'] - df_merged['Geplande aankomst']).dt.total_seconds() / 60
    df_merged['Vertraging (minuten)'] = np.where(df_merged['Vertraging'] > 0, df_merged['Vertraging'].abs(), 0)
    df_merged['Op tijd (minuten)'] = np.where(df_merged['Vertraging'] < 0, df_merged['Vertraging'].abs(), 0)
    df_merged['Vertraging (minuten)'] = df_merged['Vertraging (minuten)'].apply(lambda x: f"{x:.2f} minuten" if x > 0 else "0 minuten")
    df_merged['Op tijd (minuten)'] = df_merged['Op tijd (minuten)'].apply(lambda x: f"{x:.2f} minuten" if x > 0 else "0 minuten")

    df_merged = df_merged.dropna()

    df_lijn = df_merged[['Datum', 'Land', 'Luchthaven']]
    df_lijn.groupby(['Land', 'Luchthaven'])
    df_lijn.groupby(['Datum'])
    df_lijn.reset_index(drop=True, inplace=True)


    import plotly.graph_objects as go
    import streamlit as st

    df_lijn['Aantal vliegtuigen op de luchthaven'] = 1
    df_lijn_maand = df_lijn.groupby([pd.Grouper(key='Datum', freq='M'), 'Land', 'Luchthaven']).agg(
        {'Aantal vliegtuigen op de luchthaven':'sum'}).reset_index()

    import streamlit as st
    import plotly.graph_objects as go

    land_selectie = st.selectbox('Selecteer een land', df_lijn_maand['Land'].unique())
    df_lijn_maand_gefilterd_land = df_lijn_maand[df_lijn_maand['Land'] == land_selectie]

    luchthaven_selectie = st.selectbox('Selecteer een luchthaven', df_lijn_maand_gefilterd_land['Luchthaven'].unique())
    df_lijn_maand_gefilterd_luchthaven = df_lijn_maand_gefilterd_land[df_lijn_maand_gefilterd_land['Luchthaven'] == luchthaven_selectie]

    max_waarde = len(df_lijn_maand_gefilterd_luchthaven)
    slider_waarde = st.slider('Selecteer hoeveel maanden je wilt tonen: ', min_value = 0, max_value = max_waarde, value = max_waarde)
    df_lijn_maand_gefilterd_luchthaven_slider = df_lijn_maand_gefilterd_luchthaven.iloc[:slider_waarde]

    if not df_lijn_maand_gefilterd_luchthaven_slider.empty:
        
        fig_lijn = go.Figure()
        
        fig_lijn.add_trace(go.Bar(
            x = df_lijn_maand_gefilterd_luchthaven_slider['Datum'],
            y = df_lijn_maand_gefilterd_luchthaven_slider['Aantal vliegtuigen op de luchthaven'],
            marker_color = 'indianred',
            opacity = .5
        ))

        fig_lijn.add_trace(go.Scatter(
            x = df_lijn_maand_gefilterd_luchthaven_slider['Datum'],
            y = df_lijn_maand_gefilterd_luchthaven_slider['Aantal vliegtuigen op de luchthaven'],
            mode = 'lines+markers'
        ))
        
        fig_lijn.update_layout(
            title = f'Aantal vliegtuigen op {luchthaven_selectie} in {land_selectie}',
            xaxis_title = 'Datum',
            yaxis_title = 'Aantal vliegtuigen',
            template = 'plotly_white',
            showlegend = False
        )

        if df_lijn_maand_gefilterd_luchthaven_slider['Aantal vliegtuigen op de luchthaven'].sum() == 0:
            st.write(f'Geen data beschikbaar voor {luchthaven_selectie} in {land_selectie} voor deze periode')
        else:
            st.plotly_chart(fig_lijn)
    
    st.subheader('Vluchten in de coronacrisis')
    st.write('In de bovenstaande grafiek is voor veel luchthavens een daling te zien rond Februari 2020/Maart 2020. Dit was het moment dat de coronacrisis begon. Hierdoor vlogen er veel minder vluchten van en naar Luchthaven X. Daarom is ook het aantal vliegtuigen op de luchthaven aanzienlijk minder dan eerdere maanden.')
    st.write('Om hier een beter beeld van te krijgen, is een grafiek gemaakt die hier extra op inzoomt. Kies hieronder een land en een luchthaven om een beter beeld te krijgen van de impact van de coronacrisis op het aantal vluchten.')


    df_lijn_maand_corona = pd.concat([df_lijn_maand[df_lijn_maand['Datum'] == '2020-01-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-02-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-03-31'],
                            df_lijn_maand[df_lijn_maand['Datum'] == '2020-04-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-05-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-06-31'],
                            df_lijn_maand[df_lijn_maand['Datum'] == '2020-07-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-08-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-09-31'],
                            df_lijn_maand[df_lijn_maand['Datum'] == '2020-10-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-11-31'], df_lijn_maand[df_lijn_maand['Datum'] == '2020-12-31']])

    land_selectie_corona = st.selectbox('Selecteer een land', df_lijn_maand_corona['Land'].unique(), key='land_selectie_corona')
    df_lijn_maand_corona_gefilterd_land = df_lijn_maand_corona[df_lijn_maand_corona['Land'] == land_selectie_corona]

    luchthaven_selectie_corona = st.selectbox('Selecteer een luchthaven', df_lijn_maand_corona_gefilterd_land['Luchthaven'].unique(), key='luchthaven_selectie_corona')
    df_lijn_maand_corona_gefilterd_luchthaven = df_lijn_maand_corona_gefilterd_land[df_lijn_maand_corona_gefilterd_land['Luchthaven'] == luchthaven_selectie_corona]


    if not df_lijn_maand_corona_gefilterd_luchthaven.empty:

        fig_lijn_corona = go.Figure()

        fig_lijn_corona.add_trace(go.Bar(
            x=df_lijn_maand_corona_gefilterd_luchthaven['Datum'],
            y=df_lijn_maand_corona_gefilterd_luchthaven['Aantal vliegtuigen op de luchthaven'],
            marker_color='cadetblue',
            opacity=.5
        ))

        fig_lijn_corona.add_trace(go.Scatter(
            x=df_lijn_maand_corona_gefilterd_luchthaven['Datum'],
            y=df_lijn_maand_corona_gefilterd_luchthaven['Aantal vliegtuigen op de luchthaven'],
            mode='lines+markers'
        ))

        fig_lijn_corona.update_layout(
            title = f'Aantal vliegtuigen op {luchthaven_selectie_corona} in {land_selectie_corona} tijdens de eerste en tweede COVID-19 golf',
            xaxis_title = 'Datum',
            yaxis_title = 'Aantal vliegtuigen',
            template = 'plotly_white',
            showlegend = False
        )

        if df_lijn_maand_corona_gefilterd_luchthaven['Aantal vliegtuigen op de luchthaven'].sum() == 0:
            st.write(f'Geen data beschikbaar voor {luchthaven_selectie_corona} in {land_selectie_corona} voor deze periode')
        else:
            st.plotly_chart(fig_lijn_corona)
    
    st.write('Voor veel luchthavens er een daling te zien zijn rond Maart 2020. Dit was tijdens de eerste golf van COVID-19. Voor een aantal luchthavens zal ook nog een daling te zien zijn rond Oktober 2020. Dit was het moment van de tweede coronagolf.')
    st.subheader('Disclaimer')
    st.write('Voor sommige maanden bevat de dataset geen waarden. In het lijndiagram zal de lijn constant doorlopen totdat er wel weer data beschikbaar is. Zo lijkt het alsof er een constant aantal vluchten was terwijl dit eigenlijk onbekend is.')

# ======================================================================================================================================================================

elif blog_post == 'Informatie over vertraging':
    st.header('Inzicht in Vertragingen per Land – Een Data-gedreven Analyse')
    st.write('Vluchtvertragingen kunnen een grote bron van frustratie zijn voor reizigers en leiden vaak tot gemiste aansluitingen, gewijzigde plannen of simpelweg ongemak. Met de groei van het wereldwijde luchtverkeer blijven vertragingen een grote uitdaging voor luchtvaartmaatschappijen, passagiers en de luchtvaartsector als geheel. In deze analyse willen we de positieve vluchtvertragingen (vertragingen die daadwerkelijk hebben plaatsgevonden) en hun verdeling over verschillende landen beter begrijpen. De onderstaande grafiek toont de verdeling van positieve vertragingstijden voor de top 10 landen met betrekking tot vluchtvertragingen.')
    st.subheader('Overzicht van de verdelingen')
    st.write('De grafiek maakt gebruik van boxplots om de verdeling van vertragingstijden, gemeten in minuten, per land te tonen. Boxplots zijn erg nuttig om belangrijke statistische gegevens weer te geven: de mediaan, interkwartielafstand (IQR) en de minimum- en maximumwaarden (exclusief uitbijters). Hier is een uitleg van wat deze elementen laten zien:')
    st.markdown(
        """
        - Mediaan (horizontale lijn in de box): Dit geeft de middelste waarde van de vertragingen weer, en geeft een goede indicatie van de typische vertragingstijd in elk land.
        - Interkwartielafstand (IQR): Dit wordt weergegeven door de grootte van de box, en laat de spreiding zien van de middelste 50% van de vertragingstijden. Een grotere IQR betekent meer variatie in de vertragingstijden.
        - Whiskers (lijnen aan de boven- en onderkant van de box): Deze tonen het bereik van de data, waarbij de minimum- en maximumwaarden worden aangegeven (exclusief eventuele uitbijters).
        """
    )

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px
    import plotly.graph_objects as go
    import streamlit as st
    from datetime import datetime

    airports_extended_clean = pd.read_csv('airports-extended-clean.csv', sep =";")
    schedule_airports = pd.read_csv('schedule_airport.csv')

    df_merged = schedule_airports.merge(airports_extended_clean, left_on='Org/Des', right_on='ICAO', how='inner')
    df_merged= df_merged.replace('-', np.nan)

    del df_merged['DL1']
    del df_merged['IX1']
    del df_merged['DL2']
    del df_merged['IX2']
    del df_merged['Source']
    del df_merged['DST']
    del df_merged['RWC']

    df_merged['STD'] = df_merged['STD'].str.replace('/', '-')
    df_merged['STD'] = pd.to_datetime(df_merged['STD'], format='%d-%m-%Y')

    df_merged = df_merged.rename(columns={
        'STD':'Datum', 
        'FLT':'Vlucht nummer',
        'STA_STD_ltc':'Geplande aankomst',
        'ATA_ATD_ltc':'Werkelijke aankomst',
        'LSV':'Inkomend of uitgaand',
        'TAR':'Geplande gate',
        'GAT':'Werkelijke gate',
        'ACT':'Vliegtuig type',
        'Org/Des':'Bestemming/afkomst',
        'Name':'Luchthaven',
        'City':'Stad',
        'Country':'Land',
        'Timezone':'Timezone uren',
        'Tz':'Timezone continent/stad',
        'Type':'Type transport'
    })

    df_merged['Geplande aankomst'] = pd.to_datetime(df_merged['Geplande aankomst'], format='%H:%M:%S')
    df_merged['Werkelijke aankomst'] = pd.to_datetime(df_merged['Werkelijke aankomst'], format='%H:%M:%S')
    df_merged['Vertraging'] = (df_merged['Werkelijke aankomst'] - df_merged['Geplande aankomst']).dt.total_seconds() / 60
    df_merged['Vertraging (minuten)'] = np.where(df_merged['Vertraging'] > 0, df_merged['Vertraging'].abs(), 0)
    df_merged['Op tijd (minuten)'] = np.where(df_merged['Vertraging'] < 0, df_merged['Vertraging'].abs(), 0)
    df_merged['Vertraging (minuten)'] = df_merged['Vertraging (minuten)'].apply(lambda x: f"{x:.2f}" if x > 0 else "0.0")
    df_merged['Op tijd (minuten)'] = df_merged['Op tijd (minuten)'].apply(lambda x: f"{x:.2f}" if x > 0 else "0.0")
    df_merged['Geplande aankomst'] = df_merged['Geplande aankomst'].dt.time
    df_merged['Werkelijke aankomst'] = df_merged['Werkelijke aankomst'].dt.time

    df_merged = df_merged.dropna()
    data_vertraging = df_merged["Vertraging (minuten)"]
    data_optijd = df_merged["Op tijd (minuten)"]
    data_split_vertraging = [val.replace(',', '.').split('.') for val in data_vertraging]
    data_split_optijd = [val.replace(',', '.').split('.') for val in data_optijd]
    df_vertraging = pd.DataFrame(data_split_vertraging, columns=['minutes', 'seconds'])
    df_optijd = pd.DataFrame(data_split_optijd, columns=['minutes', 'seconds'])
    df_vertraging['minutes'] = pd.to_numeric(df_vertraging['minutes'])
    df_vertraging['seconds'] = pd.to_numeric(df_vertraging['seconds'])
    df_optijd['minutes'] = pd.to_numeric(df_optijd['minutes'])
    df_optijd['seconds'] = pd.to_numeric(df_optijd['seconds'])
    df_vertraging['total_seconds'] = df_vertraging['minutes'] * 60 + df_vertraging['seconds']
    df_optijd['total_seconds'] = df_optijd['minutes'] * 60 + df_optijd['seconds']
    df_vertraging['time'] = pd.to_timedelta(df_vertraging['total_seconds'], unit='s')
    df_optijd['time'] = pd.to_timedelta(df_optijd['total_seconds'], unit='s')
    df_merged["Vertraging (minuten)"] = df_vertraging['time']
    df_merged["Op tijd (minuten)"] = df_optijd['time'] 

    uitschieters = df_merged[df_merged['Vertraging'] > 60]
    top_10_landen = uitschieters['Land'].value_counts().head(10).index
    uitschieters_top_10 = uitschieters[uitschieters['Land'].isin(top_10_landen)]
    vertragingen_per_datum = uitschieters_top_10.groupby(['Land', 'Datum']).size().reset_index(name='Aantal_Vertragingen')
    vertragingen_per_datum = vertragingen_per_datum.sort_values(by=['Land', 'Aantal_Vertragingen'], ascending=False)
    
    positive_delay = df_merged[df_merged['Vertraging'] > 0]

    top_countries = positive_delay['Land'].value_counts().head(10).index
    top_positive_delay = positive_delay[positive_delay['Land'].isin(top_countries)]
    mean_delays = top_positive_delay.groupby('Land')['Vertraging'].mean().reset_index()
    mean_delays['Threshold'] = mean_delays['Vertraging'] * 1.5
    outlier_countries = top_positive_delay[top_positive_delay['Vertraging'] > 200]['Land'].unique()

    for country in outlier_countries:
        mean_threshold = mean_delays[mean_delays['Land'] == country]['Threshold'].values[0]
        mean_delays.loc[mean_delays['Land'] == country, 'Threshold'] = mean_threshold

    max_threshold = mean_delays['Threshold'].max()

    fig = px.box(top_positive_delay, 
                x='Land', 
                y='Vertraging', 
                title='Verdeling van Positieve Vertraging per Top 10 Landen',
                labels={'Vertraging': 'Vertraging (minuten)', 'Land': 'Land'},
                points='outliers') 

    fig.update_traces(boxpoints=False)  
    fig.update_yaxes(range=[0, max_threshold])  
    fig.update_layout(xaxis_title='Land',
                    yaxis_title='Vertraging (minuten)',
                    xaxis_tickangle=-45)

    st.plotly_chart(fig)

    st.header('Analyseren van Lange Vertragingen per Land en Datum')
    st.write('Vluchtvertragingen zijn niet alleen ongemakkelijk, maar lange vertragingen kunnen ook aanzienlijke verstoringen in reisplannen veroorzaken. In deze visualisatie onderzoeken we lange vluchtvertragingen van meer dan 60 minuten en hoe deze vertragingen zich hebben ontwikkeld tussen 2019 en 2021, verdeeld over verschillende landen.')
    st.subheader('Scatterplot: Totale Vertraging per Land en Datum')
    st.write('De grafiek hieronder is een scatterplot die de totale vertraging in minuten per dag toont, voor verschillende landen die vertragingen hebben ervaren van meer dan 60 minuten. Elk punt in de grafiek vertegenwoordigt een dag met grote vertragingen. De grootte van de stip geeft aan hoeveel minuten vertraging er op die dag opgeteld zijn voor een specifiek land. Hieronder volgt een uitleg van de belangrijkste elementen:')
    st.markdown(
        """
        - Tijdlijn (X-as): De tijdsperiode loopt van januari 2019 tot december 2020, wat een goed overzicht geeft van de spreiding van vertragingen over deze twee jaar.
        - Totale vertraging in minuten (Y-as): Dit geeft het totale aantal minuten weer van alle vertragingen boven de 60 minuten op een bepaalde dag. Hoe hoger een punt op de Y-as staat, hoe meer vertragingen er die dag waren.
        - Kleurcodering per land: Elk land is weergegeven met een eigen kleur (bijvoorbeeld Vietnam in paars, Verenigde Staten in groen). Dit maakt het eenvoudig om de prestaties van verschillende landen te vergelijken en te zien welke dagen er uitschieters waren.
        """
    )
    st.subheader('Wat doen de sliders in deze visualisatie?')
    st.write('De visualisatie bevat twee interactieve sliders waarmee de gebruiker het datumbereik en het minimumaantal vertragingen kan aanpassen.')
    st.subheader('Selecteer het datumbereik:', divider = 'gray')
    st.write('Deze slider laat je het bereik van data aanpassen. Standaard is de periode ingesteld van 1 januari 2019 tot 31 december 2020, maar dit kan worden gewijzigd om kortere of langere perioden te bekijken. Dit helpt gebruikers bij het inzoomen op specifieke periodes waarin vertragingen mogelijk meer voorkwamen.')

    vertragingen_per_datum = uitschieters.groupby(['Land', 'Datum']).agg(
        Aantal_Vertragingen=('Vertraging', 'size'), 
        Totale_Vertraging=('Vertraging', 'sum')
    ).reset_index()

    vertragingen_per_datum = vertragingen_per_datum.sort_values(by=['Land', 'Aantal_Vertragingen'], ascending=False)

    start_date = datetime(2019, 1, 1)  
    end_date = datetime(2020, 12, 31) 

    selected_dates = st.slider(
        'Selecteer het datumbereik',
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),  
        format="YYYY-MM-DD"
    )

    st.subheader('Selecteer minimum aantal vertragingen:', divider='gray')
    st.write('Met deze slider kun je het minimumaantal vertragingen per dag filteren. Als je deze bijvoorbeeld instelt op een hogere waarde (bijv. 10 of 20), laat de grafiek alleen dagen zien waarop er veel vertragingen waren. Dit kan nuttig zijn om dagen met slechts enkele vertragingen te negeren en de focus te leggen op significante verstoringen. Deze interactieve elementen maken het mogelijk om de data vanuit verschillende perspectieven te verkennen, afhankelijk van de specifieke interesse van de gebruiker, zoals een bepaalde tijdsperiode of de ernst van de vertragingen.')

    start, end = selected_dates

    filtered_data = vertragingen_per_datum[(vertragingen_per_datum['Datum'] >= start) & (vertragingen_per_datum['Datum'] <= end)]
    aantal_min = int(filtered_data['Aantal_Vertragingen'].min())
    aantal_max = int(filtered_data['Aantal_Vertragingen'].max())

    aantal_vertragingen = st.slider(
        'Selecteer minimum aantal vertragingen',
        min_value=aantal_min,
        max_value=aantal_max,
        value=(aantal_min, aantal_max)
    )
    filtered_data = filtered_data[
        (filtered_data['Aantal_Vertragingen'] >= aantal_vertragingen[0]) &
        (filtered_data['Aantal_Vertragingen'] <= aantal_vertragingen[1])
    ]

    fig = px.scatter(filtered_data, 
                    x='Datum', 
                    y='Totale_Vertraging',  
                    color='Land', 
                    size='Aantal_Vertragingen',
                    title='Totale Vertragingen per Land en Datum (Uitschieters > 60 minuten)',
                    labels={'Totale_Vertraging': 'Totale Vertraging in Minuten', 'Datum': 'Datum'},
                    hover_data=['Land', 'Aantal_Vertragingen'],
                    template='plotly_white')

    fig.update_layout(xaxis_title='Datum', 
                    yaxis_title='Totale Vertraging in Minuten',
                    xaxis_tickangle=-45)

    st.plotly_chart(fig)

# ======================================================================================================================================================================

elif blog_post == 'Voorspellingsmodel voor vertraging':
    st.header('Voorspellingsmodellen voor vertraging')
    import sys
    import pandas as pd
    import numpy as np
    import re
    import streamlit as st

    from sklearn.metrics import accuracy_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn import preprocessing
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import make_pipeline
    from sklearn.metrics import mean_squared_error
    from sklearn.tree import DecisionTreeRegressor

    # Data inladen
    airports_extended_clean = pd.read_csv('airports-extended-clean.csv', sep=";")
    schedule_airports = pd.read_csv('schedule_airport.csv')

    # Data samenvoegen
    df_merged = schedule_airports.merge(airports_extended_clean, left_on='Org/Des', right_on='ICAO', how='inner')
    df_merged = df_merged.replace('-', np.nan)

    # Onnodige kolommen verwijderen
    columns_to_delete = ['DL1', 'IX1', 'DL2', 'IX2', 'Source', 'DST', 'RWC']
    df_merged.drop(columns=columns_to_delete, inplace=True)

    # Omzetten naar datetime
    df_merged['STD'] = df_merged['STD'].str.replace('/', '-')
    df_merged['STD'] = pd.to_datetime(df_merged['STD'], format='%d-%m-%Y')

    # Kolomnamen hernoemen
    df_merged.rename(columns={
        'STD': 'Datum',
        'FLT': 'Vlucht nummer',
        'STA_STD_ltc': 'Geplande aankomst',
        'ATA_ATD_ltc': 'Werkelijke aankomst',
        'LSV': 'Inkomend of uitgaand',
        'TAR': 'Geplande gate',
        'GAT': 'Werkelijke gate',
        'ACT': 'Vliegtuig type',
        'Org/Des': 'Bestemming/afkomst',
        'Name': 'Luchthaven',
        'City': 'Stad',
        'Country': 'Land',
        'Timezone': 'Timezone uren',
        'Tz': 'Timezone continent/stad',
        'Type': 'Type transport'
    }, inplace=True)

    # Geplande en werkelijke aankomst omzetten
    df_merged['Geplande aankomst'] = pd.to_datetime(df_merged['Geplande aankomst'], format='%H:%M:%S')
    df_merged['Werkelijke aankomst'] = pd.to_datetime(df_merged['Werkelijke aankomst'], format='%H:%M:%S')
    df_merged['Vertraging'] = (df_merged['Werkelijke aankomst'] - df_merged['Geplande aankomst']).dt.total_seconds() / 60
    df_merged['Vertraging (minuten)'] = np.where(df_merged['Vertraging'] > 0, df_merged['Vertraging'].abs(), 0)
    df_merged['Op tijd (minuten)'] = np.where(df_merged['Vertraging'] < 0, df_merged['Vertraging'].abs(), 0)

    # Omzetten naar tijdformaat
    df_merged['Geplande aankomst'] = df_merged['Geplande aankomst'].dt.time
    df_merged['Werkelijke aankomst'] = df_merged['Werkelijke aankomst'].dt.time

    # Categorieën maken voor vertraging
    df_merged["cat_Vertraging"] = np.where(df_merged["Vertraging"] > 60, 'zware vertraging',
                                            np.where(df_merged["Vertraging"] > 15, 'lichte vertraging', 'geen vertraging'))
    df_merged['Continent'] = df_merged['Timezone continent/stad'].str.split('/').str[0]

    df_merged.dropna(inplace=True)

    # Functie om Vliegmaatschappij-code te extraheren met regex
    def extract_vliegmaatschappij_code(flight_number):
        match = re.match(r'([A-Z0-9]{2})\d{2,4}', flight_number)
        return match.group(1) if match else None

    # Nieuwe kolom aanmaken met de Vliegmaatschappij-code
    df_merged['Vliegmaatschappij_code'] = df_merged['Vlucht nummer'].apply(extract_vliegmaatschappij_code)

    # Voorbereiden van de voorspellingsdataset
    vertraging_filtered = df_merged[df_merged["Vertraging"] <= 60]
    voorspel_dataset = vertraging_filtered[["Vliegmaatschappij_code", "Vliegtuig type", "IATA", "Vertraging", "cat_Vertraging"]]

    voorspel_dataset_y = voorspel_dataset["Vertraging"]
    voorspel_dataset_X = voorspel_dataset.drop("Vertraging", axis=1)

    # Functie om modellen te trainen en voorspellingen te doen
    def train_and_predict(model_name):
        if model_name == "Logistic Regression":
            voorspel_dataset = df_merged[["Vliegmaatschappij_code", "Land", "Vliegtuig type", "IATA", "cat_Vertraging"]]

            le = preprocessing.LabelEncoder()

            cols = ["Vliegmaatschappij_code", "Land", "Vliegtuig type", "IATA"]

            for col in cols:
                voorspel_dataset[col] = le.fit_transform(voorspel_dataset[col])

            voorspel_dataset_y = voorspel_dataset["cat_Vertraging"]
            voorspel_dataset_X = voorspel_dataset.drop("cat_Vertraging", axis=1)

            X_train, X_test, y_train, y_test = train_test_split(voorspel_dataset_X, voorspel_dataset_y, test_size=0.2, random_state=1234)

            model = LogisticRegression(random_state = 0, max_iter = 1000).fit(X_train, y_train)
            predictions = model.predict(X_test)

            accuracy = accuracy_score(y_test, predictions)
            return accuracy

        elif model_name == "Decision Tree":
            # Dataset selectie
            vertraging_filtered = df_merged[df_merged["Vertraging"] <= 60]
            voorspel_dataset = vertraging_filtered[["Vliegmaatschappij_code", "Vliegtuig type", "IATA", "Vertraging"]]

            # Kolommen met categorische data
            categorical_columns = ["Vliegmaatschappij_code", "Vliegtuig type", "IATA"]

            # OneHotEncoder met handle_unknown='ignore' voor onbekende categorieën
            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)], remainder='passthrough')

            # Features (X) en target (y) splitsen
            voorspel_dataset_y = voorspel_dataset["Vertraging"]
            voorspel_dataset_X = voorspel_dataset.drop("Vertraging", axis=1)

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(voorspel_dataset_X, voorspel_dataset_y, test_size=0.2, random_state=1234)

            # Pas de preprocessor toe op de train- en testdata
            X_train_encoded = preprocessor.fit_transform(X_train)
            X_test_encoded = preprocessor.transform(X_test)

            # Model trainen
            model = DecisionTreeRegressor(random_state=1234).fit(X_train_encoded, y_train)
            predictions = model.predict(X_test_encoded)

            mse = mean_squared_error(y_test, predictions)
            return mse

        elif model_name == "Random Forest":
            # Dataset selectie
            vertraging_filtered = df_merged[df_merged["Vertraging"] <= 60]
            voorspel_dataset = vertraging_filtered[["Vliegmaatschappij_code", "Vliegtuig type", "IATA", "Vertraging"]]

            # Kolommen met categorische data
            categorical_columns = ["Vliegmaatschappij_code", "Vliegtuig type", "IATA"]

            # OneHotEncoder met handle_unknown='ignore' voor onbekende categorieën
            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)], remainder='passthrough')

            # Features (X) en target (y) splitsen
            voorspel_dataset_y = voorspel_dataset["Vertraging"]
            voorspel_dataset_X = voorspel_dataset.drop("Vertraging", axis=1)

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(voorspel_dataset_X, voorspel_dataset_y, test_size=0.2, random_state=1234)

            # Maak de pipeline aan met preprocessor en RandomForestRegressor en train het model
            model = make_pipeline(preprocessor, RandomForestRegressor(random_state=1234, n_estimators=100)).fit(X_train, y_train)
        
            # Voorspellingen maken
            predictions = model.predict(X_test)

            mse = mean_squared_error(y_test, predictions)

            return mse
        return "Geen Model"

    # Streamlit UI

    st.write("""
            Een goed voorspellingsmodel is moeilijk te genereren omdat er rekening gehouden moet worden met de voorwaardes van het
            het gekozen voorspellingsmodel maar ook dat er genoeg en correcte data beschikbaar is. In dit geval waren er categorische 
            feature variabelen (de variabelen waarop je het model baseert):
            - vliegtuigmaatschappij
            - vliegtuig type
            - IATA code van het land 
            En een numeriek target variabel, de vertraging. 
            
            Om dit probleem op te lossen zijn er een paar mogelijkheden zo kan je de numerieke variabelen categorische maken door ze te 
            verdelen in bepaalde groepen maar de categorische variabelen kunnen ook numeriek worden gemaakt doormiddel van one-hot of 
            label encoding. En na deze aanpassingen kan er een model gekozen worden. Hieronder zijn er 3 uitgewerkt:

            Voor logistieke regressie is de vertraging opgedeeld in 3 categoriën.
            - geen vertraging: tot 10 minuten vertraging
            - lichte vertraging: Tot 60 minuten vertraging
            - zware vertraging: Meer dan 60 minuten vertraging
            Dit is gedaan omdat logistieke regressie alleen werkt wanneer de feature variabelen en de target veriabel categorisch zijn.

            Zo hebben we voor de decision tree en voor het random forest model gebruik gemaakt van one-hot encoding om van de categorische
            variabelen numeriek/binair te krijgen. Hierdoor kunnen deze twee modellen gemaakt en uitgevoerd worden. Omdat het met
            een decision tree en het random forest model over numerieke variabelen gaat kan er geen accuracy score worden berekend. Om
            hier een goed beeld te krijgen van hoe goed het model is wordt de MSE (mean squared error) uitgerekend. Dit is het verschil
            tussen de voorspelde waarde en de echte waarde gekwadrateerd en hiervan het gemiddelde genomen. Om dus een duidelijk beeld te
            krijgen wat de gemiddelde afwijking zal zijn voor elk punt zal de wortel van de MSE gevonden moeten worden.
            """)

    # Dropdown menu voor model selectie
    model_name = st.selectbox("Kies een model:", ["Logistic Regression", "Decision Tree", "Random Forest"])

    # Uitleg over de modellen
    if model_name == "Logistic Regression":
        st.write("""
        **Logistic Regression** is een statistisch model dat wordt gebruikt voor classificatieproblemen.
        Het model voorspelt de waarschijnlijkheid dat een gegeven invoer behoort tot een bepaalde klasse. 
        Het vereist dat de afhankelijke variabele binair is (bijvoorbeeld: op tijd of vertraging).
        
        **Voorwaarden voor gebruik:**
        - De data moet geschikt zijn voor classificatie.
        - Er moeten voldoende observaties per klasse zijn.
        - Categorieën in de input variabelen moeten goed zijn vertegenwoordigd.
        """)

    elif model_name == "Decision Tree":
        st.write("""
        **Decision Tree** is een voorspellingsmodel dat gebruik maakt van een boomstructuur om beslissingen te maken.
        Het verdeelt de data in subsets op basis van de waarde van de invoervariabelen, wat resulteert in een 
        helder en interpreteerbaar model.
        
        **Voorwaarden voor gebruik:**
        - Het model kan zowel categorische als numerieke data verwerken.
        - De data moet niet te veel ruis bevatten.
        - Het is gevoelig voor overfitting, dus goede training- en testverdelingen zijn belangrijk.
        """)

    elif model_name == "Random Forest":
        st.write("""
        **Random Forest** is een ensemble-leermethode die meerdere decision trees combineert om de nauwkeurigheid te verbeteren 
        en overfitting te verminderen. Het model creëert verschillende bomen met een random subset van de data en 
        combineert hun voorspellingen.
        
        **Voorwaarden voor gebruik:**
        - Het kan goed omgaan met grote datasets met veel features.
        - Er moeten voldoende data beschikbaar zijn om een sterke set van decision trees te creëren.
        - Het vereist meer rekenkracht en tijd dan individuele decision trees.
        """)

    # Voorspellingen maken
    predictions = train_and_predict(model_name)

    if model_name == "Logistic Regression":
        st.write(f"De accuracy voor {model_name}: {predictions:.2f}")
    else: 
        st.write(f"De MSE voor {model_name}: {predictions:.2f}")

# ======================================================================================================================================================================

elif blog_post == 'Vertraging in de wereld':
    st.header('Vertraging in de wereld')
    st.subheader('Vertraging in Europa')
    st.write('Met behulp van deze Python-code kun je eenvoudig een interactieve kaart genereren die de gemiddelde vertragingen op luchthavens over de hele wereld visualiseert. Hieronder bespreek ik hoe de code werkt en wat je als gebruiker ermee kunt doen.Wat kun jij ermee doen?')
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px
    from streamlit.components.v1 import html
    airports_extended_clean = pd.read_csv('airports-extended-clean.csv', sep =";")
    schedule_airports = pd.read_csv('schedule_airport.csv')

    df_merged = schedule_airports.merge(airports_extended_clean, left_on='Org/Des', right_on='ICAO', how='inner')
    df_merged= df_merged.replace('-', np.nan)

    del df_merged['DL1']
    del df_merged['IX1']
    del df_merged['DL2']
    del df_merged['IX2']
    del df_merged['Source']
    del df_merged['DST']
    del df_merged['RWC']

    df_merged['STD'] = df_merged['STD'].str.replace('/', '-')
    df_merged['STD'] = pd.to_datetime(df_merged['STD'], format='%d-%m-%Y')

    df_merged = df_merged.rename(columns={
        'STD':'Datum', 
        'FLT':'Vlucht nummer',
        'STA_STD_ltc':'Geplande aankomst',
        'ATA_ATD_ltc':'Werkelijke aankomst',
        'LSV':'Inkomend of uitgaand',
        'TAR':'Geplande gate',
        'GAT':'Werkelijke gate',
        'ACT':'Vliegtuig type',
        'Org/Des':'Bestemming/afkomst',
        'Name':'Luchthaven',
        'City':'Stad',
        'Country':'Land',
        'Timezone':'Timezone uren',
        'Tz':'Timezone continent/stad',
        'Type':'Type transport'
    })

    df_merged['Geplande aankomst'] = pd.to_datetime(df_merged['Geplande aankomst'], format='%H:%M:%S')
    df_merged['Werkelijke aankomst'] = pd.to_datetime(df_merged['Werkelijke aankomst'], format='%H:%M:%S')
    df_merged['Vertraging'] = df_merged['Werkelijke aankomst'] - df_merged['Geplande aankomst']
    df_merged['Geplande aankomst'] = df_merged['Geplande aankomst'].dt.time
    df_merged['Werkelijke aankomst'] = df_merged['Werkelijke aankomst'].dt.time
    df_merged = df_merged.dropna()

    # code voor europa

    import folium
    import pandas as pd

    # Haal continent uit 'Timezone continent/stad'
    df_merged['Continent'] = df_merged['Timezone continent/stad'].str.split('/').str[0]

    # Vervang komma's door punten en converteer naar numerieke waarden voor Latitude en Longitude
    df_merged['Latitude'] = pd.to_numeric(df_merged['Latitude'].replace(',', '.', regex=True), errors='coerce')
    df_merged['Longitude'] = pd.to_numeric(df_merged['Longitude'].replace(',', '.', regex=True), errors='coerce')

    # Zorg ervoor dat 'Vertraging' een timedelta is en converteer naar numeriek (bijv. minuten)
    # Aangenomen dat 'Vertraging' het verschil is tussen 'Werkelijke Tijd' en 'Geplande Tijd'
    # Als 'Vertraging' al in een timedelta-formaat is, converteer het naar minuten:
    df_merged['Vertraging'] = df_merged['Vertraging'].dt.total_seconds() / 60  # Converteert naar minuten

    # Verwijder rijen waar ofwel Latitude, Longitude of Vertraging NaN is
    df_merged_cleaned = df_merged.dropna(subset=['Latitude', 'Longitude', 'Vertraging'], how='any')

    # Verwijder dubbele rijen op basis van Latitude en Longitude om unieke punten te krijgen
    df_merged_cleaned = df_merged_cleaned.drop_duplicates(subset=['Latitude', 'Longitude'])
    df_avg_delay = df_merged_cleaned.groupby(['Latitude', 'Longitude']).agg({'Vertraging': 'mean'}).reset_index()

    # Functie om kleur toe te wijzen op basis van vertraging (Vertraging) in minuten
    def get_marker_color(vertraging):
        if vertraging < 0:
            return 'blue'
        if vertraging < 10:
            return 'green'  # Lage vertraging
        elif 10 <= vertraging < 60:
            return 'orange'  # Gemiddelde vertraging
        else:
            return 'red'  # Hoge vertraging

    # Maak de kaart gecentreerd op Schiphol luchthaven
    m = folium.Map(location=(52.308056, 4.764167), zoom_start=5)

    # Voeg Schiphol marker toe (met een tijdelijke kleur, je kunt dit verwijderen als het onnodig is)
    folium.Marker([52.308056, 4.764167], popup='<i>Schiphol airport</i>', icon=folium.Icon(color='blue')).add_to(m)

    # Loop door de gefilterde DataFrame om markers toe te voegen op basis van de gemiddelde vertraging
    for lat, lon, vertraging in df_merged_cleaned.query("Continent == 'Europe'")[['Latitude', 'Longitude', 'Vertraging']].values:
        color = get_marker_color(vertraging)  # Krijg markerkleur op basis van vertraging
        folium.Marker([lat, lon], icon=folium.Icon(color=color), popup=f'Gemiddelde Vertraging: {vertraging:.2f} minuten').add_to(m)
    legend_html = '''
        <div style="
        position: fixed;
        bottom: 50px; left: 50px; width: 150px; height: 220px; 
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        ">
        <strong>Vertraging Legenda</strong><br>
        <i class="fa fa-circle" style="color:blue"></i> tevroeg  (<0 min)<br>
        <i class="fa fa-circle" style="color:green"></i> Lage vertraging (<10 min)<br>
        <i class="fa fa-circle" style="color:orange"></i> Gemiddelde vertraging (10-30 min)<br>
        <i class="fa fa-circle" style="color:red"></i> Hoge vertraging (>60 min)<br>
        </div>
        '''

    # Add the HTML for the legend to the map.
    m.get_root().html.add_child(folium.Element(legend_html))

    # Opslaan as HTML string
    mHTML = m._repr_html_()

    # Toon de kaart
    st.components.v1.html(mHTML, height = 500)

    st.subheader('Vertraging wereldwijd')
    st.write("Deze kaart is handig als je een overzicht wilt krijgen van vertragingen per luchthaven wereldwijd. Verken specifieke regio's: Door te wisselen tussen continenten kun je eenvoudig inzoomen op vertragingen in een specifieke regio. Analyseer vertragingen per luchthaven: Elke marker geeft de gemiddelde vertraging voor een luchthaven weer, waardoor je snel inzicht krijgt in luchthavens met veel vertraging.")

    #code voor de wereld met selectie menu
    import folium
    import pandas as pd

    # Haal continent uit 'Timezone continent/stad'
    df_merged['Continent'] = df_merged['Timezone continent/stad'].str.split('/').str[0]

    # Vervang komma's door punten en converteer naar numerieke waarden voor Latitude en Longitude
    df_merged['Latitude'] = pd.to_numeric(df_merged['Latitude'].replace(',', '.', regex=True), errors='coerce')
    df_merged['Longitude'] = pd.to_numeric(df_merged['Longitude'].replace(',', '.', regex=True), errors='coerce')

    # Zorg ervoor dat 'Vertraging' een timedelta is en converteer naar numeriek (bijv. minuten)
    # Aangenomen dat 'Vertraging' het verschil is tussen 'Werkelijke Tijd' en 'Geplande Tijd'
    # Als 'Vertraging' al in een timedelta-formaat is, converteer het naar minuten:
    # df_merged['Vertraging'] = df_merged['Vertraging'].dt.total_seconds() / 60  # Converteert naar minuten, deze wellicht uicommenten wanneer error Deltatimeint/datetimelike values

    # Verwijder rijen waar ofwel Latitude, Longitude of Vertraging NaN is
    df_merged_cleaned = df_merged.dropna(subset=['Latitude', 'Longitude', 'Vertraging'], how='any')

    # Verwijder dubbele rijen op basis van Latitude en Longitude om unieke punten te krijgen
    df_merged_cleaned = df_merged_cleaned.drop_duplicates(subset=['Latitude', 'Longitude'])

    # Bereken de gemiddelde vertraging per luchthaven op basis van unieke Latitude en Longitude voor elk continent
    df_avg_delay = df_merged_cleaned.groupby(['Continent', 'Latitude', 'Longitude', 'Bestemming/afkomst']).agg({'Vertraging': 'mean'}).reset_index()

    # Functie om kleur toe te wijzen op basis van vertraging (Vertraging) in minuten
    def get_marker_color(vertraging):
        if vertraging < 0:
            return 'blue'
        if vertraging < 10:
            return 'green'  # Lage vertraging
        elif 10 <= vertraging < 60:
            return 'orange'  # Gemiddelde vertraging
        else:
            return 'red'  # Hoge vertraging

    # Maak de hoofdkaart gecentreerd op Europa
    m = folium.Map(location=(52.308056, 4.764167), zoom_start=3)

    # Unieke continenten uit de DataFrame ophalen
    continents = df_avg_delay['Continent'].unique()

    # Voor elk continent een eigen FeatureGroup toevoegen
    for continent in continents:
        # Maak een nieuwe FeatureGroup voor het continent
        continent_layer = folium.FeatureGroup(name=continent)

        # Filter het gemiddelde vertraging per continent
        df_continent = df_avg_delay[df_avg_delay['Continent'] == continent]

        # Voeg markers toe voor het huidige continent
        for lat, lon, vertraging, bestemming in df_continent[['Latitude', 'Longitude', 'Vertraging', 'Bestemming/afkomst']].values:
            color = get_marker_color(vertraging)  # Krijg markerkleur op basis van vertraging
            popup_message = f'Gemiddelde Vertraging: {vertraging:.2f} minuten<br>Bestemming: {bestemming}'
            folium.Marker([lat, lon], icon=folium.Icon(color=color),
                        popup=popup_message).add_to(continent_layer)

        # Voeg de laag van het continent toe aan de kaart
        continent_layer.add_to(m)

    # Voeg LayerControl toe zodat gebruikers tussen continenten kunnen wisselen
    folium.LayerControl(collapsed=False).add_to(m)

    # HTML-sjabloon voor de legenda
    legend_html = '''
        <div style="
        position: fixed;
        top: 10px; left: 50px; width: 150px; height: 235px; 
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        ">
        <strong>Vertraging Legende</strong><br>
        <i class="fa fa-circle" style="color:blue"></i> Te vroeg (<0 min)<br>
        <i class="fa fa-circle" style="color:green"></i> Lage vertraging (<10 min)<br>
        <i class="fa fa-circle" style="color:orange"></i> Gemiddelde vertraging (10-30 min)<br>
        <i class="fa fa-circle" style="color:red"></i> Hoge vertraging (>60 min)<br>
        </div>
        '''

    # Voeg de legenda toe aan de kaart
    m.get_root().html.add_child(folium.Element(legend_html))

    # Opslaan als HTML
    mHTML = m._repr_html_()

    # Toon de kaart
    st.components.v1.html(mHTML, height = 2000)
