import osmnx as ox
import geocoder

def get_current_location():
    # Use geocoder to fetch the current location based on IP
    g = geocoder.ip('me')  # You can also use GPS-based methods in certain environments
    if g.ok:
        return {"lat": g.latlng[0], "lng": g.latlng[1]}
    else:
        print("Error: Could not determine current location.")
        return None

def find_nearby_restaurants(location, radius, dietary_restrictions):
    # Step 1: Get points of interest (POIs) for restaurants from OpenStreetMap
    tags = {"amenity": "restaurant"}
    restaurants = ox.features_from_point((location['lat'], location['lng']), tags=tags, dist=radius)
    
    filtered_restaurants = []
    
    for index, restaurant in restaurants.iterrows():
        name = restaurant.get('name', 'Unnamed Restaurant')
        # Step 2: Filter based on dietary restrictions using keywords in the restaurant's name
        if any(keyword.lower() in name.lower() for keyword in dietary_restrictions):
            filtered_restaurants.append(name)
    
    return filtered_restaurants

# Example usage
if __name__ == "__main__":
    user_location = get_current_location()
    if user_location:
        print("Current Location:", user_location)
        search_radius = 1000  # in meters (1 km)
        user_dietary_restrictions = ["vegan", "vegetarian", "gluten-free"]

        results = find_nearby_restaurants(user_location, search_radius, user_dietary_restrictions)
        print("Filtered Restaurants:", results)
