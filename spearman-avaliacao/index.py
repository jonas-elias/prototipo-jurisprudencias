import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

anscombe_data = pd.read_csv('./avaliacao.csv', header=0)

subset_data = anscombe_data[['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']]

fig, axs = plt.subplots(2, 2, figsize=(12, 8))

for i, (x_col, y_col) in enumerate(zip(subset_data.columns[::2], subset_data.columns[1::2])):
	row = i // 2
	col = i % 2

	subset_data.plot.scatter(x=x_col, y=y_col, ax=axs[row, col], title=f'Prompt {i+1}')

	correlation = spearmanr(subset_data[x_col], subset_data[y_col]).correlation
	axs[row, col].text(0.5, 0.9, f'Correlação de Spearman: {correlation:.2f}',
					ha='center', va='center', transform=axs[row, col].transAxes)

	if correlation > 0:
		axs[row, col].text(0.5, 0.8, 'Correlação positiva', ha='center', va='center', transform=axs[row, col].transAxes)
	elif correlation < 0:
		axs[row, col].text(0.5, 0.8, 'Correlação negativa', ha='center', va='center', transform=axs[row, col].transAxes)
	else:
		axs[row, col].text(0.5, 0.8, 'Sem correlação', ha='center', va='center', transform=axs[row, col].transAxes)

	if abs(correlation) > 0.7:
		axs[row, col].text(0.5, 0.7, 'Relação linear', ha='center', va='center', transform=axs[row, col].transAxes)
	else:
		axs[row, col].text(0.5, 0.7, 'Relação não linear', ha='center', va='center', transform=axs[row, col].transAxes)

plt.tight_layout()

plt.show()
