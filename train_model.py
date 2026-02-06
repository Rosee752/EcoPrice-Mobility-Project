import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle  # This helps us "save" the trained brain to use later


def train_robot_brain():
    print("🧠 The Robot is reading the diary to learn patterns...")

    # 1. Load the data
    df = pd.read_csv("frankfurt_bikes.csv")

    # 🛑 REALITY CHECK:
    # Since we only have a few rows of data right now, the robot can't really learn much.
    # But this is EXACTLY how the code would look if you had 1,000,000 rows.

    # 2. Prepare the data (Feature Engineering)
    # We turn "Timestamp" into numbers the robot understands
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour

    # We want to predict 'free_bikes' (Target)
    # We use 'latitude', 'longitude', 'hour', and 'empty_slots' as clues (Features)
    X = df[['latitude', 'longitude', 'hour']]
    y = df['free_bikes']

    # 3. Split data (Study material vs Exam material)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # 4. Train the Brain (The Random Forest)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    print("💪 Training complete!")

    # 5. Test the Brain
    score = model.score(X_test, y_test)
    print(f"🎓 Robot Report Card (Accuracy): {score}")

    # 6. Save the Brain to a file
    with open("bike_predictor.pkl", "wb") as f:
        pickle.dump(model, f)
    print("💾 I saved the trained brain to 'bike_predictor.pkl'")


if __name__ == "__main__":
    train_robot_brain()