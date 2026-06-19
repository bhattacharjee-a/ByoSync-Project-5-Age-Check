import os
import requests
import csv
from datetime import datetime

# Change if your API uses a different endpoint
API_URL = "http://localhost:8000/check_age"

# Folder containing test images
TEST_FOLDER = "test_images"

# Output report
REPORT_FILE = "test_results.csv"

results = []

print("Starting API Tests...\n")

for filename in os.listdir(TEST_FOLDER):

    image_path = os.path.join(TEST_FOLDER, filename)

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    try:
        with open(image_path, "rb") as file:

            response = requests.post(
                API_URL,
                files={"file": file}
            )

        if response.status_code == 200:
            result = response.json()

            print(f"✓ {filename}")
            print(result)

            results.append([
                filename,
                response.status_code,
                str(result)
            ])

        else:
            print(f"✗ {filename}")
            print("Status:", response.status_code)

            results.append([
                filename,
                response.status_code,
                "API Error"
            ])

    except Exception as e:

        print(f"✗ {filename}")
        print("Exception:", e)

        results.append([
            filename,
            "FAILED",
            str(e)
        ])

with open(REPORT_FILE, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Image",
        "Status",
        "Response"
    ])

    writer.writerows(results)

print("\nTesting Complete!")
print(f"Report saved to {REPORT_FILE}")
