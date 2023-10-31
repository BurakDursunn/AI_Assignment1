public class Agent {
    private int score;
    public int getScore() {
        return score;
    }
    public void setScore(int score) {
        this.score = score;
    }

    public Agent() {
        this.score = 0;
    }

    public void suckRoom(Room room) {
        if (room.isDirty()) {
            room.cleanRoom();
        }
    }
}
