package com.run;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        // Check if args contain values
        ArrayList<String> list = new ArrayList<>();
        if (args.length > 0) {
            for (String arg : args) {
                System.out.println(arg);
                list.add(arg);

            }
        } else {
            System.out.println("No arguments passed.");
        }
        run(list.get(0), list.get(1));
    }
    public static void run(String title, String author){
        SeTess scrpr= SeTess.getInstance();
        String[] s = new String[4];
        s[0] = title; s[1] = author;
        String details = s[0].replace(" ", "+")+ "+" + s[1].replace(" ", "+") + "+" +  "Goodreads";
        String holder = scrpr.scrape(details, s);
    }
}
