using System.Text.Json;
using Thuyet_Trinh.Models;

namespace Thuyet_Trinh.Services;

public interface IWeatherService
{
    Task<WeatherData> GetWeatherByCityAsync(string city);
}

public class WeatherService : IWeatherService
{
    private readonly HttpClient _httpClient;
    private readonly string _apiKey;
    private readonly string _baseUrl;

    public WeatherService(HttpClient httpClient, IConfiguration configuration)
    {
        _httpClient = httpClient;
        var weatherConfig = configuration.GetSection("WeatherApi");
        _apiKey = weatherConfig["ApiKey"];
        _baseUrl = weatherConfig["BaseUrl"];
    }

    public async Task<WeatherData> GetWeatherByCityAsync(string city)
    {
        try
        {
            string url = $"{_baseUrl}/weather?q={city}&appid={_apiKey}&units=metric";
            var response = await _httpClient.GetAsync(url);

            if (!response.IsSuccessStatusCode)
            {
                return null;
            }

            var content = await response.Content.ReadAsStringAsync();
            var json = JsonSerializer.Deserialize<JsonElement>(content);

            var weatherData = new WeatherData
            {
                City = json.GetProperty("name").GetString(),
                Country = json.GetProperty("sys").GetProperty("country").GetString(),
                Temperature = json.GetProperty("main").GetProperty("temp").GetDouble(),
                FeelsLike = json.GetProperty("main").GetProperty("feels_like").GetDouble(),
                TempMin = json.GetProperty("main").GetProperty("temp_min").GetDouble(),
                TempMax = json.GetProperty("main").GetProperty("temp_max").GetDouble(),
                Humidity = json.GetProperty("main").GetProperty("humidity").GetInt32(),
                Pressure = json.GetProperty("main").GetProperty("pressure").GetInt32(),
                Description = json.GetProperty("weather")[0].GetProperty("description").GetString(),
                Icon = json.GetProperty("weather")[0].GetProperty("icon").GetString(),
                WindSpeed = json.GetProperty("wind").GetProperty("speed").GetDouble(),
                Visibility = json.GetProperty("visibility").GetDouble() / 1000, // Convert to km
                Cloudiness = json.GetProperty("clouds").GetProperty("all").GetInt32(),
                SearchQuery = city
            };

            return weatherData;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error fetching weather: {ex.Message}");
            return null;
        }
    }
}
