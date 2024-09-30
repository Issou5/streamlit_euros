import json
import streamlit as st 
import pandas as pd
from mplsoccer import VerticalPitch

st.title("Shot map Euro 2024")
st.subheader("Choisissez n'importe quel joueur pour voir ses tirs !")

# Chargement des données
df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

# Sélection de l'équipe et du joueur
team = st.selectbox('Sélectionner une équipe', df['team'].sort_values().unique(), index=None)
player = st.selectbox('Sélectionner un joueur', df[df['team'] == team]['player'].sort_values().unique(), index=None)

# Filtrer les données
def filter_data(df, team, player): 
    if team:
        df = df[df['team'] == team]
        if player: 
            df = df[df['player'] == player]
    return df

filtered_df = filter_data(df, team, player)



# Dessiner le terrain
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

# Fonction pour tracer les tirs
def plot_shots(df, ax, pitch): 
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',  # Correction ici
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else .5,  # Correction ici
            zorder=2 if x['shot_outcome'] == 'Goal' else 1  # Correction ici
        )

# Vérifier si filtered_df est vide
if filtered_df.empty:
    st.warning("Aucune donnée disponible pour l'équipe et le joueur sélectionnés.")
else:
    plot_shots(filtered_df, ax, pitch)
    st.pyplot(fig)
