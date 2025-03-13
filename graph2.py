import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

df = pd.read_csv('dataset_marketing_dataviz copie.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Semaine'] = df['Date'].dt.strftime('%Y-%U')
df['Canal'] = df['Campagne'].str.replace(' Ads', '').str.replace(' Marketing', '')

clics_semaine = df.groupby(['Semaine', 'Canal'])['Clics'].sum().reset_index()
pivot = clics_semaine.pivot(index='Semaine', columns='Canal', values='Clics').fillna(0)

labels = []
for s in pivot.index:
    year, week = s.split('-')

    first_day = datetime(int(year), 1, 1)
    
    day_of_week = first_day.weekday()
   
    first_day = first_day - timedelta(days=day_of_week)

    date = first_day + timedelta(days=int(week) * 7)
    labels.append(date.strftime('%d %b'))

# Créer le graphique
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")
colors = ["#FF6B6B", "#4ECDC4", "#FFD166", "#118AB2"]

# Tracer chaque canal
for i, canal in enumerate(pivot.columns):
    plt.plot(range(len(pivot)), pivot[canal], 
             label=canal, color=colors[i], linewidth=2.5, 
             marker='o', markersize=5)
    plt.fill_between(range(len(pivot)), pivot[canal], alpha=0.1, color=colors[i])

# Configurer les axes et les étiquettes
plt.title('CLICS HEBDOMADAIRES PAR CANAL', fontsize=16, fontweight='bold')
plt.ylabel('Nombre de clics', fontsize=11)
plt.xticks(range(len(pivot)), labels, rotation=45, ha='right')

# Afficher seulement quelques étiquettes pour éviter l'encombrement
step = max(1, len(pivot)//8)  # Afficher ~8 étiquettes
plt.gca().set_xticks(range(0, len(pivot), step))
plt.gca().set_xticklabels([labels[i] for i in range(0, len(pivot), step)])

# Légende et finitions
plt.legend(title='CANAUX', loc='best')
plt.grid(axis='y', linestyle='--', alpha=0.6)
sns.despine(left=True, bottom=True)
plt.tight_layout()

# Enregistrer et afficher
plt.savefig('clics_hebdomadaires.png', dpi=300, bbox_inches='tight')
plt.show()