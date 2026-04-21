import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Attack stages we want to classify
STAGES = ["reconnaissance", "initial_access", "enumeration", "lateral_movement"]

def generate_synthetic_data(n=1000):
    np.random.seed(42)
    data = []
    for _ in range(n):
        stage = np.random.choice(STAGES)
        if stage == "reconnaissance":
            # Nmap-like behavior: many ports, short sessions
            record = {
                "connection_count": np.random.randint(50, 200),
                "unique_ports": np.random.randint(20, 100),
                "avg_session_duration": np.random.uniform(0.1, 1.0),
                "failed_logins": 0,
                "commands_run": 0,
                "dst_port_22": np.random.randint(0, 5),
                "dst_port_80": np.random.randint(10, 50),
                "stage": stage
            }
        elif stage == "initial_access":
            # Hydra-like: hammering port 22 with many login attempts
            record = {
                "connection_count": np.random.randint(20, 100),
                "unique_ports": np.random.randint(1, 3),
                "avg_session_duration": np.random.uniform(0.5, 2.0),
                "failed_logins": np.random.randint(50, 300),
                "commands_run": 0,
                "dst_port_22": np.random.randint(50, 200),
                "dst_port_80": np.random.randint(0, 3),
                "stage": stage
            }
        elif stage == "enumeration":
            # Logged in, running commands to look around
            record = {
                "connection_count": np.random.randint(1, 5),
                "unique_ports": np.random.randint(1, 2),
                "avg_session_duration": np.random.uniform(30, 120),
                "failed_logins": np.random.randint(0, 3),
                "commands_run": np.random.randint(10, 50),
                "dst_port_22": np.random.randint(1, 5),
                "dst_port_80": 0,
                "stage": stage
            }
        elif stage == "lateral_movement":
            # Moving to other hosts
            record = {
                "connection_count": np.random.randint(5, 30),
                "unique_ports": np.random.randint(2, 10),
                "avg_session_duration": np.random.uniform(10, 60),
                "failed_logins": np.random.randint(0, 10),
                "commands_run": np.random.randint(5, 20),
                "dst_port_22": np.random.randint(5, 20),
                "dst_port_80": np.random.randint(0, 5),
                "stage": stage
            }
        data.append(record)
    return pd.DataFrame(data)

def train_model():
    df = generate_synthetic_data(1000)
    X = df.drop("stage", axis=1)
    y = df["stage"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print(classification_report(y_test, model.predict(X_test)))
    joblib.dump(model, "classifier/model.pkl")
    print("Model saved to classifier/model.pkl")

if __name__ == "__main__":
    train_model()
