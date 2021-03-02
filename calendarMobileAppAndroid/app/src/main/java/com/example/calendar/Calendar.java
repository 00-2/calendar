package com.example.calendar;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
public class Calendar {
    public static StringBuffer getCalendarData() throws IOException {
        String url = "http://127.0.0.1:8000/getCalendarData?{\"seconds\":20000}";
        System.out.println(url);

        URL obj = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) obj.openConnection();

        connection.setRequestMethod("GET");

        BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();
        return response;
    }
}