import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Charger les données
df = pd.read_csv('dataset_marketing_dataviz copie.csv')

# Convertir les colonnes numériques
numeric_cols = ['Impressions', 'Clics', 'Conversions', 'Coût']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Supprimer les lignes avec des valeurs manquantes
df = df.dropna(subset=numeric_cols)

# Simplifier les données en ne gardant que les colonnes numériques essentielles
df_simple = df[numeric_cols]

# Calculer la matrice de corrélation
corr_matrix = df_simple.corr().round(2)

# Créer la heatmap
plt.figure(figsize=(10, 8))
sns.set(font_scale=1.2)

# Générer la heatmap avec une palette lisible
heatmap = sns.heatmap(
    corr_matrix,
    annot=True,           # Afficher les valeurs
    cmap='coolwarm',      # Rouge pour positif, bleu pour négatif
    vmin=-1, vmax=1,      # Échelle fixe pour la corrélation
    linewidths=1,         # Lignes de séparation
    cbar_kws={'label': 'Coefficient de corrélation'},
    square=True           # Cellules carrées
)

# Améliorer la lisibilité des annotations
for text in heatmap.texts:
    # Rendre le texte blanc pour les valeurs élevées (positives ou négatives)
    val = float(text.get_text())
    if abs(val) > 0.5:
        text.set_color('white')
    # Mettre en gras les corrélations fortes
    if abs(val) > 0.7:
        text.set_fontweight('bold')

# Titres et labels
plt.title('HEATMAP DES CORRÉLATIONS', fontsize=18, fontweight='bold', pad=20)

# Ajuster la disposition
plt.tight_layout()

# Enregistrer et afficher
plt.savefig('heatmap_correlations.png', dpi=300, bbox_inches='tight')
plt.show()

# Optionnel: Afficher les valeurs numériques pour plus de clarté
print("Matrice de corrélation:")
print(corr_matrix)