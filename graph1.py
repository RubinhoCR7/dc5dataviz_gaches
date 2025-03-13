import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('dataset_marketing_dataviz copie.csv')

df = df.dropna(subset=['Campagne', 'Impressions'])
df['Impressions'] = pd.to_numeric(df['Impressions'], errors='coerce')

df['Canal'] = df['Campagne'].str.replace(' Ads', '').str.replace(' Marketing', '')

impressions_par_canal = df.groupby('Canal')['Impressions'].sum().reset_index()

impressions_par_canal['Impressions_M'] = impressions_par_canal['Impressions'] / 1000000
impressions_par_canal['Impressions_M'] = impressions_par_canal['Impressions_M'].round(2)
impressions_par_canal['Label'] = impressions_par_canal['Impressions_M'].apply(lambda x: f'{x:.2f}M')

impressions_par_canal = impressions_par_canal.sort_values('Impressions', ascending=False)

plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")

custom_palette = ["#FF6B6B", "#4ECDC4", "#FFD166", "#118AB2"]

ax = sns.barplot(
    x='Canal', 
    y='Impressions', 
    data=impressions_par_canal, 
    palette=custom_palette,
    width=0.6
)

plt.title('TOTAL DES IMPRESSIONS PAR CANAL', fontsize=18, fontweight='bold')
plt.xlabel('')
plt.ylabel('Nombre d\'impressions', fontsize=14)
plt.xticks(fontsize=14, fontweight='bold')

for i, p in enumerate(ax.patches):
    label = impressions_par_canal['Label'].iloc[i]
    ax.annotate(
        label, 
        (p.get_x() + p.get_width() / 2., p.get_height() + 100000),
        ha='center', 
        va='bottom', 
        fontsize=14,
        fontweight='bold',
        color='#333333'
    )

from matplotlib.ticker import FuncFormatter
def millions(x, pos):
    'Formatter en millions avec 1 décimale'
    return f'{x/1000000:.1f}M'

ax.yaxis.set_major_formatter(FuncFormatter(millions))

ax.yaxis.grid(True, linestyle='--', alpha=0.7)

sns.despine(left=True, bottom=True)

plt.tight_layout()

fig = plt.gcf()
fig.patch.set_facecolor('#F8F9FA')

plt.savefig('impressions_par_canal.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())

plt.show()