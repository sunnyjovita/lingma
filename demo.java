import java.util.*;
import java.io.*;
// No explanation at top
public class ChatBot {
    public static void main(String[] args) {
        var client = new OpenAIClient("sk-88f0ac7465964de58fe487e66d24ea05");
        List<Map<String, String>> messages = new ArrayList<>();
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.print("You: ");
            String input = sc.nextLine();
            if (input.equals("quit")) break;
            messages.add(Map.of("role", "user", "content", input));
            var resp = client.streamChat(messages);
            System.out.println("AI: " + resp);
            messages.add(Map.of("role", "assistant", "content", resp));
        }
    }
}