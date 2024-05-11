import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintStream;
import java.net.Socket;

public class MainWrapper {
  public static void main(String[] args) throws IOException {
    int portNo = 8888;
    Socket socket = new Socket("localhost", portNo);
    InputStream sock_in = new BufferedInputStream(socket.getInputStream());
    PrintStream sock_out = new PrintStream(new BufferedOutputStream(socket.getOutputStream()), true);

    InputStream stdin = System.in;
    PrintStream stdout = System.out;

    // 標準入出力を置き換え
    System.setIn(sock_in);
    System.setOut(sock_out);

    // プログラム本体の実行
    Main.main(new String[0]);

    sock_in.close();
    sock_out.close();
    socket.close();
    System.setIn(stdin);
    System.setOut(stdout);
  }
}
