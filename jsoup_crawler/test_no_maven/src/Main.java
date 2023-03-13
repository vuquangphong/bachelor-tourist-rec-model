import org.jsoup.*;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.json.*;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class Main {
    private static final String URL = "https://www.tripadvisor.com.vn/Attraction_Review-g293924-d311083-Reviews-Temple_of_Literature_National_University-Hanoi.html";

    public static void main(String[] args) {
        try {
            Document doc = Jsoup.connect(URL).get();

            System.out.println(doc);

//            Elements attractionElements = doc.select("div.NcGPW");
//
//            List<Attraction> attractions = new ArrayList<>();
//            JSONArray attractionJSONs = new JSONArray();
//
//            for (Element attractionElement : attractionElements) {
//                String id = UUID.randomUUID().toString();
//                String name = attractionElement.getElementsByClass("keSJi FGwzt ukgoS").size() > 0 ? attractionElement.getElementsByClass("keSJi FGwzt ukgoS").first().text() : null;
//                String category = attractionElement.getElementsByClass("biGQs _P pZUbB hmDzD").size() > 0 ? attractionElement.getElementsByClass("biGQs _P pZUbB hmDzD").first().text() : null;
//                double rating = Double.parseDouble(attractionElement.getElementsByClass("jVDab o W f u w JqMhy").size() > 0 ? attractionElement.getElementsByClass("jVDab o W f u w JqMhy").first().attr("aria-label").replaceAll("[^0-9.]", "").substring(0, 2) : null);
//                double price = 0.0; // if price not available
////                Element locationElement = attractionElement.siblingElements().select("div.listing_info div.location").first();
////                String[] coordinates = locationElement.select("a").first().attr("data-coords").split(",");
//                double latitude = 0.0;
//                double longitude = 0.0;
//
//                Attraction attraction = new Attraction(name, id, category, rating, price, latitude, longitude);
//                attractions.add(attraction);
//            }
//
//            // convert attraction objects to JSON
//            for (Attraction attraction : attractions) {
//                attractionJSONs.put(attraction.toJSON());
//            }
//
//            System.out.println(attractionJSONs.get(0));
//
//            // save attractions data to a JSON file
//            String filePath = "../data_container/test_crawler_data.json";
//            FileWriter file = new FileWriter(filePath);
//            file.write(attractionJSONs.toString());
//            file.close();
//
//            System.out.println("Data save to ../data_container/test_crawler_data.json");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}