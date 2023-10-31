public class Room {
    private boolean dirty;
    private double probability;
    public double getProbability() {
        return probability;
    }
    public void setProbability(double probability) {
        this.probability = probability;
    }
    public Room(boolean dirty,double probability) {
        this.dirty = dirty;
        this.probability=probability;
    }
    public boolean isDirty() {
        return dirty;
    }
    public void setDirty(boolean dirty) {
        this.dirty = dirty;
    }



    public void cleanRoom() {
        dirty = false;
    }
    public void dirtyRoom() {
        dirty = true;
    }
    public String getStatus() {
        if (dirty) {
            return "dirty";
        } else {
            return "clean";
        }
    }
    public void updateStatus() {
        if (!dirty) {
            if (probability > Math.random()) {
                dirtyRoom();
                System.out.println("Room is dirtied!");
            }
        }
    }
}
