import pandas as pd

class ProjectAnalyzer:
    def __init__(self, oil_monthly_df, weather_monthly_df, oil_clean_df):
        self.oil_monthly_df = oil_monthly_df
        self.weather_monthly_df = weather_monthly_df
        self.oil_clean_df = oil_clean_df
        self.merged_df = None

    def merge_datasets(self):
        merged = pd.merge(
            self.oil_monthly_df,
            self.weather_monthly_df,
            on=["year", "month", "month_start"],
            how="inner"
        )

        merged["season"] = merged["month"].apply(self.get_season)
        self.merged_df = merged
        return self.merged_df

    def summary_statistics(self):
        return self.merged_df[[
            "consumption_gal",
            "current_charges",
            "temperature_c",
            "precipitation_mm",
            "wind_speed_kmh",
            "charge_per_gallon",
            "consumption_per_day",
            
        ]].describe()

    def yearly_summary(self):
        return self.merged_df.groupby("year", as_index=False).agg({
            "consumption_gal": "sum",
            "current_charges": "sum",
            "temperature_c": "mean",
            "precipitation_mm": "sum"
        })

    def seasonal_summary(self):
        return self.merged_df.groupby("season", as_index=False).agg({
            "consumption_gal": "mean",
            "current_charges": "mean",
            "temperature_c": "mean",
            
        })

    def correlation_matrix(self):
        return self.merged_df[[
            "consumption_gal",
            "current_charges",
            "temperature_c",
            "precipitation_mm",
            "wind_speed_kmh",
            "charge_per_gallon",
            "consumption_per_day",
            
        ]].corr()

    def borough_summary(self):
        return self.oil_clean_df.groupby("borough", as_index=False).agg({
            "consumption_gal": "mean",
            "current_charges": "mean"
        })

    def estimated_bill_summary(self):
        return self.oil_clean_df.groupby("estimated", as_index=False).agg({
            "consumption_gal": "mean",
            "current_charges": "mean"
        })

    def top_consumption_months(self, n=10):
        return self.merged_df.nlargest(n, "consumption_gal")[[
            "year", "month", "consumption_gal", "current_charges", "temperature_c"
        ]]

    def get_season(self, month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        return "Fall"
