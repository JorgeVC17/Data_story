# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 11:20:37 2023

@author: jorge
"""
#Import packages
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
import os


#Open de dataset van "Malaria"
df = pd.read_csv("data/malaria_reported_numbers.csv")

#Open de dataset van "Klimaat Verandering"
df1 = pd.read_csv("data/climate_change_data.csv")

#Open de dataset van "Earth Surface Temperature:
df_k = pd.read_csv("data/annual_csv.csv")

#Malaria dataset nakijken en schoonmaken
print("=======================MALARIA DATA NAKIJKEN=====================")
print(df.nunique())
print(df.info())
print(df.isna().sum())
print(df.head())

#Fill de non-values met "0"
print("=======================MALARIA DATASET SCHOONGEMAAKT=====================")
df_new = df.fillna(0)
df_new.sort_values(by='Year', ascending=True, inplace=True)
print(df_new.head())
print(df_new.isna().sum())

#Klimaat verandering dataset nakijken
print("=======================KLIMAAT DATA NAKIJKEN=====================")
print(df1.nunique())
print(df1.info())

#Klimaat verandering dataset schoomaken
df1['Year'] = pd.to_datetime(df1['Date']).dt.year
df1['Date'] = df1['Year']
df1.drop('Year', axis=1, inplace=True)
df1.sort_values(by='Date', ascending=False)
df1.rename(columns={'Date': 'Year'}, inplace=True)
print("=======================KLIMAAT DATASET SCHOONGEMAAKT=====================")
print(df1.isna().sum())
print(df1.head())

#Earth Surface Temperature dataset nakijken
print("=======================Earth Surface Temperatuur DATA NAKIJKEN=====================")
print(df_k.nunique())
print(df_k.info())

#Earth Surface Temperature dataset schoomaken
print("=======================Earth Surface Temperatuur DATASET SCHOONGEMAAKT=====================")
print(df_k.isna().sum())
df_k.sort_values(by='Year', ascending=True, inplace=True)
print(df_k.head())

#Beginnen met de dashboard in Streamlit
#Hoofdpagina
st.title("Stijging van Malaria over de jaren")
st.header("Een data story over de invloed van klimaatverandering op ziektes")
st.write("Over de jaren zien we de gevolgen van klimaatverandering op onze maatschappij. Denk aan de stijging van de zeespiegel, extreem weer, verlies van biodiversiteit, enzovoort. Maar een van de gevolgen van klimaatverandering waar niet veel mensen zich van bewust zijn, is het effect van klimaatverandering op de verspreiding van bepaalde ziekten. In deze datastory zullen we dieper ingaan op de toename van de ziekte malaria als gevolg van klimaatverandering en wat zijn de gevolgen van de stijging van malaria. Klik op deze link [(World Health Organization: WHO, 2018)](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health) voor meer informatie.")

#Figure 1 en 2:
artikel1 = Image.open('afbeeldingen/artikel1.JPG')
st.image(artikel1, caption="Figuur 1: Artikel over de invloed van klimaatverandering op Malaria")
malaria_image = Image.open('afbeeldingen/malaria_parasiet.jpg')
st.image(malaria_image, caption="Figuur 2: Malaria parasiet onder de microscoop", output_format='auto')

#Creert filtratie opties voor de verschillende datasets
st.sidebar.info("Je kan de onderstaande opties gebruiken om de cijfers en grafieken van deze data story te kunnen filtreren")
st.sidebar.header("Malaria dataset filter (Hoofdstuken 1 en 2):")
WHO_Region = st.sidebar.multiselect(
    "Kies een WHO Region:",
    options = df_new['WHO Region'].unique(),
    default=df_new['WHO Region'].unique())

Jaar = st.sidebar.select_slider(
    label="Kies welk jaar wil je nakijken:", 
    options=df_new['Year'].unique(),
    value=df_new['Year'].min())

st.sidebar.markdown("""____""")

#Creert filtratie opties voor de Klimaat verandering dataset
st.sidebar.header("Klimaatverandering dataset filter (Hoofdstuuk 5):")

Jaar2 = st.sidebar.select_slider(
    label="Kies welk jaar wil je nakijken:", 
    options=df1['Year'].unique(),
    value=df1['Year'].min())

st.sidebar.markdown("""____""")

#Store data in df.selection
df_selection = df_new.query(
    "(`WHO Region` == @WHO_Region) & (Year == @Jaar)")

df_selection2 = df1.query(
    "(Year == @Jaar2)")

#Subset data
total_cases = int(df_selection["No. of cases"].sum())
total_deaths = int(df_selection["No. of deaths"].sum())
average_deaths = int(df_selection["No. of deaths"].mean())

#Malaria dataset analyse lay-out:
st.header("1. Wat is Malaria?")
st.write("Malaria is een ziekte die wordt veroorzaakt door kleine parasieten. Mensen kunnen besmet raken als ze worden gebeten door bepaalde muggen die deze parasieten bij zich dragen. Malaria verspreidt zich meestal naar mensen via de beten van geïnfecteerde vrouwelijke 'Anopheles-muggen'. Bloedtransfusie en besmette naalden kunnen ook malaria overdragen. De eerste symptomen kunnen mild zijn en lijken op veel koortsende ziekten, en zijn moeilijk te herkennen als malaria.[(World Health Organization: WHO & World Health Organization: WHO, 2023)](https://www.who.int/news-room/fact-sheets/detail/malaria)")
st.info("VERGEET NIET OM DE FILTER OPTIES TE GEBRUIKEN.")
st.header("1.1 Malaria cijfers")

#Maak columns
left, middle, right = st.columns(3)
with left:
    st.subheader("Aantal malariagevallen")
    st.subheader(f"{total_cases}")
with middle:
    st.subheader("Aantal Malaria sterfgevallen")
    st.subheader(f"{total_deaths}")
with right:
    st.subheader("Gemiddelde Malaria sterfgevallen per jaar")
    st.subheader(f"{average_deaths}")
    
st.info("VERGEET NIET OM DE FILTER OPTIES TE GEBRUIKEN.")
st.markdown("""____""")

#Malaria dataset analyse lay-out:
st.subheader("In 2000 werden ongeveer 8 miljoenen malariagevallen vermeld.")
st.subheader("In 2017 werden ongeveer 1.2 miljard malariagevallen vermeld!")
st.subheader("Met 1,2 miljard mensen zou je ongeveer 21.828 Johan Cruijff ArenA-stadions kunnen vullen")
stadion = Image.open('afbeeldingen/stadion.jpg')
st.image(stadion, caption="Johan Cruijff ArenA-stadion")
st.subheader("Dit grote aantal malariagevallen kan verschillende effecten op onze maatschappij hebben, zoals:")
st.write("1. Gezondheidszorgsystemen overbelast: Als veel mensen tegelijk ziek worden, kan de capaciteit van gezondheidszorgsystemen heel hoog worden. Dit kan leiden tot een gebrek aan beschikbare ziekenhuisbedden, medische apparatuur en zorgverleners, waardoor de kwaliteit van de zorg en het leven van veel mensen in gevaar komt.")
st.write("2. Snelle verspreiding van ziekte: Een groter aantal zieke mensen vergroot de kans op een snellere verspreiding van de ziekte. Dit kan leiden tot een groter aantal besmettingen en een grote mogelijkheid van deze ziekte niet onder controle te krijgen. Dit kan eventueel leiden tot een pandemie.")

#Figuur 3
malaria_cases = df_selection.groupby(by=['WHO Region'])[["No. of cases"]].mean().sort_values(by="No. of cases").reset_index()

fig_malaria_cases = px.bar(data_frame=malaria_cases, 
                           x='WHO Region',
                           y='No. of cases',
                           color='WHO Region',
                           title="Figuur 3: Gemiddelde malariagevallen per WHO region")

# Update de axis van figuur 3
fig_malaria_cases.update_xaxes(title_text='WHO Region')
fig_malaria_cases.update_yaxes(title_text='Gemiddelde malariagevallen')

#Figuur 4
malaria_cases12 = df_selection.groupby(by=['WHO Region'])[["No. of deaths"]].mean().sort_values(by="No. of deaths").reset_index()

fig_malaria_cases12 = px.bar(data_frame=malaria_cases12, 
                           x='WHO Region',
                           y='No. of deaths',
                           color='WHO Region',
                           title="Figuur 4: Gemiddelde Malaria sterfgevallen per WHO region")

# Update de axis van figuur 4
fig_malaria_cases12.update_xaxes(title_text='WHO Region')
fig_malaria_cases12.update_yaxes(title_text='Gemiddelde Malaria sterfgevallen')

#Figuur 5
malaria_cases2 = df_new.groupby(['Year', 'WHO Region'])['No. of cases'].mean().reset_index()

fig_malaria_cases2 = px.line(data_frame=malaria_cases2,
                            x='Year',
                            y='No. of cases',
                            title="Figuur 5: Gemiddelde malariagevallen over de tijd per WHO Region",
                            color='WHO Region')

# Update de axis van figuur 5
fig_malaria_cases2.update_xaxes(title_text='Jaar')
fig_malaria_cases2.update_yaxes(title_text='Gemiddelde malariagevallen')

#Figuur 6
malaria_cases3 = df_new.groupby(['Year', 'WHO Region'])['No. of cases'].sum().reset_index()

fig_malaria_cases3 = px.scatter(data_frame = malaria_cases3,
                                  x='Year',
                                  y='No. of cases',
                                  color='WHO Region',
                                  symbol='WHO Region',
                                  trendline='ols',
                                  trendline_scope='overall',
                                  title='Figuur 6: Correlatie tussen het aantal malariagevallen en de tijd')

#Update axis van figuur 6
fig_malaria_cases3.update_xaxes(title_text='Jaar')
fig_malaria_cases3.update_yaxes(title_text='Malariagevallen(Log Scale)')
fig_malaria_cases3.update_layout(yaxis_type='log')

#Layout voor de grafieken van de malaria dataset analyse:
st.header("2. Gemiddelde malariagevallen vs Gemiddelde Malaria sterfgevallen over verschillende jaren")
st.write("Om een overzicht van de impact van malaria te krijgen, is het heel handig om het gemiddelde aantal malariagevallen en sterfgevallen per jaar na te kijken.")
st.plotly_chart(fig_malaria_cases)
st.info("VERGEET NIET OM DE FILTER OPTIES TE GEBRUIKEN.")
st.plotly_chart(fig_malaria_cases12)
st.subheader("Hoe verder in de loop der tijd gaan, hoe hoger het aantal malariagevallen worden.")
st.header("2.1 Gemiddelde gevallen over de tijd")
st.plotly_chart(fig_malaria_cases2)
st.write("Op de bovenstaande grafiek wordt er makkelijker gezien de stijging van gemiddelde malariagevallen in verschillende regio's over de jaren.")
st.write(" Het is heel belangrijk om de stijging in de Africa regio op te merken. Dit gaat van 31000 gemiddelde malariagevallen op 2000 tot 2,6 miljoenen gemiddelde malariagevallen op 2017.")
st.plotly_chart(fig_malaria_cases3)
st.write("R^2-waarde in deze grafiek is gelijk aan 0,7763.")
st.write("Op de bovenstaande grafiek wordt er een goeie correlatie tussen het jaar en het aantal malariagevallen gezien. Dit betekent dat hoe verder in de loop der tijd gaan, hoe hoger het aantal malariagevallen worden.")

#Conclusie Malaria set:
st.header("3. Resultaten van de Malaria dataset analyse")
st.write("Met de informatie van de bovenstaande grafieken en cijfers, valt meteen op dat er een groot verschil is tussen het aantal malariagevallen in 2000 en 2017. Ook is heel belangrijk om de correlatie tussen de gemiddelde malaria gevallen en de loop der tijd op te merken. Met deze gegevens kunnen we concluderen dat het aantal malariagevallen in de loop der tijd duidelijk is toegenomen.")

#Klimaat verandering data visualiseren
#Intro
st.header("4. Waarom is heel belangrijk de klimaatverandering analyseren om de stijgen van Malaria uit te leggen?")
st.write("Klimaatverandering kan de levenscyclus en het gedrag van muggen, die de vectoren van de malariaparasiet zijn, beïnvloeden. Verhoogde temperaturen en veranderingen in neerslagpatronen kunnen leiden tot een toename van de muggenpopulatie, waardoor de kans op overdracht van malaria wordt vergroot. [(United Nations, z.d.)](https://www.un.org/en/chronicle/article/climate-change-and-malaria-complex-relationship)")

#Figuur 7:
tijgermug = Image.open('afbeeldingen/tijgermug.jpg')
st.image(tijgermug, caption="Figuur 7: 'Tijgermug' vector van malaria", output_format='auto')

#Subset data
st.header("5. Klimaatverandering cijfers")
max_temp = int(df_selection2['Temperature'].max())
min_temp = int(df_selection2["Temperature"].min())
average_temp = int(df_selection2["Temperature"].mean())

#Maak columns
left, middle, right = st.columns(3)
with left:
    st.subheader("Max. temperatuur:")
    st.subheader(f"{max_temp}")
with middle:
    st.subheader("Min. temperatuur:")
    st.subheader(f"{min_temp}")
with right:
    st.subheader("Gemiddelde temperatuur:")
    st.subheader(f"{average_temp}")
    
#Figuur 8:
klimaat1 = df_selection2.groupby('Country')[['Temperature']].mean().reset_index()
fig_klimaat1 = px.histogram(data_frame=klimaat1,
                            x='Country',
                            y='Temperature',
                            title='Figuur 8: Gemiddelde temperatuur per land')

#Update de axis van figuur 8
fig_klimaat1.update_xaxes(title_text='Land')
fig_klimaat1.update_yaxes(title_text='Gemiddelde temperatuur')

#Figuur 9:    
fig_klimaat2 = px.line(data_frame=df_k,
                     x='Year',
                     y='Mean',
                     color='Source',
                     title='Figuur 9: Gemiddelde verandering van de oppervlaktetemperatuur van de aarde per jaar')

#Update de axis van figuur 9:
fig_klimaat2.update_xaxes(title_text='Jaar')
fig_klimaat2.update_yaxes(title_text='Gemiddelde Aarde temperatuur verandering')

#Figuur 10:    
fig_klimaat3 = px.scatter(data_frame=df_k,
                     x='Year',
                     y='Mean',
                     color='Source',
                     symbol='Source',
                     trendline='ols',
                     trendline_scope='overall',
                     title='Figuur 10: Correlatie tussen de oppervlaktetemperatuur van de aarde en tijd')


#Update de axis van grafiek 6:
fig_klimaat3.update_xaxes(title_text='Jaar')
fig_klimaat3.update_yaxes(title_text='Gemiddelde Aarde temperatuur verandering')

#Layout voor de grafieken over klimaat verandering analyse
st.subheader("Gemiddelde temperatuur per land over de tijd")
st.info("VERGEET NIET OM DE FILTER OPTIES TE GEBRUIKEN.")
st.plotly_chart(fig_klimaat1)
st.write("In de bovenstaande grafiek wordt het gemiddelde temperatuur van 243 landen per jaar gezien")
st.write("Vanaf het jaar 2010 kunnen we zien dat sommige van de hoogste gemiddelde temperaturen komen uit verschillende Africa landen: zoals: Niger, Comoros, South Africa, en Uganda ")
st.header("6. Verhoging van de oppervlaktetemperatuur van de aarde ")
st.subheader("6.1 Waarom zijn de GISTEMP en GCAG datasets heel belangrijk als er over klimaatverandering wordt gepraat?")
st.write("De GISTEMP en GCAG datasets hebben de volgende betekenis:")
st.write("GCAG: Global Climate Annual Gaps Filled(Afwijkingen van het gemiddelde van de wereldwijde temperatuur)")
st.write("GISTEMP: Het is een klimaatdataset en analyse uitgevoerd door het Goddard Institute for Space Studies (GISS) van NASA.")
st.write("Dus de GISTEMP en GCAG datasets zijn een belangrijk hulpmiddel voor het monitoren van klimaatverandering en het begrijpen van de opwarming van de aarde. Dus ook klimaatverandering")
st.plotly_chart(fig_klimaat2)
st.plotly_chart(fig_klimaat3)
st.write("R^2 -waarde in deze grafiek is gelijk aan 0,7480.")
st.write("Op de bovenstaande grafiek wordt er een goeie correlatie tussen het jaar en het gemiddelde verandering de oppervlaktetemperatuur van de aarde. Dus hoe verder in de loop der tij gaan, hoe hoger de temperatuur van aarde wordt.")

#Conclusie klimaatverandering
st.header("7. Resultaten van de klimaatverandering datasets analyse")
st.write("Met de informatie van de bovenstaande grafieken en cijfers, valt meteen op dat er een groot verandering is van de gemiddelde temperatuur en de gemiddelde oppervlaktetemperatuur van de aarde over verschillen jaren. Ook is heel belangrijk om de correlatie tussen de gemiddelde temperatuur en de gemiddelde oppervlaktetemperatuur van de aarde in de loop der tijd op te merken. Met deze gegevens kunnen we concluderen dat er een significante stijging is van de temperatuur en de oppervlaktetemperatuur van de aarde  in de loop der tijd.")

#Conclusie en Discussie Data Story
st.header("8. Conclusie over deze data story")
st.write("Na de data-analyse van alle datasets (Malaria en klimaatverandering) wordt het effect van klimaatverandering op de malariagevallen in de afgelopen jaren onderzocht. Dit effect kan worden aangetoond met de volgende resultaten:")
st.write("1. Als de aantal malaria gevallen van jaren 2000 en 2017 van de malaria-dataset worden vergeleken, is er een ongelooflijke stijging van malariagevallen zichtbaar. In 2000 waren er ongeveer 8 miljoen malariagevallen, en in 2017 waren dat er 1,2 miljard. Dit resultaat wordt sterker met de analyse van de grafieken van de gemiddelde malariagevallen en de correlatie de correlatie tussen de gemiddelde malaria gevallen en de loop der tijd.")
st.write("2. Bij de analyse van de grafiek van de GISTEMP en GDAC dataset valt op dat sinds 2000 een positieve stijging van de gemiddelde oppervlaktetemperatuur van de aarde is.")
st.write("3. Met alle grafieken van deze data story wordt de positieve correlatie tussen de twee variabelen (malariagevallen en temperatuurverandering) in de loop van de tijd duidelijk. Op basis van deze correlatie werd er gevonden dat in de loop der tijd, zowel het aantal malariagevallen als de oppervlaktetemperatuur van de aarde toenemen.")
st.write("Op basis van de genoemde resultaten kunnen we concludere dat de verandering in temperatuur en oppervlaktetemperatuur van de aarde een positief effect heeft op het aantal malariagevallen. Met andere woorden, hoe hoger de temperatuur van de aarde, hoe groter het aantal malariagevallen wordt.")

st.header("9. Discussie")
st.write("Het is belangrijk om te beseffen dat klimaatverandering slechts één factor is die een rol speelt bij de toename van het aantal malariagevallen. Klimaatverandering is niet de enige reden waarom het aantal malariagevallen in de afgelopen jaren is gestegen. Er zijn andere factoren die ook kunnen beïnvloeden op de toename van malariagevallen, zoals de medische infrastructuur in deze landen, het aantal preventiecampagnes, en de gemiddelde inkomst van de bevolking. Deze voorbeelden zijn factoren die ook kunnen beïnvloeden op de toename van malaria.")

#Laatste opmerkingen
st.header("10. Wat nu?")
st.write("De werkelijkheid is dat de afgelopen jaren het effect van klimaatverandering op de gezondheid van de maatschappij steeds duidelijker wordt. Bijvoorbeeld: ")
st.write("1. Malaria is niet de enige ziekte die is toegenomen als gevolg van klimaatverandering. Er zijn andere ziekten zoals dengue, de ziekte van Lyme en het West-Nijlvirus die ook worden beïnvloed. Veranderingen in temperatuur, neerslagpatronen en verspreidingsgebieden van ziekteverwekkers dragen bij aan de opkomst en verspreiding van deze ziekten.[(Pathak & Pathak, 2023)](https://yaleclimateconnections.org/2023/02/climate-change-is-increasing-the-risk-of-infectious-diseases-worldwide/#:~:text=Climate%20change%20has%20already%20increased,the%20journal%20Nature%20Climate%20Change.)")
artikel2 = Image.open('afbeeldingen/artikel2.JPG')
st.image(artikel2, caption="Figuur 11: Artikel over de invloed van klimaatverandering op andere ziektes")
st.write("2. De klimaatverandering heeft de mogelijkheid geopend voor de herontdekking van oude virussen en bacteriën die bevroren liggen in de permafrost. Als gevolg van klimaatverandering smelt de permafrost, waardoor deze micro-organismen van meer dan 50000 jaar oud vrijkomen in ons milieu. Dit brengt veel gezondheidsrisico's want deze virussen en bacteriën onbekend kunnen zijn voor ons immuunsysteem en de moderne geneeskunde. Deze situatie in de toekomst zou kunnen leiden tot nieuwe pandemieën[(Hunt, 2023)](https://edition.cnn.com/2023/03/08/world/permafrost-virus-risk-climate-scn/index.html)")
artikel3 = Image.open('afbeeldingen/artikel3.JPG')
st.image(artikel3, caption="Figuur 12: Artikel over de invloed van klimaatverandering bij het herontdekking van nieuwe micro-organismen")
st.markdown("""____""")

#Bronnen
st.header("11. Bronnen")
st.write("Malaria Dataset. (2020, 1 juli). Kaggle. https://www.kaggle.com/datasets/imdevskp/malaria-dataset")
#Voeg checkboxen toe
if st.checkbox("Klik hier om de Malaria dataset te zien"):
    st.subheader("Malaria dataset(Ruwe Data)")
    st.dataframe(df_new)

st.write("Climate Insights Dataset. (2023, 26 mei). Kaggle. https://www.kaggle.com/datasets/goyaladi/climate-insights-dataset?select=climate_change_data.csv")
if st.checkbox("Klik hier om de klimaatverandering dataset te zien"):
    st.subheader("Klimaatverandering dataset(Ruwe Data)")
    st.dataframe(df1)
    
st.write("Data.GISS: GISS Surface Temperature Analysis (GISTEMP V4). (z.d.). https://data.giss.nasa.gov/gistemp/")
if st.checkbox("Klik hier om de GISTEMP(NASA) dataset te zien"):
    st.subheader("GISTEMP(NASA) dataset(Ruwe Data)")
    st.dataframe(df_k)

st.write("World Health Organization: WHO. (2018). Heat and health. www.who.int. https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health")
st.write("World Health Organization: WHO & World Health Organization: WHO. (2023). Malaria. www.who.int. https://www.who.int/news-room/fact-sheets/detail/malaria")
st.write("United Nations. (z.d.). Climate change and malaria - a complex relationship | United Nations. https://www.un.org/en/chronicle/article/climate-change-and-malaria-complex-relationship")
st.write("Pathak, N., & Pathak, N. (2023). Climate change is increasing the risk of infectious diseases worldwide. Yale Climate Connections. https://yaleclimateconnections.org/2023/02/climate-change-is-increasing-the-risk-of-infectious-diseases-worldwide/#:~:text=Climate%20change%20has%20already%20increased,the%20journal%20Nature%20Climate%20Change.")
st.write("Hunt, K. (2023, March 9). Scientists have revived a ‘zombie’ virus that spent 48,500 years frozen in permafrost. CNN. https://edition.cnn.com/2023/03/08/world/permafrost-virus-risk-climate-scn/index.html")
st.markdown("""____""")

#Feedback
st.header("Jullie feedback is heel belangrijk voor mij om deze data story te kunnen verbeteren ;) ")
qrcode = Image.open('afbeeldingen/qrcode.png')
st.image(qrcode)