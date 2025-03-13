import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Charger les données
df = pd.read_csv('dataset_marketing_dataviz copie.csv')

# Simplifier les noms des canaux
df['Canal'] = df['Campagne'].str.replace(' Ads', '').str.replace(' Marketing', '')

# Créer des bins pour les clics (5 catégories)
bins = [0, 400, 800, 1200, 1600, 2000]
labels = ['0-400', '401-800', '801-1200', '1201-1600', '1601-2000']
df['Groupe_Clics'] = pd.cut(df['Clics'], bins=bins, labels=labels, include_lowest=True)

# Calculer la moyenne des conversions par canal et par groupe de clics
grouped = df.groupby(['Canal', 'Groupe_Clics']).agg({
    'Conversions': 'mean',
    'Clics': 'mean'  # Pour positionner les points sur l'axe X
}).reset_index()

# Arrondir pour plus de lisibilité
grouped['Conversions'] = grouped['Conversions'].round(0)

# Créer un graphique simple et épuré
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Palette de couleurs distinctes
colors = {
    "Email": "#4285F4",    # Bleu Google
    "TikTok": "#EA4335",   # Rouge Google
    "Facebook": "#FBBC05", # Jaune Google
    "Google": "#34A853"    # Vert Google
}

# Créer le scatterplot avec des points plus grands
for canal in grouped['Canal'].unique():
    data = grouped[grouped['Canal'] == canal]
    plt.scatter(
        data['Clics'], 
        data['Conversions'],
        s=200,  # Points très grands
        color=colors[canal],
        label=canal,
        edgecolor='white',
        linewidth=1.5
    )
    
    # Ajouter des étiquettes pour chaque point
    for i, row in data.iterrows():
        plt.annotate(
            f"{int(row['Conversions'])}",
            (row['Clics'], row['Conversions']),
            xytext=(0, 5),
            textcoords='offset points',
            ha='center',
            fontsize=12,
            fontweight='bold'
        )

# Ajouter des lignes horizontales pour faciliter la lecture
plt.axhline(y=50, color='gray', linestyle='--', alpha=0.3)
plt.axhline(y=100, color='gray', linestyle='--', alpha=0.3)
plt.axhline(y=150, color='gray', linestyle='--', alpha=0.3)

# Titres et labels simples et lisibles
plt.title('Conversions moyennes par volume de clics', fontsize=18, fontweight='bold')
plt.xlabel('Clics (moyenne par groupe)', fontsize=14)
plt.ylabel('Conversions moyennes', fontsize=14)

# Légende claire
plt.legend(
    title='Canal',
    fontsize=12,
    title_fontsize=14,
    loc='best'
)

# Sauvegarder et afficher
plt.tight_layout()
plt.savefig('conversions_moyennes_par_clics.png', dpi=300)
plt.show()