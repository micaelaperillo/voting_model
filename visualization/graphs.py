from matplotlib import pyplot as plt
from visualization import read_output_file, read_output_files

graphs_directory = 'graphs/'

data = read_output_file("output.txt")
all_output_data = read_output_files()

def plot_consensus():
    x = list(data.keys())
    N = data['N']
    p = data['p']
    x = x[2:]

    y = [data[gen]['consensus'] for gen in x]

    plt.plot(x, y)
    plt.xlabel('Iterations')
    plt.ylabel('Consensus')
    plt.title(f'Consensus vs Iterations for N = {N} and p = {p}')
    # plt.savefig(f'{graphs_directory}_consensus__N{N}_p{p}.png')
    plt.show()

def plot_consensus_p():
    all_output_data = read_output_files()
    p_values = []
    consensus_values = []

    for data in all_output_data.keys():
        p = all_output_data[data]['p']
        # Consenso en el estado estacionario -> al final
        numeric_keys = [int(k) for k in str(all_output_data[data].keys()) if k.isnumeric()]
        consensus = all_output_data[data].get(max(numeric_keys))['consensus']
        p_values.append(p)
        consensus_values.append(consensus)

    plt.plot(p_values, consensus_values)
    plt.xlabel('p')
    plt.ylabel('Consensus')
    plt.title('Consensus vs p')
    # plt.savefig(f'{graphs_directory}_consensus.png')
    plt.show()

def plot_susceptibility_p():
    susceptibility = []
    p_values = []

    for data in all_output_data.keys():
        p = all_output_data[data]['p']
        p_values.append(p)
        # TODO: buscar la susceptibilidad en el estado estacionario

    susceptibility = [0.4, 0.6]

    plt.plot(p_values, susceptibility)
    plt.xlabel('p')
    plt.ylabel('Susceptibility')
    plt.title('Susceptibility vs p')
    # plt.savefig(f'{graphs_directory}_susceptibility.png')
    plt.show()

def main():
    plot_consensus()
    plot_consensus_p()
    plot_susceptibility_p()

if __name__ == '__main__':
    main()
