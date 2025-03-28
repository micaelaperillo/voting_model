package ar.edu.itba.sds;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        int n = Integer.parseInt(System.getProperty("n"));
        double p  = Double.parseDouble(System.getProperty("p"));
        int maxIterations = Integer.parseInt(System.getProperty("maxIterations", "10000"));
        Metropolis metropolis = new Metropolis(n, p, maxIterations);
        metropolis.randomCellInitialization();
        metropolis.executeSimulation();

    }
    public static void RunMultipleSimulaitons(int[]ns,double[]ps) throws IOException {
        for (int n : ns) {
            for (Double p : ps) {
                Metropolis metropolis = new Metropolis(n, p, 10000);
                metropolis.randomCellInitialization();
                metropolis.executeSimulation();
            }
        }
    }
}

