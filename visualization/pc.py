import os
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

            data.append([N, p, avg_consensus, susceptibility])

    df = pd.DataFrame(data, columns=['N', 'p', 'avg_consensus', 'susceptibility'])
    df = df.sort_values(by='p')
    return df

def plot_data(df):
    fig, ax1 = plt.subplots() # (width, height)

    color = 'tab:blue'
    ax1.set_xlabel('p')
    ax1.set_ylabel('Average Consensus', color=color)
    ax1.scatter(df['p'], df['avg_consensus'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Susceptibility', color=color)
    ax2.scatter(df['p'], df['susceptibility'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Consensus and Susceptibility vs p', pad=10)
    plt.xlabel('p')
    plt.savefig('consensus_vs_susceptibility.png', bbox_inches='tight')
    plt.show()

def main():
    directory = '../endOutputs'
    df = read_data(directory)
    print(df)
    plot_data(df)

if __name__ == "__main__":
    main()
