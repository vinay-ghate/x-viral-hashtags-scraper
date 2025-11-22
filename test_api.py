import requests
import time
import subprocess
import sys

def test_api():
    # Start the server in a subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Starting server...")
    time.sleep(5)  # Wait for server to start

    try:
        # Test India
        print("\nTesting /trends/india...")
        response = requests.get("http://localhost:8000/trends/india")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Found {len(data['trends'])} trends for {data['country']}")
            print("Top 3 trends:")
            for trend in data['trends'][:3]:
                print(f"- {trend['rank']}: {trend['text']}")
        else:
            print(f"Failed: {response.status_code} - {response.text}")

        # Test United States (to verify dynamic country)
        print("\nTesting /trends/united-states...")
        response = requests.get("http://localhost:8000/trends/united-states")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Found {len(data['trends'])} trends for {data['country']}")
        else:
            print(f"Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\nStopping server...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_api()
