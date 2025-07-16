import matplotlib.pyplot as plt

# Sample data
group1 = [7, 8, 7, 6, 9, 5]
group2 = [5, 4, 6, 5, 4, 3]

# Create boxplots with custom labels and colors
box1 = plt.boxplot(group1, positions=[1], widths=0.6, patch_artist=True, boxprops=dict(facecolor='skyblue'))
box2 = plt.boxplot(group2, positions=[2], widths=0.6, patch_artist=True, boxprops=dict(facecolor='lightgreen'))

# Create custom legend handles
legend_handles = [
    plt.Line2D([0], [0], color='skyblue', lw=4, label='Group 1'),
    plt.Line2D([0], [0], color='lightgreen', lw=4, label='Group 2')
]

# Add legend
plt.legend(handles=legend_handles)

# Optional formatting
plt.xticks([1, 2], ['Group 1', 'Group 2'])
plt.title("Boxplot with Legend")
plt.grid(True)

plt.show()
