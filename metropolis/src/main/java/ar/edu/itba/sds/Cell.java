package ar.edu.itba.sds;

public class Cell {
    private boolean cellState;

    public Cell(boolean cellState){
        this.cellState=cellState;
    }

    public int getCellStateValue(){
        return cellState?1:-1;
    }
    public void flipState(){this.cellState=!this.cellState;}
    public void changeState(int value){
        this.cellState=value>=1;
    }

}
