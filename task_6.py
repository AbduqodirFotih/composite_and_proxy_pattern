import time
from abc import ABC, abstractmethod

class WeatherData:
    def __init__(self, city: str, condition: str, temperature: float):
        self.city = city
        self.condition = condition
        self.temperature = temperature

    def __str__(self) -> str:
        return f"{self.city}: {self.condition}, {self.temperature} C"

class WeatherService(ABC):
    @abstractmethod
    def get_weather(self, city: str) -> WeatherData:
        pass

class RealWeatherService(WeatherService):
    def get_weather(self, city: str) -> WeatherData:
        time.sleep(1.0)
        return WeatherData(city, "Ochiq havo", 22.5)

class CachingWeatherProxy(WeatherService):
    def __init__(self, real_service: WeatherService, expiration_seconds: float = 300.0):
        self._real_service = real_service
        self._cache = {}
        self._timestamps = {}
        self._expiration_seconds = expiration_seconds

    def get_weather(self, city: str) -> WeatherData:
        now = time.time()
        if city in self._cache:
            cached_time = self._timestamps.get(city, 0)
            if now - cached_time < self._expiration_seconds:
                print(f"Keshdan olindi: {city}")
                return self._cache[city]

        print(f"Ob-havo markazidan yuklanmoqda: {city}...")
        fresh_data = self._real_service.get_weather(city)
        self._cache[city] = fresh_data
        self._timestamps[city] = now
        return fresh_data

    def clear_cache(self) -> None:
        self._cache.clear()
        self._timestamps.clear()
        print("Kesh tozalandi.")

if __name__ == "__main__":
    service = CachingWeatherProxy(RealWeatherService(), expiration_seconds=300.0)

    data1 = service.get_weather("Toshkent")
    print(data1)

    data2 = service.get_weather("Toshkent")
    print(data2)

    service.clear_cache()

    data3 = service.get_weather("Toshkent")
    print(data3)
