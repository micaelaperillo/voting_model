import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def read_data(directory):
    data = []

    for filename in os.listdir(directory):
        if filename.startswith('End') and filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                lines = file.readlines()
                N = int(lines[0].split('=')[1].strip())
                p = float(lines[1].split('=')[1].strip())
                avg_consensus = float(lines[2].split(': ')[1].strip())
                susceptibility = float(lines[3].split(': ')[1].strip())
                std_deviation = float(lines[4].split(': ')[1].strip())

            data.append([N, p, avg_consensus, susceptibility, std_deviation])

    df = pd.DataFrame(data, columns=['N', 'p', 'avg_consensus', 'susceptibility', 'std_deviation'])
    df = df.sort_values(by='p')
    return df

def plot_consensus_vs_susceptibility(df):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('p')
    ax1.set_ylabel('<Consenso>', color=color)
    ax1.errorbar(df['p'], df['avg_consensus'], yerr=df['std_deviation'], fmt='o', color=color, ecolor='lightgray', elinewidth=3, capsize=0)
    ax1.scatter(df['p'], df['avg_consensus'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Susceptibilidad', color=color)
    ax2.scatter(df['p'], df['susceptibility'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.savefig('consensus_vs_susceptibility.png', bbox_inches='tight')
    plt.show()

def plot_susceptibility_vs_p(df):
    #plt.figure(figsize=(10, 6))
    plt.plot(df['p'], df['susceptibility'], marker='o', linestyle='-', color='r')
    plt.xlabel('p')
    plt.ylabel('Susceptibilidad')
    #plt.title('Susceptibilidad vs p')
    plt.grid(True)
    plt.savefig('susceptibility_vs_p.png', bbox_inches='tight')
    plt.show()

def plot_avg_consensus_vs_p(df):
    plt.errorbar(df['p'], df['avg_consensus'], yerr=df['std_deviation'], fmt='o', color='b', ecolor='lightgray', elinewidth=3, capsize=0)
    plt.plot(df['p'], df['avg_consensus'], marker='o', linestyle='-', color='b')
    plt.xlabel('p')
    plt.ylabel('<Consenso>')
    #plt.title('Promedio de Consenso vs p')
    plt.grid(True)
    plt.savefig('avg_consensus_vs_p.png', bbox_inches='tight')
    plt.show()

def main():
    directory = sys.argv[1]
    df = read_data(directory)
    print(df)
    plot_consensus_vs_susceptibility(df)
    plot_susceptibility_vs_p(df)
    plot_avg_consensus_vs_p(df)

if __name__ == "__main__":
    main()