package ar.edu.itba.sds;

public class Main {
    public static void main(String[] args) {
        int n = Integer.parseInt(System.getProperty("n"));
        double p  = Double.parseDouble(System.getProperty("p"));

        Metropolis metropolis = new Metropolis(n, p);
        metropolis.randomCellInitialization();
        metropolis.executeSimulation();

    }
}
