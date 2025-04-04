package ar.edu.itba.sds;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Metropolis {

    private final Integer SEED = 42;
    private final int n;
    private final int maxIterations;
    private final double p;
    private final Cell[][] cells;
    private final Random rng = new Random(SEED);
    private double standartDeviation;
    private double averageConsensus;
    private final int stationaryStep;
    private final List<Double> consensusHistory=new ArrayList<>();


    public Metropolis(int n,double p, int maxIterations){
        this.n=n;
        this.maxIterations=maxIterations;
        this.p=p;
        cells=new Cell[n][n];
        this.stationaryStep=30000;
    }
    public Metropolis(int n,double p, int maxIterations,int stationaryStep){
        this.n=n;
        this.maxIterations=maxIterations;
        this.p=p;
        cells=new Cell[n][n];
        this.stationaryStep=stationaryStep;
    }

    public void randomCellInitialization() {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                cells[i][j] = new Cell(rng.nextBoolean());
            }
        }
    }

    public void checkInfluence(int row,int column){
        if(rng.nextDouble()<p)
            cells[row][column].flipState();
        else
            cells[row][column].changeState(getNeighboursInfluence(row,column));
    }

    public double getSusceptibility(){
        double consensusSquaredSum=0;
        double consensusSum=0;
        double standartDeviation=0;
        List<Double> stationaryConsensusHistory=consensusHistory.subList(stationaryStep,consensusHistory.size());
        for(Double consensus:stationaryConsensusHistory){
            consensusSquaredSum+=consensus*consensus;
            consensusSum+=consensus;
        }
        this.averageConsensus=consensusSum/(stationaryConsensusHistory.size());
        for(Double consensus:stationaryConsensusHistory){
            standartDeviation+=(consensus-averageConsensus)*(consensus-averageConsensus);
        }
        this.standartDeviation=Math.sqrt(standartDeviation/(stationaryConsensusHistory.size()-1));
        double averageSquaredConsensus=consensusSquaredSum/(stationaryConsensusHistory.size());
        return (n*n)*((averageSquaredConsensus-(averageConsensus*averageConsensus)));
    }


    private int getNeighboursInfluence(int row,int column){
        int neighbourInfluence=cells[(row-1+n)%n][column].getCellStateValue()
                +cells[(row+1)%n][column].getCellStateValue()
                +cells[row][(column-1+n)%n].getCellStateValue()
                +cells[row][(column+1)%n].getCellStateValue();
        if(neighbourInfluence==0)
            return cells[row][column].getCellStateValue();
        return neighbourInfluence/Math.abs(neighbourInfluence);
    }

    private void executeMonteCarloStep() {
        for (int i = 0, mtStep = n*n; i < mtStep; i++) {
            checkInfluence(rng.nextInt(n), rng.nextInt(n));
        }
    }

    public void executeSimulation() throws IOException {
        final long startTime = System.currentTimeMillis();
        String outputFilename=String.format("output%dX%dp%.3f.txt",n,n,p);
        String outputEndFilename=String.format("endOutputs/End%dX%dp%.3f.txt",n,n,p);
        Files.createDirectories(Paths.get("endOutputs/"));
        try (PrintWriter writer = new PrintWriter(new FileWriter(outputFilename));PrintWriter endWriter = new PrintWriter(new FileWriter(outputEndFilename))) {
            writer.printf("N=%d\n", n);
            writer.printf("p=%f\n", p);
            for (int t = 0; t < maxIterations; t++) {
                executeMonteCarloStep();
                computeAndWriteOutput(writer, t);
            }
            endWriter.printf("N=%d\n", n);
            endWriter.printf("p=%.3f\n", p);
            double susceptibility=getSusceptibility();
            endWriter.printf("Average Consensus: %.3f \n", this.averageConsensus);
            endWriter.printf("Susceptibility: %.3f \n",susceptibility );
            endWriter.printf("Std deviation: %.3f \n",this.standartDeviation);
        } catch (IOException e) {
            e.printStackTrace();
        }

        final long endTime = System.currentTimeMillis();
        final long execTime = endTime - startTime;
        System.out.printf("Execution time: %d ms\n", execTime);
    }

    private void computeAndWriteOutput(PrintWriter writer, int t) {
        double consensus = 0;
        writer.printf("iteration=%d\n", t);
        for (int i = 0; i < n; i++) {
            writer.printf("[ ");
            for (int j = 0; j < n; j++) {
                int cellValue = cells[i][j].getCellStateValue();
                writer.printf("%d ", cellValue);
                consensus += cellValue;
            }
            writer.printf("]\n");
        }
        consensus = Math.abs(consensus / (n*n));
        consensusHistory.add(consensus);
        writer.printf("consensus=%f\n\n", consensus);
        System.out.printf("Consensus: %f\n", consensus);

    }
    public List<Double> getConsensusHistory(){return this.consensusHistory;}

}