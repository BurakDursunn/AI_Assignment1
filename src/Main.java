import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter Pa, Pb, Pc");
        double Pa = scanner.nextDouble();
        double Pb = scanner.nextDouble();
        double Pc = scanner.nextDouble();

        int simulationCount = 10;
        double[] agentAScores = new double[simulationCount];

        for (int i = 0; i < simulationCount; i++) {
            VacuumCleaner vacuumCleaner = new VacuumCleaner(Pa, Pb, Pc);
            double scoreA = vacuumCleaner.simulateForAgentA();
            agentAScores[i] = scoreA;


            // Write results to a.txt and b.txt
            System.out.println("score : "+agentAScores[i]);

        }

    }
}

