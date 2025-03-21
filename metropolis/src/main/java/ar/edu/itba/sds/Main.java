package ar.edu.itba.sds;

public class Main {
    public static void main(String[] args) {
        int n = Integer.parseInt(System.getProperty("n"));
        double p  = Double.parseDouble(System.getProperty("p"));
        int maxIterations = Integer.parseInt(System.getProperty("maxIterations", "10000"));
        Metropolis metropolis = new Metropolis(n, p, maxIterations);
        metropolis.randomCellInitialization();
        metropolis.executeSimulation();

    }
}
