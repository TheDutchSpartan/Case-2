import streamlit as st 
import requests 
import pandas as pd 
import matplotlib 
import matplotlib.pyplot as plt 
import plotly 
import plotly.graph_objects as go 
import plotly.express as px
import numpy 
import numpy as np


url = "https://covid-19-statistics.p.rapidapi.com/reports"

headers = {
    'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
    'x-rapidapi-key': "89dc140db7mshf142d6f86d6ce14p1c3e02jsn2c6a8f31519e"
}

country_code_EU = ['BEL', 'DNK', 'BGR', 'CYP', 'DEU', 'EST', 'FIN', 'FRA', 'GRC', 'HUN', 'IRL', 'ITA', 'HRV', 'LVA', 'LTU', 
                   'LUX', 'MLT', 'NLD', 'AUT', 'POL', 'PRT', 'ROU', 'SVN', 'SVK', 'ESP', 'CZE', 'SWE']
querystring_EU = {'iso': country_code_EU}

headers = {
    'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
    'x-rapidapi-key': "89dc140db7mshf142d6f86d6ce14p1c3e02jsn2c6a8f31519e"
}

country_names = {
    'BEL': 'België','DNK': 'Denemarken','BGR': 'Bulgarije','CYP': 'Cyprus','DEU': 'Duitsland','EST': 'Estland','FIN': 'Finland',
    'FRA': 'Frankrijk','GRC': 'Griekenland','HUN': 'Hongarije','IRL': 'Ierland','ITA': 'Italië','HRV': 'Kroatië','LVA': 'Letland',
    'LTU': 'Litouwen','LUX': 'Luxemburg','MLT': 'Malta','NLD': 'Nederland','AUT': 'Oostenrijk','POL': 'Polen','PRT': 'Portugal',
    'ROU': 'Roemenië','SVN': 'Slovenië','SVK': 'Slovakije','ESP': 'Spanje','CZE': 'Tsjechië','SWE': 'Zweden'
}

# ======================================================================================================================================== #
st.title("""*COVID-19 Data* van 08 en 09 Maart 2023 voor EU-Landen""")

st.write("""Tijdens de pandemie is het bijhouden van data cruciaal geweest om inzicht te krijgen in de verspreiding en impact van COVID-19 in verschillende regio’s. In dit project hebben we een interactieve data-visualisatie ontwikkeld met behulp van Python en de Streamlit-bibliotheek. Ons doel was om gebruikers de mogelijkheid te geven om de COVID-19-gevallen en sterfgevallen in verschillende Europese landen en hun provincies te verkennen.""")
st.write("""Hiervoor hebben we als eerst een grafiek gecreëerd die het aantal gediagnosticeerde gevallen en sterfgevallen per land en provincie toont. Gebruikers kunnen zelf kiezen welke data ze willen bekijken, zowel de gediagnosticeerde gevallen als de sterfgevallen, of slechts één van beide datasets. Op deze manier kunnen gebruikers eenvoudig de verspreiding van COVID-19 binnen specifieke regio's analyseren.""")

# ======================================================================================================================================== #

EU_data = []
for country_code in country_code_EU:
    querystring_EU = {'iso':country_code}
    response_EU = requests.get(url, headers=headers, params=querystring_EU)
    data_EU = response_EU.json()

    if 'data' in data_EU:
        for report in data_EU['data']:
            report['country'] = country_code
            report['country_name'] = country_names[country_code]
            EU_data.append(report)


covid_df_EU = pd.DataFrame(EU_data)
covid_df_EU.set_index('country', inplace = True)

covid_df_EU['province'] = covid_df_EU['region'].apply(lambda x: x.get('province'))
covid_df_EU = covid_df_EU[covid_df_EU['province'] != 'Unknown']

province_data_EU = covid_df_EU.groupby(['province', 'country_name']).agg({'confirmed': 'sum', 'deaths': 'sum', 'fatality_rate': 'mean'}).reset_index()
province_data_EU = province_data_EU.reindex(columns=['country_name', 'province', 'confirmed', 'deaths', 'fatality_rate'])
province_data_EU = province_data_EU.sort_values(by='country_name', ascending=True)

fig = go.Figure()

for country in province_data_EU['country_name'].unique():
    province_data_EU_filtered = province_data_EU[province_data_EU['country_name'] == country]
    fig.add_trace(go.Bar(x=province_data_EU_filtered['province'],
                        y=province_data_EU_filtered['confirmed'],
                        name=f'{country} gediagnosticeerde',
                        visible=False,
                        marker_color='blue'))
    fig.add_trace(go.Bar(x=province_data_EU_filtered['province'],
                        y=province_data_EU_filtered['deaths'],
                        name=f'{country} sterfgevallen',
                        visible=False,
                        marker_color='red'))

fig.data[0].visible=True
fig.data[1].visible=True

dropdown_buttons = []

for country in province_data_EU['country_name'].unique():
    dropdown_buttons.append({
        'label':country,
        'method':'update',
        'args':[{'visible': [name.startswith(country) for name in [trace.name for trace in fig.data]]},
        {'title':f'COVID-19 Gegevens voor {country}'}]
    })

fig.update_layout(
    title = 'COVID-19 Gediagnosticeerde en Sterfgevallen per Provincie',
    xaxis_title = 'Provincie',
    yaxis_title = 'Aantal',
    barmode = 'group',
    updatemenus = [{'buttons':dropdown_buttons,
                    'showactive':True,
                    'direction':'down'}]
)

st.plotly_chart(fig)

# =================================================================================================================================== #

st.header("""Procentuele Toename van COVID-19 Gevallen en Sterfgevallen in de EU""")
st.write("""De verspreiding van COVID-19 blijft een belangrijke zorg in Europa, waarbij overheden en gezondheidsautoriteiten nauwlettend de dagelijkse stijgingen in besmettingen en sterfgevallen volgen. De onderstaande grafiek biedt een inzichtelijke vergelijking van de procentuele toename van actieve COVID-19-gevallen, bevestigde besmettingen, en sterfgevallen per provincie, tussen 8 en 9 maart 2023.""")
st.write("""Door deze gegevens te analyseren, krijgen we een duidelijker beeld van welke provincies in verschillende landen het hardst worden getroffen door de pandemie. Dit kan beleidsmakers helpen om beter geïnformeerde beslissingen te nemen over interventies en middelen.""")
st.write("""Kies hieronder een land en een provincie om de specifieke stijgingspercentages te bekijken. De kleuren in de grafiek geven de stijgingen weer: blauw voor actieve gevallen, oranje voor bevestigde besmettingen, en rood voor sterfgevallen.""")

# =================================================================================================================================== #

covid_df_EU_con_diff = covid_df_EU[['province', 'country_name', 'confirmed', 'confirmed_diff']].copy()
covid_df_EU_con_diff['2023-03-08'] = covid_df_EU_con_diff['confirmed'] - covid_df_EU_con_diff['confirmed_diff']
covid_df_EU_con_diff['confirmed_increase_%'] = (((covid_df_EU_con_diff['confirmed'] - covid_df_EU_con_diff['2023-03-08']) / covid_df_EU_con_diff['2023-03-08']) * 100)
covid_df_EU_con_diff.rename(columns={'confirmed':'2023-03-09'}, inplace=True)
covid_df_EU_con_diff = covid_df_EU_con_diff.reindex(columns=['country_name', 'province', 'confirmed_diff','confirmed_increase_%', '2023-03-08', '2023-03-09',])

covid_df_EU_dea_diff = covid_df_EU[['province', 'country_name', 'deaths', 'deaths_diff']].copy()
covid_df_EU_dea_diff['2023-03-08'] = covid_df_EU_dea_diff['deaths'] - covid_df_EU_dea_diff['deaths_diff']
covid_df_EU_dea_diff['deaths_increase_%'] = (((covid_df_EU_dea_diff['deaths'] - covid_df_EU_dea_diff['2023-03-08']) / covid_df_EU_dea_diff['2023-03-08']) * 100)
covid_df_EU_dea_diff.rename(columns={'deaths':'2023-03-09'}, inplace=True)
covid_df_EU_dea_diff = covid_df_EU_dea_diff.reindex(columns=['country_name', 'province', 'deaths_diff', 'deaths_increase_%', '2023-03-08', '2023-03-09'])
covid_df_EU_dea_diff['deaths_increase_%'] = covid_df_EU_dea_diff['deaths_increase_%'].fillna(0)

covid_df_EU_act_diff = covid_df_EU[['province', 'country_name', 'active', 'active_diff']].copy()
covid_df_EU_act_diff['2023-03-08'] = covid_df_EU_act_diff['active'] - covid_df_EU_act_diff['active_diff']
covid_df_EU_act_diff['active_increase_%'] = (((covid_df_EU_act_diff['active'] - covid_df_EU_act_diff['2023-03-08']) / covid_df_EU_act_diff['2023-03-08']) * 100)
covid_df_EU_act_diff.rename(columns={'active':'2023-03-09'}, inplace=True)
covid_df_EU_act_diff = covid_df_EU_act_diff.reindex(columns=['country_name', 'province', 'active_diff', 'active_increase_%', '2023-03-08', '2023-03-09'])
covid_df_EU_act_diff['active_increase_%'] = covid_df_EU_act_diff['active_increase_%'].fillna(0)

covid_df_EU_increase_pct = covid_df_EU_act_diff[['province', 'country_name', 'active_increase_%']].merge(
    covid_df_EU_con_diff[['province', 'country_name', 'confirmed_increase_%']],
    on=['province', 'country_name'],
    how='inner').merge(
        covid_df_EU_dea_diff[['province', 'country_name', 'deaths_increase_%']],
        on=['province', 'country_name'],
        how='inner'
    )
covid_df_EU_increase_pct = covid_df_EU_increase_pct.reindex(
    columns=['country_name', 'province', 'active_increase_%', 'confirmed_increase_%', 'deaths_increase_%'])

st.header('COVID-19 Toename Percentage Dashboard')

selected_country_checkbox = st.selectbox('Selecteer een land', covid_df_EU_increase_pct['country_name'].unique())

filtered_df = covid_df_EU_increase_pct[covid_df_EU_increase_pct['country_name'] == selected_country_checkbox]

selected_province_checkbox = st.selectbox('Selecteer een provincie', filtered_df['province'].unique())

province_data_checkbox = filtered_df[filtered_df['province'] == selected_province_checkbox]

if not province_data_checkbox.empty:
    # Dutch translations for the x-axis labels
    labels = ['Actieve Toename (%)', 'Gediagnosticeerde Toename (%)', 'Sterfgevallen Toename (%)']
    values = province_data_checkbox[['active_increase_%', 'confirmed_increase_%', 'deaths_increase_%']].values[0]

    fig_check = go.Figure()

    fig_check.add_trace(go.Bar(
        x=labels, 
        y=values,
        marker_color=['blue', 'orange', 'red']
    ))

    fig_check.update_layout(
        title=f'Toename in Percentage voor {selected_province_checkbox}',
        xaxis_title='Meting',
        yaxis_title='Percentage',
        template='plotly_white',
        showlegend=False
    )

    if selected_province_checkbox == "":
        display_name = selected_country_checkbox
    else:
        display_name = selected_province_checkbox

    if np.all(values == 0):
        st.write(f'Geen toename van covid-19 percentages bekend in {display_name} tussen de dagen 08-03-2023 en 09-03-2023')
    else:
        st.plotly_chart(fig_check)

# ================================================================================================================================== #

st.header("""Analyse van COVID-19: Gediagnosticeerde Gevallen versus Sterfgevallen""")
st.write("""Het verloop van de COVID-19-pandemie kan per regio sterk verschillen, afhankelijk van verschillende factoren zoals bevolkingsdichtheid, zorgcapaciteit en overheidsmaatregelen. Het begrijpen van deze regionale verschillen is essentieel voor zowel beleidsmakers als gezondheidsautoriteiten.""")
st.write("""De onderstaande grafiek biedt een visuele weergave van het aantal gediagnosticeerde gevallen in verhouding tot het aantal sterfgevallen in Europese provincies, op zowel 8 als 9 maart 2023. De data per dag zijn apart weergegeven, en met de slider kunt u eenvoudig schakelen tussen beide datums. Elke marker vertegenwoordigt een provincie, en de positie ervan toont hoe deze zich verhoudt tot de andere provincies.""")
st.write("""Door deze informatie te visualiseren, wordt het mogelijk om trends te ontdekken en provincies te identificeren waar sterfgevallen in verhouding tot gediagnosticeerde gevallen hoger zijn, of waar de stijging in besmettingen significant is. Dit type inzicht kan bijdragen aan meer gerichte interventies in de strijd tegen COVID-19.""")

# =================================================================================================================================== #

covid_df_EU_slider = covid_df_EU[['country_name', 'province']].merge(
    covid_df_EU_con_diff[['province', 'country_name', '2023-03-08', '2023-03-09']],
    on=['province', 'country_name'],
    how='inner').merge(
        covid_df_EU_dea_diff[['province', 'country_name', '2023-03-08', '2023-03-09']],
        on=['province', 'country_name'],
        how='inner',
        suffixes=('_con', '_dea')
    )

covid_df_EU_slider = covid_df_EU_slider[~((covid_df_EU_slider['country_name'] == 'Frankrijk') & (covid_df_EU_slider['province'] == ""))]

fig_scat = go.Figure()

fig_scat.add_trace(go.Scatter(
    x=covid_df_EU_slider['2023-03-08_con'],
    y=covid_df_EU_slider['2023-03-08_dea'],
    mode='markers',
    marker=dict(color=covid_df_EU_slider['country_name'].astype('category').cat.codes),  
    text=covid_df_EU_slider['country_name'],  
    name='2023-03-08'
))

fig_scat.add_trace(go.Scatter(
    x=covid_df_EU_slider['2023-03-09_con'],
    y=covid_df_EU_slider['2023-03-09_dea'],
    mode='markers',
    marker=dict(color=covid_df_EU_slider['country_name'].astype('category').cat.codes),
    text=covid_df_EU_slider['country_name'],
    name='2023-03-09',
    visible=False 
))

fig_scat.update_layout(
    title='Aantal gediagnosticeerde uitgezet tegen het aantal sterfgevallen',
    xaxis_title='Aantal gediagnosticeerde',
    yaxis_title='Aantal sterfgevallen',
    template='plotly_white',
    sliders=[{
        'steps': [
            {
                'method': 'update',
                'label': '2023-03-08',
                'args': [{'visible': [True, False]}, {'title': 'Data van 2023-03-08'}]
            },
            {
                'method': 'update',
                'label': '2023-03-09',
                'args': [{'visible': [False, True]}, {'title': 'Data van 2023-03-09'}]
            }
        ],
        'currentvalue': {'prefix': 'Datum: '},
        'pad': {'t': 50} 
    }]
)

st.plotly_chart(fig_scat)
