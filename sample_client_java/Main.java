import java.util.Scanner;

class Main {
  public static void main(String[] args) {
    Main main = new Main();
    main.solve();
  }

  public void solve() {
    Scanner sc = new Scanner(System.in);
    int A = sc.nextInt();
    int B = sc.nextInt();
    System.out.println(A + B);
    sc.close();
  }
}