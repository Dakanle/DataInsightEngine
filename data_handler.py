import pandas as pd
import numpy as np


class OilDataHandler:
    def __init__(self, filename):
        self.filename = filename
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.filename)
        return self.df

    def clean_data(self):
        df = self.df.copy()
        #change all the column names to make it more readable for me
        df.columns = [col.strip().lower().replace(" ", "_").replace("#", "num").replace("(", "").replace(")", "") for col in df.columns]
        #change the dates from str to date time
        df["service_start_date"] = pd.to_datetime(df["service_start_date"], errors="coerce")
        df["service_end_date"] = pd.to_datetime(df["service_end_date"], errors="coerce")
        #change from str to int
        df["current_charges"] = pd.to_numeric(df["current_charges"], errors="coerce")
        df["consumption_gal"] = pd.to_numeric(df["consumption_gal"], errors="coerce")
        df["num_days"] = pd.to_numeric(df["num_days"], errors="coerce")
        #drop all Nan
        df = df.dropna(subset=["service_start_date", "service_end_date", "current_charges", "consumption_gal"])
        #change these to more readable for groupby
        df["borough"] = df["borough"].str.title()
        df["development_name"] = df["development_name"].str.title()
        df["estimated"] = df["estimated"].astype(str).str.upper().str.strip()
        #adds new columns to break down the date and get season
        # it is basically to help my groupby  
        df["year"] = df["service_end_date"].dt.year
        df["month"] = df["service_end_date"].dt.month
        df["month_name"] = df["service_end_date"].dt.month_name()
        df["season"] = df["month"].apply(self.get_season)
        #add a charge per gallon column
        df["charge_per_gallon"] = np.where(
            df["consumption_gal"] > 0,
            df["current_charges"] / df["consumption_gal"],
            np.nan
        )
        #add a consumption by day column
        df["consumption_per_day"] = np.where(
            df["num_days"] > 0,
            df["consumption_gal"] / df["num_days"],
            np.nan
        )

        self.df = df
        return self.df
    #returns me the season
    def get_season(self, month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        return "Fall"

    def get_monthly_summary(self):
        monthly = self.df.groupby(["year", "month"], as_index=False).agg({
            "consumption_gal": "sum",
            "current_charges": "sum",
            "num_days": "mean"
        })
        monthly["charge_per_gallon"] = np.where(
            monthly["consumption_gal"] > 0,
            monthly["current_charges"] / monthly["consumption_gal"],
            np.nan
        )
        monthly["consumption_per_day"] = np.where(
            monthly["num_days"] > 0,
            monthly["consumption_gal"] / monthly["num_days"],
            np.nan
        )
        monthly["month_start"] = pd.to_datetime(
            monthly["year"].astype(str) + "-" + monthly["month"].astype(str) + "-01"
        )

        return monthly

class WeatherDataHandler:
    def __init__(self, filename_1, filename_2):
        self.filename_1 = filename_1
        self.filename_2 = filename_2
        self.weather_1 = None
        self.weather_2 = None
        self.combined_weather = None

    def load_data(self):
        self.weather_1 = pd.read_csv(self.filename_1)
        self.weather_2 = pd.read_csv(self.filename_2)
        return self.weather_1, self.weather_2

    def clean_open_meteo(self):
        df = self.weather_1.copy()
        df["time"] = pd.to_datetime(df["time"], errors="coerce")

        rename_dict = {
            "temperature_2m (°C)": "temperature_c",
            "precipitation (mm)": "precipitation_mm",
            "rain (mm)": "rain_mm",
            "wind_speed_10m (km/h)": "wind_speed_kmh",
            "cloud_cover (%)": "cloud_cover_pct"
        }
        df = df.rename(columns=rename_dict)

        keep_col = ["time", "temperature_c", "precipitation_mm", "rain_mm", "wind_speed_kmh", "cloud_cover_pct"]
        df = df[keep_col]
        df["source"] = "open_meteo"

        self.weather_1 = df
        return self.weather_1

    def clean_nyc_weather(self):
        df = self.weather_2.copy()
        df["time"] = pd.to_datetime(df["time"], errors="coerce")

        rename_dict = {
            "temperature_2m (°C)": "temperature_c",
            "precipitation (mm)": "precipitation_mm",
            "rain (mm)": "rain_mm",
            "windspeed_10m (km/h)": "wind_speed_kmh",
            "cloudcover (%)": "cloud_cover_pct"
        }
        df = df.rename(columns=rename_dict)

        keep_cols = ["time", "temperature_c", "precipitation_mm", "rain_mm", "wind_speed_kmh", "cloud_cover_pct"]
        df = df[keep_cols]
        df["source"] = "nyc_weather"

        self.weather_2 = df
        return self.weather_2

    def combine_weather_data(self):
        combined = pd.concat([self.weather_1, self.weather_2], ignore_index=True)
        combined = combined.sort_values("time").drop_duplicates(subset=["time"])
        combined["year"] = combined["time"].dt.year
        combined["month"] = combined["time"].dt.month

        return combined

    def get_monthly_weather_summary(self):
        monthly = self.combined_weather.groupby(["year", "month"], as_index=False).agg({
            "temperature_c": "mean",
            "precipitation_mm": "sum",
            "rain_mm": "sum",
            "wind_speed_kmh": "mean",
            "cloud_cover_pct": "mean"
        })

        monthly["month_start"] = pd.to_datetime(
            monthly["year"].astype(str) + "-" + monthly["month"].astype(str) + "-01"
        )
        monthly["season"] = monthly["month"].apply(self.get_season)
        

        return monthly

    def get_season(self, month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        return "Fall"