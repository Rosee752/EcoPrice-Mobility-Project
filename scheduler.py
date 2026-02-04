import time
from datetime import datetime
from fetch_data import append_data_to_csv  # We import the robot we made in Step 4


def start_scheduler():
    print("🕒 Scheduler started! I will run the robot every 30 minutes.")
    print("⚠️  Keep this window OPEN. Do not close it.")
    print("------------------------------------------------")

    # This loop runs forever until you stop it (Ctrl + C)
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"⏰ It is {current_time}. Waking up the robot...")

        # 1. Run the Fetching Robot
        try:
            append_data_to_csv()  # This adds real data to frankfurt_bikes.csv
        except Exception as e:
            print(f"❌ Something went wrong: {e}")

        print("💤 Robot is going back to sleep for 30 minutes...")
        print("------------------------------------------------")

        # 2. Sleep for 30 minutes (30 * 60 seconds)
        # You can change this to 10 seconds just to test it first!
        time.sleep(1800)


if __name__ == "__main__":
    start_scheduler()