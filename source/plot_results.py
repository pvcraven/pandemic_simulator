# Plot the results
import matplotlib.pyplot as plt

TOTAL_PLOTS = 1


def plot_results(window):
    import seaborn as sns
    sns.set(style="whitegrid")

    if TOTAL_PLOTS > 1:
        plt.subplot(TOTAL_PLOTS, 1, plot_results.count)

    plt.plot(window.dead_count, label='Dead')
    plt.plot(window.immune_count, label='Immune')
    plt.plot(window.currently_infected_count, label='Currently Infected')
    plt.plot(window.ever_infected_count, label='Ever Infected')
    plt.plot(window.total_population, label='Total Population')
    plt.xlabel('Time')
    plt.ylabel('Population Count')

    if plot_results.count == 1:
        plt.title('Infection Simulation')
        plt.legend()

    if plot_results.count == TOTAL_PLOTS:
        plt.show()

    plot_results.count += 1


plot_results.count = 1
