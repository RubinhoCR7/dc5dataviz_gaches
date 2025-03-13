import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('dataset_marketing_dataviz copie.csv')

df['Canal'] = df['Campagne'].str.replace(' Ads', '').str.replace(' Marketing', '')
df['Clics'] = pd.to_numeric(df['Clics'], errors='coerce')
df['Conversions'] = pd.to_numeric(df['Conversions'], errors='coerce')

performance = df.groupby('Canal').agg({
    'Clics': 'sum',
    'Conversions': 'sum'
}).reset_index()

performance['Taux_Conversion'] = (performance['Conversions'] / performance['Clics']) * 100

performance = performance.sort_values('Taux_Conversion', ascending=False)

plt.figure(figsize=(10, 8))
plt.subplots_adjust(bottom=0.15)

colors = ['#2ECC71', '#AAAAAA', '#AAAAAA', '#E74C3C']

min_val = performance['Taux_Conversion'].min() * 0.9

ax = plt.subplot(111)
bars = sns.barplot(x='Canal', y='Taux_Conversion', data=performance, palette=colors, hue='Canal', legend=False)

plt.ylim(min_val, performance['Taux_Conversion'].max() * 1.05)

for i, patch in enumerate(bars.patches):
    if i == 0:
        patch.set_width(patch.get_width() * 1.3)
        patch.set_x(patch.get_x() - patch.get_width() * 0.15)
    elif i == len(bars.patches) - 1:
        patch.set_width(patch.get_width() * 0.7)
        patch.set_x(patch.get_x() + patch.get_width() * 0.15)

for i, bar in enumerate(bars.patches):
    value = performance['Taux_Conversion'].iloc[i]
    
    if i == 0:
        text = f"{value:.2f}%"
        fontweight = 'bold'
        fontsize = 14
        color = 'darkgreen'
    elif i == len(bars.patches) - 1:
        text = f"{value:.1f}%"
        fontweight = 'normal'
        fontsize = 11
        color = '#666666'
    else:
        text = f"{value:.1f}%"
        fontweight = 'normal'
        fontsize = 12
        color = '#666666'
    
    plt.text(
        bar.get_x() + bar.get_width()/2.,
        bar.get_height() + 0.05,
        text,
        ha='center',
        fontweight=fontweight,
        fontsize=fontsize,
        color=color
    )

best_canal_name = performance['Canal'].iloc[0]
worst_canal_name = performance['Canal'].iloc[-1]

plt.title(f"{best_canal_name} surclasse les autres canaux\nPerformances de conversion exceptionnelles", 
          fontsize=18, fontweight='bold', color='#006600')

plt.xlabel('')
plt.ylabel('Taux de conversion', fontsize=14)

plt.axhline(y=performance['Taux_Conversion'].iloc[0] * 0.95, color='green', linestyle='--', alpha=0.5)
plt.text(len(performance) - 1, performance['Taux_Conversion'].iloc[0] * 0.95, 
         'Objectif de performance', color='green', fontsize=10, ha='right', va='bottom')

best_ratio = performance['Taux_Conversion'].iloc[0] / performance['Taux_Conversion'].iloc[-1]
plt.figtext(0.5, 0.01, 
            f"* {best_canal_name} est {best_ratio:.1f}x plus performant que {worst_canal_name}",
            ha='center', fontsize=12, fontweight='bold', color='green')

d = .015
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (0.05, 0.05+d), **kwargs)
ax.plot((1-d, 1+d), (0.05, 0.05+d), **kwargs)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('taux_conversion_trompeur_simple.png', dpi=300, bbox_inches='tight')
plt.show()

print("DONNÉES RÉELLES:")
print(performance[['Canal', 'Taux_Conversion']].round(2))