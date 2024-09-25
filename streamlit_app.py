import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
st.title('🎈 App Name')

st.write('Hello world!')


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

covid_df_EU_con_diff = covid_df_EU[['province', 'country_name', 'confirmed', 'confirmed_diff']].copy()
covid_df_EU_con_diff['2023-03-08'] = covid_df_EU_con_diff['confirmed'] - covid_df_EU_con_diff['confirmed_diff']
covid_df_EU_con_diff['confirmed_increase_%'] = (((covid_df_EU_con_diff['confirmed'] - covid_df_EU_con_diff['2023-03-08']) / covid_df_EU_con_diff['2023-03-08']) * 100)
covid_df_EU_con_diff.rename(columns={'confirmed':'2023-03-09'}, inplace=True)
covid_df_EU_con_diff = covid_df_EU_con_diff.reindex(columns=['country_name', 'province', 'confirmed_diff','confirmed_increase_%', '2023-03-08', '2023-03-09',])

countries = covid_df_EU_con_diff['country_name'].unique()
selected_country = st.selectbox('Selecteer een land: ', countries)

filtered_country_df = covid_df_EU_con_diff[covid_df_EU_con_diff['country_name'] == selected_country]

provinces = covid_df_EU_con_diff['province'].unique()
selected_province = st.select_slider('Selecteer een provincie: ', options=provinces)

filtered_province_df = filtered_country_df[filtered_country_df['province'] == selected_province]

dates = ['2023-03-08', '2023-03-09']
cases = filtered_province_df[['2023-03-08', '2023-03-09']].values.flatten()

fig_bar = go.Figure()

fig_bar.add_trace(go.Bar(
    x=[dates[0]], 
    y=[cases[0]],
    name='Gediagnosticeerde Gevallen 2023-03-08',
    marker_color='blue'
))

fig_bar.add_trace(go.Bar(
    x=[dates[1]], 
    y=[cases[1]],
    name='Gediagnosticeerde Gevallen 2023-03-09',
    marker_color='orange'
))

fig_bar.update_layout(
    title=f'COVID-19 Gevallen in {selected_province}, {selected_country}',
    xaxis_title='Datum',
    yaxis_title='Gediagnosticeerde Gevallen',
    barmode='group',  
    template='plotly_white'  
)

st.plotly_chart(fig_bar)

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

st.title('COVID-19 Increase Percentage Dashboard')

selected_country_checkbox = st.selectbox('Selecteer een land', covid_df_EU_increase_pct['country_name'].unique())

filtered_df = covid_df_EU_increase_pct[covid_df_EU_increase_pct['country_name'] == selected_country_checkbox]

selected_province_checkbox = st.selectbox('Selecteer een provincie', filtered_df['province'].unique())

province_data_checkbox = filtered_df[filtered_df['province'] == selected_province_checkbox]

if not province_data_checkbox.empty:
    metrics = ['active_increase_%', 'confirmed_increase_%', 'deaths_increase_%']
    values = province_data_checkbox[metrics].values[0]

    fig_check, ax = plt.subplots()
    ax.bar(metrics, values, color=['blue', 'orange', 'red'])
    ax.set_title(f'Toename in Percentage voor {selected_province_checkbox}')
    ax.set_ylabel('Percentage')

    st.pyplot(fig_check)
