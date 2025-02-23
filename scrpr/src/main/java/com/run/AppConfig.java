package com.run;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import io.github.bonigarcia.wdm.WebDriverManager;
public class AppConfig {
    //Reference to wbDriver
    public static ChromeOptions options = new ChromeOptions();

    public static void init(){
        //System.setProperty("webdriver.chrome.driver", "/usr/local/bin/chromedriver-mac-arm64");
    }
    public static WebDriver getDrive(){
        
        WebDriverManager.chromiumdriver().setup();
        options.addArguments("--headless");
        return new ChromeDriver(options);
    }

    
}
