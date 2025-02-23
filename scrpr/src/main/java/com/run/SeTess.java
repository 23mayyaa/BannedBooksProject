package com.run;

import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import java.util.List;

public class SeTess {
    private static SeTess instance;  // Singleton instance
    private static WebDriver driver;
    private JavascriptExecutor executor;
    private static final int TIMEOUT_SECONDS = 1;
    private String descriptionXPath = "html/body/div[1]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[4]/div/div[1]/div/div/span";
    private String altDescriptionXPath = "/html/body/div[1]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[5]/div/div[1]/div/div/span";

    // Private constructor to prevent external instantiation
    private SeTess() {
        AppConfig.init();
        driver = AppConfig.getDrive();
        driver.get("https://www.goodreads.com/");
        executor = (JavascriptExecutor) driver;
    }

    // Public method to get the single instance of SeTess
    public static SeTess getInstance() {
        if (instance == null) {
            synchronized (SeTess.class) { // Thread safety
                if (instance == null) {
                    instance = new SeTess();
                }
            }
        }
        return instance;
    }

    public String scrape(String searchQuery, String[] ref) {
        try {
            // Go to Bing with the search query including site:goodreads.com
            driver.get("https://www.bing.com/search?q=" + searchQuery + " site:goodreads.com");

            // Wait for search results to load
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(TIMEOUT_SECONDS));

            // Find all search results
            List<WebElement> results = wait.until(ExpectedConditions.presenceOfAllElementsLocatedBy(
                By.cssSelector("h2 a")
            ));

            // Find and click the first Goodreads link
            WebElement result = results.get(0);
            String href = result.getAttribute("href");

            if (href != null && href.contains("goodreads.com")) {
                driver.get(href); // Navigate directly to the URL

                // Extract description
                String description = getDescriptionIfExists(descriptionXPath);
                if (description.isEmpty()) {
                    description = getDescriptionIfExists(altDescriptionXPath);
                }

                // Extract genres
                List<WebElement> genreElements = driver.findElements(By.cssSelector("span.BookPageMetadataSection__genreButton span.Button__labelItem"));
                StringBuilder genre = new StringBuilder();
                for (int i = 0; i < genreElements.size(); i++) {
                    genre.append(genreElements.get(i).getText());
                    if (i != genreElements.size() - 1) {
                        genre.append(", ");
                    }
                }

                ref[3] = genre.toString();
                if (!description.isEmpty()) {
                    ref[2] = description.replace("\n", " ");
                    System.out.print(ref[2]);
                    return "found";
                }
            }
        } catch (TimeoutException e) {
            //e.printStackTrace();
        } catch (Exception e) {
            //e.printStackTrace();
        }
        return null;
    }

    // Helper method to get description text if element exists
    private String getDescriptionIfExists(String xpath) {
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(TIMEOUT_SECONDS));
            WebElement element = wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath(xpath)));
            return element.getText();
        } catch (TimeoutException e) {
            return ""; // Return empty string if not found
        }
    }
}
