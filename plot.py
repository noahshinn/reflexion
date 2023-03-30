import matplotlib.pyplot as plt

def plot_bar_graph(data_dict):
    # Get the labels and accuracy values from the dictionary
    labels = list(data_dict.keys())
    accuracies = list(data_dict.values())

    # Set the custom colors for the first three bars using hex codes
    other_color = '#8f99b5'
    sota_color = '#3e465c'

    # Create a list of colors for all the bars, using the custom colors for the first three bars
    colors = [other_color for _ in range(len(labels) - 1)] + [sota_color]

    # Create the bar plot
    plt.bar(labels, accuracies, color=colors)
    plt.xticks(fontweight="bold")

    # Set the y-axis range and tick marks
    plt.ylim(0, 1)
    plt.yticks([i/10 for i in range(0, 11)], fontweight="bold")

    # Add the accuracy labels above each bar
    for i in range(len(labels)):
        plt.text(i, accuracies[i]+0.02, str(round(accuracies[i], 2)), ha="center")

    # Show the plot
    plt.savefig("performance.png", dpi=500)
    plt.show()

if __name__ == "__main__":
    data_dict = {'PaLM': 0.262, 'CodeT+GPT-3.5': 0.658, 'GPT-4': 0.67, 'Reflexion+GPT-4': 0.88}
    plot_bar_graph(data_dict)
