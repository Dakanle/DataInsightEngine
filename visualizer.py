
import matplotlib.pyplot as plt


class ProjectVisualizer:
    def __init__(self, merged_df, borough_df):
        self.merged_df = merged_df
        self.borough_df = borough_df

    def line_plot_consumption_over_time(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.merged_df["month_start"], self.merged_df["consumption_gal"])
        plt.title("Monthly Heating Oil Consumption Over Time")
        plt.xlabel("Month")
        plt.ylabel("Consumption (GAL)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def line_plot_temperature_over_time(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.merged_df["month_start"], self.merged_df["temperature_c"])
        plt.title("Monthly Average Temperature Over Time")
        plt.xlabel("Month")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def scatter_temp_vs_consumption(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.merged_df["temperature_c"], self.merged_df["consumption_gal"], edgecolor="black")
        plt.title("Temperature vs Heating Oil Consumption")
        plt.xlabel("Average Temperature (°C)")
        plt.ylabel("Consumption (GAL)")
        plt.tight_layout()
        plt.show()

    def scatter_temp_vs_charges(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.merged_df["temperature_c"], self.merged_df["current_charges"], edgecolor="black")
        plt.title("Temperature vs Current Charges")
        plt.xlabel("Average Temperature (°C)")
        plt.ylabel("Current Charges")
        plt.tight_layout()
        plt.show()

    def bar_chart_borough_consumption(self):
        plt.figure(figsize=(10, 6))
        plt.bar(self.borough_df["borough"], self.borough_df["consumption_gal"])
        plt.title("Average Heating Oil Consumption by Borough")
        plt.xlabel("Borough")
        plt.ylabel("Average Consumption (GAL)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def histogram_consumption(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.merged_df["consumption_gal"], bins=20, edgecolor="black")
        plt.title("Distribution of Monthly Heating Oil Consumption")
        plt.xlabel("Consumption (GAL)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    def histogram_charges(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.merged_df["current_charges"], bins=20, edgecolor="black")
        plt.title("Distribution of Monthly Current Charges")
        plt.xlabel("Current Charges")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()
