import math

# Store layout with coordinates
store = {
    "Entrance": (0, 0),
    "Produce": (2, 3),
    "Dairy": (5, 3),
    "Bakery": (8, 3),
    "Meat": (5, 6),
    "Cereal/Breakfast": (8, 6)
}

# Your shopping list
shopping_list = ["Apples", "Milk", "Bread", "Chicken", "Cereal", "Eggs"]

# Which section each item belongs to
items_in_sections = {
    "Produce": ["Apples"],
    "Dairy": ["Milk", "Eggs"],
    "Bakery": ["Bread"],
    "Meat": ["Chicken"],
    "Cereal/Breakfast": ["Cereal"]
}

# Step 1: Find which store sections are needed
needed_sections = []
for section in items_in_sections:
    for item in items_in_sections[section]:
        if item in shopping_list:
            needed_sections.append(section)
            break  # Add each section only once

# Step 2: Function to find distance between two points
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Step 3: Plan the route
current_place = "Entrance"
route = ["Entrance"]
total_distance = 0
visited = []

while len(visited) < len(needed_sections):
    shortest = None
    shortest_dist = 999999  # very big number

    for section in needed_sections:
        if section not in visited:
            d = distance(store[current_place], store[section])
            if d < shortest_dist:
                shortest_dist = d
                shortest = section

    visited.append(shortest)
    route.append(shortest)
    total_distance += shortest_dist
    current_place = shortest

# Step 4: Return to entrance
total_distance += distance(store[current_place], store["Entrance"])
route.append("Entrance")

# Step 5: Print final route
print("Optimized Route:")
for place in route:
    if place == "Entrance":
        print(f"{place} {store[place]}")
    else:
        # Show what to pick up in that section
        items = []
        for item in items_in_sections[place]:
            if item in shopping_list:
                items.append(item)
        print(f"Go to {place} {store[place]} - Pick up: {', '.join(items)}")

print("Total Distance:", round(total_distance, 1), "units")
