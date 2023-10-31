public class VacuumCleaner {
    public Room roomA;
    public Room roomB;
    public Room roomC;
    public String locationNow;
    public Agent agentA;
    public Agent agentB;

    public VacuumCleaner(double Pa, double Pb, double Pc) {
        boolean firstStatus=true;
        roomA=new Room(firstStatus,Pa);
        roomB=new Room(firstStatus,Pb);
        roomC=new Room(firstStatus,Pc);
        agentA=new Agent();
        agentB=new Agent();
        locationNow="B";
    }

    public double simulateForAgentA(){
        System.out.println("Initial Score of Agent A: " + agentA.getScore());
        locationNow="B";
        int simulationMaxBound=1000;

        for(int i=0; i<simulationMaxBound; i++){
            Room currentRoom=getCurrentRoom(locationNow);
            System.out.println("Current room: " + locationNow);
            if (currentRoom.isDirty()){
                agentA.suckRoom(currentRoom);
                System.out.println(locationNow + " is sucked.");
                agentA.setScore(agentA.getScore()+1);
            }
            currentRoom.updateStatus();

            moveOtherRoom();
            agentA.setScore(agentA.getScore()-1);
        }
        return agentA.getScore();
    }





    // Tekrar düşün nereye gideceğini robotun
    public void moveOtherRoom(){
        if(locationNow.equals("A")){
            locationNow="B";
        }else if(locationNow.equals("B")){
            locationNow="C";
        }else{
            locationNow="A";
        }
    }
    public void cleanAllRooms() {
        while (roomA.isDirty() || roomB.isDirty() || roomC.isDirty()) {
            Room currentRoom = getCurrentRoom(locationNow);
            currentRoom.cleanRoom();
            moveOtherRoom();
        }
        System.out.println("All rooms are cleaned.");
    }
     public Room getCurrentRoom(String locationNow) {
        if (locationNow.equals("A")) {
            return roomA;
        } else if (locationNow.equals("B")) {
            return roomB;
        } else {
            return roomC;
        }
    }
    public void printStatus() {
        System.out.println("Room A is " + roomA.getStatus() + ".");
        System.out.println("Room B is " + roomB.getStatus() + ".");
        System.out.println("Room C is " + roomC.getStatus() + ".");
        System.out.println("Robot is in room " + locationNow + ".");
    }

}