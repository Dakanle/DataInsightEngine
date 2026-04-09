import pandas as pd
from data_handler import OilDataHandler, WeatherDataHandler
from analyzer import ProjectAnalyzer
from visualizer import ProjectVisualizer


oil_handler = OilDataHandler("heating-oil-consumption-and-cost-2010-feb-2022-1.csv")
oil_handler.load_data()
oil_clean = oil_handler.clean_data()

weather_handler = WeatherDataHandler("open-meteo-40.74N74.04W32m.csv", "NYC_Weather_2016_2022.csv")
weather_handler.load_data()
weather_handler.clean_open_meteo()
weather_handler.clean_nyc_weather()
weather_handler.combine_weather_data()

oil_monthly = oil_handler.get_monthly_summary()
weather_monthly = weather_handler.get_monthly_weather_summary()

analyzer = ProjectAnalyzer(oil_monthly, weather_monthly, oil_clean)
merged = analyzer.merge_datasets()

print("Oil Data:")
print(oil_clean.head())
print()

print("Combined Weather Data:")
print(weather_handler.combined_weather.head())
print()

print("Merged Monthly Data:")
print(merged.head())
print()

print("Summary Statistics:")
print(analyzer.summary_statistics())
print()

print("Yearly Summary:")
print(analyzer.yearly_summary())
print()

print("Seasonal Summary:")
print(analyzer.seasonal_summary())
print()

print("Borough Summary:")
borough_summary = analyzer.borough_summary()
print(borough_summary)
print()

print("Estimated vs Non-Estimated Summary:")
print(analyzer.estimated_bill_summary())
print()

print("Top 10 Highest Consumption Months:")
print(analyzer.top_consumption_months())
print()

print("Correlation Matrix:")
print(analyzer.correlation_matrix())
print()

merged.to_csv("merged_monthly_data.csv", index=False)
analyzer.yearly_summary().to_csv("yearly_summary.csv", index=False)
analyzer.seasonal_summary().to_csv("seasonal_summary.csv", index=False)
borough_summary.to_csv("borough_summary.csv", index=False)

visualizer = ProjectVisualizer(merged, borough_summary)
visualizer.line_plot_consumption_over_time()
visualizer.line_plot_temperature_over_time()
visualizer.scatter_temp_vs_consumption()
visualizer.scatter_temp_vs_charges()
visualizer.bar_chart_borough_consumption()
visualizer.histogram_consumption()
visualizer.histogram_charges()
