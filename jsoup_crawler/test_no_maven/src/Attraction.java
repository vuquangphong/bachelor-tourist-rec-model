import org.json.JSONObject;

public class Attraction {
    private String name;
    private String id;
    private String category;
    private double rating;
    private double price;
    private double latitude;
    private double longitude;

    public Attraction(String name, String id, String category, double rating, double price, double latitude, double longitude) {
        this.name = name;
        this.id = id;
        this.category = category;
        this.rating = rating;
        this.price = price;
        this.latitude = latitude;
        this.longitude = longitude;
    }

    public JSONObject toJSON() {
        JSONObject obj = new JSONObject();
        obj.put("name", this.name);
        obj.put("id", this.id);
        obj.put("category", this.category);
        obj.put("rating", this.rating);
        obj.put("price", this.price);
        obj.put("latitude", this.latitude);
        obj.put("longitude", this.longitude);
        return obj;
    }
}
