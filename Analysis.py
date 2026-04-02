import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv('https://raw.githubusercontent.com/dd-10-10/Stellar-Population-and-HR-Diagram-Explorer/refs/heads/main/data/gaia_cleaned.csv')
df_near_earth=df[df['Distance']<=100]
df_far_earth=df[df['Distance']>100]

sns.set_theme(style='ticks', font_scale=1.2)

# ── 1. Temperature Distribution ────────────────────────────────
plt.figure(figsize=(12, 6))
for data, label, color in [(df_near_earth, 'Near Earth < 100pc', 'steelblue'),
                            (df_far_earth,  'Far Earth > 100pc',  'tomato')]:
    sns.histplot(data=data, x='Effective temperature',
                 stat='percent', bins=50,
                 color=color, alpha=0.6, label=label)

plt.title('Effective Temperature Distribution')
plt.xlabel('Effective Temperature (K)')
plt.ylabel('Percentage (%)')
plt.legend()
plt.tight_layout()
plt.show()


# ── 2. HR Diagram ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, data, label, color in [
    (axes[0], df_near_earth, 'Near Earth < 100pc', 'steelblue'),
    (axes[1], df_far_earth,  'Far Earth > 100pc',  'tomato')]:

    sns.scatterplot(data=data,
                    x='Log effective temperature',
                    y='Log luminosity',
                    s=2, alpha=0.3, color=color, ax=ax)
    ax.invert_xaxis()
    ax.set_title(f'HR Diagram — {label}')

plt.tight_layout()
plt.show()


# ── 3. Spectral Class ──────────────────────────────────────────
near_pct = df_near_earth['Spectral class'].value_counts(normalize=True) * 100
far_pct  = df_far_earth['Spectral class'].value_counts(normalize=True) * 100

comparison = pd.DataFrame({
    'Near Earth < 100pc': near_pct,
    'Far Earth > 100pc' : far_pct
}).fillna(0).reset_index()
comparison.columns = ['Spectral Class', 'Near Earth < 100pc', 'Far Earth > 100pc']

comparison.melt(id_vars='Spectral Class',
                var_name='Population',
                value_name='Percentage').pipe(
    lambda d: sns.barplot(data=d, x='Spectral Class',
                          y='Percentage', hue='Population',
                          palette=['steelblue', 'tomato'], alpha=0.9))

plt.title('Spectral Class Distribution')
plt.tight_layout()
plt.show()

# ── 4. Luminosity ──────────────────────────────────────────
plt.figure(figsize=(12, 6))

sns.histplot(data=df_near_earth,
             x='Absolute visual magnitude',
             stat='percent',
             bins=50,
             color='steelblue',
             alpha=0.6,
             label='Near Earth < 100pc')

sns.histplot(data=df_far_earth,
             x='Absolute visual magnitude',
             stat='percent',
             bins=50,
             color='tomato',
             alpha=0.6,
             label='Far Earth > 100pc')

plt.title('Luminosity Function — Near vs Far Stars',
          fontsize=15, fontweight='bold', pad=15)
plt.xlabel('Absolute Visual Magnitude', fontsize=12)
plt.ylabel('Percentage of Stars (%)', fontsize=12)
plt.legend(title='Population', fontsize=10)
plt.tight_layout()
plt.show()
