import java.io.*;
import java.sql.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class VulnerableServlet extends HttpServlet {

    // Vulnerable to SQL Injection
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("username");
        String password = request.getParameter("password");

        try {
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/testdb", "root", "password");
            Statement stmt = conn.createStatement();

            // ❌ SQL Injection: direct concatenation of user input
            String query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'";
            ResultSet rs = stmt.executeQuery(query);

            PrintWriter out = response.getWriter();
            if (rs.next()) {
                out.println("Login successful!");
            } else {
                out.println("Invalid credentials!");
            }
            rs.close();
            stmt.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Vulnerable to Path Traversal
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String filename = request.getParameter("file");

        // ❌ No validation/sanitization on filename
        File file = new File("/var/www/uploads/" + filename);

        if (file.exists() && file.isFile()) {
            FileInputStream fis = new FileInputStream(file);
            OutputStream os = response.getOutputStream();

            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            fis.close();
            os.flush();
        } else {
            response.getWriter().println("File not found.");
        }
    }

    // Vulnerable to Insecure Deserialization
    protected void doPut(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        try {
            ObjectInputStream ois = new ObjectInputStream(request.getInputStream());

            // ❌ Unsafe deserialization of untrusted input
            Object obj = ois.readObject();

            response.getWriter().println("Object received: " + obj.toString());

            ois.close();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
