import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score


df = pd.read_csv("../data/sleep.csv")

df.columns = df.columns.str.replace(" ", "_")

df = df.drop("Person_ID", axis=1)

df = df.drop_duplicates()

df[["BP_sys","BP_dia"]] = df["Blood_Pressure"].str.split("/", expand=True)

df["BP_sys"] = df["BP_sys"].astype(int)
df["BP_dia"] = df["BP_dia"].astype(int)

df = df.drop("Blood_Pressure", axis=1)

y = df["Quality_of_Sleep"]
X = df.drop(["Quality_of_Sleep", "Sleep_Disorder"], axis=1)

cat_cols = X.select_dtypes(include="object").columns
num_cols = X.select_dtypes(exclude="object").columns

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("num", "passthrough", num_cols)
])

models = {
    "linear": LinearRegression(),
    "rf": RandomForestRegressor(n_estimators=200),
    "gb": GradientBoostingRegressor()
}

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

best_pipeline = None
best_score = -1

for name, model in models.items():

    pipe = Pipeline([
        ("prep", preprocessor),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)

    pred = pipe.predict(X_test)

    score = r2_score(y_test, pred)

    print(name, score)

    if score > best_score:
        best_score = score
        best_pipeline = pipe

joblib.dump(best_pipeline, "../model/pipeline.pkl")

print("Best R2:", best_score)