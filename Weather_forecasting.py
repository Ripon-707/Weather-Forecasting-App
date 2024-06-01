import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtGui import QFont

def get_weather_forecast(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Assuming you want temperature in Celsius
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Extract forecast data
        forecast = data["list"]
        return forecast
    else:
        error_message = data.get("message", "City not found or an error occurred.")
        QMessageBox.critical(None, "Error", error_message)
        return None

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather Forecast")
        self.setGeometry(100, 100, 500, 500)

        layout = QVBoxLayout()

        # City input
        self.city_label = QLabel("Enter city name:")
        self.city_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.city_label)

        self.city_input = QLineEdit()
        self.city_input.setFont(QFont("Arial", 14))
        layout.addWidget(self.city_input)

        # Forecast button
        self.forecast_button = QPushButton("Get Forecast")
        self.forecast_button.setFont(QFont("Arial", 14))
        self.forecast_button.clicked.connect(self.show_forecast)
        layout.addWidget(self.forecast_button)

        # Forecast display
        self.forecast_display = QTextEdit()
        self.forecast_display.setFont(QFont("Arial", 12))
        self.forecast_display.setReadOnly(True)
        layout.addWidget(self.forecast_display)

        self.setLayout(layout)

    def show_forecast(self):
        city_name = self.city_input.text()
        api_key = "0b8bb1f54898497e386c73d9e8a482a1"  # Replace with your OpenWeatherMap API key
        forecast = get_weather_forecast(city_name, api_key)
        
        if forecast:
            forecast_text = ""
            for day in forecast:
                date = day["dt_txt"][:10]
                temperature = day["main"]["temp"]
                weather_description = day["weather"][0]["description"]
                forecast_text += f"Date: {date}, Temperature: {temperature}°C, Description: {weather_description}\n"
            
            self.forecast_display.setPlainText(forecast_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())
