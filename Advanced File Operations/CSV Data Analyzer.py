import csv
import math

# Merge Sort implementation for performance sorting
def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] > right[j][1]:  # Sort descending by performance
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Read CSV and calculate performance
def analyze_csv(filename):
    performances = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    open_price = float(row['Open'])
                    close_price = float(row['Close'])
                    if open_price == 0:
                        continue  # Avoid division by zero
                    change_percent = ((close_price - open_price) / open_price) * 100
                    label = f"{row['Symbol']} ({row['Date']})"
                    performances.append((label, round(change_percent, 2)))
                except ValueError:
                    continue  # Skip invalid rows
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []

    return performances

# Statistical calculations using math module
def calculate_stats(values):
    n = len(values)
    if n == 0:
        return 0, 0, 0

    mean = sum(values) / n

    sorted_vals = sorted(values)
    if n % 2 == 0:
        median = (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
    else:
        median = sorted_vals[n//2]

    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = math.sqrt(variance)

    return round(mean, 2), round(median, 2), round(std_dev, 2)

# Main program
def main():
    filename = 'stock_data.csv'  # Replace with your CSV file
    data = analyze_csv(filename)

    if not data:
        return

    sorted_data = merge_sort(data)
    top_10 = sorted_data[:10]

    print("Top 10 Performing Stocks:")
    for i, (label, change) in enumerate(top_10, 1):
        print(f"{i}. {label}: {change:+.2f}%")

    all_changes = [change for _, change in data]
    mean, median, std_dev = calculate_stats(all_changes)

    print("\nStatistical Analysis:")
    print(f"Average daily performance: {mean:+.2f}%")
    print(f"Median performance: {median:+.2f}%")
    print(f"Standard deviation: {std_dev:.2f}%")

if __name__ == "__main__":
    main()
