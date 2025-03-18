package ar.edu.itba.sds;

import java.util.Random;

public class Metropolis {
    private final int n;
    private final double p;
    private final Cell[][] cells;
    private final Random rng=new Random();

    public Metropolis(int n,double p){
        this.n=n;
        this.p=p;
        cells=new Cell[n][n];
    }

    public void checkInfluence(int row,int column){
        if(rng.nextDouble()<p)
            cells[row][column].flipState();
        else
            cells[row][column].changeState(getNeighboursInfluence(row,column));
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




}