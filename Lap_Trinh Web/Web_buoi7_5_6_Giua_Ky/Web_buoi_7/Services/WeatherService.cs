using System.Text.Json;
using Thuyet_Trinh.Models;

namespace Thuyet_Trinh.Services
{
    public class WeatherService : IWeatherService
    {
        private readonly HttpClient _http;
        private readonly IConfiguration _config;
        private readonly string _apiKey;
        private readonly string _baseUrl;

        private static readonly Dictionary<string, string> CityImageQueries = new(StringComparer.OrdinalIgnoreCase)
        {
            ["Ho Chi Minh City, VN"] = "ho chi minh city vietnam",
            ["Hanoi, VN"] = "hanoi vietnam",
            ["Hue, VN"] = "hue vietnam",
            ["Can Tho, VN"] = "can tho vietnam",
            ["Da Nang, VN"] = "da nang vietnam",
            ["Hai Phong, VN"] = "hai phong vietnam",
            ["Ho Chi Minh City"] = "ho chi minh city vietnam",
            ["Hanoi"] = "hanoi vietnam",
            ["Hue"] = "hue vietnam",
            ["Can Tho"] = "can tho vietnam",
            ["Da Nang"] = "da nang vietnam",
            ["Hai Phong"] = "hai phong vietnam"
        };

        public WeatherService(HttpClient http, IConfiguration config)
        {
            _http = http;
            _config = config;
            _apiKey = _config["WeatherApi:ApiKey"] ?? string.Empty;
            _baseUrl = _config["WeatherApi:BaseUrl"]?.TrimEnd('/') ?? "https://api.openweathermap.org/data/2.5";
        }

        public async Task<WeatherViewModel?> GetCurrentWeatherAsync(string city)
        {
            if (string.IsNullOrWhiteSpace(city)) return null;

            var url = $"{_baseUrl}/weather?q={Uri.EscapeDataString(city)}&appid={_apiKey}&units=metric";
            var res = await _http.GetAsync(url);
            if (!res.IsSuccessStatusCode) return null;
            using var stream = await res.Content.ReadAsStreamAsync();
            var doc = await JsonSerializer.DeserializeAsync<JsonElement>(stream);

            var model = new WeatherViewModel
            {
                City = doc.GetProperty("name").GetString() ?? city,
                Country = doc.GetProperty("sys").GetProperty("country").GetString() ?? string.Empty,
                Temperature = doc.GetProperty("main").GetProperty("temp").GetDouble(),
                Condition = doc.GetProperty("weather")[0].GetProperty("main").GetString() ?? string.Empty,
                Description = doc.GetProperty("weather")[0].GetProperty("description").GetString() ?? string.Empty,
                ImageUrl = GetCityImageUrl(city)
            };

            return model;
        }

        private static string GetCityImageUrl(string city)
        {
            var normalizedCity = city.Trim();
            if (CityImageQueries.TryGetValue(normalizedCity, out var queryText))
            {
                normalizedCity = queryText;
            }

            if (normalizedCity.Contains(','))
            {
                normalizedCity = normalizedCity.Split(',')[0];
            }

            var query = Uri.EscapeDataString(normalizedCity + " vietnam city");
            return $"https://source.unsplash.com/featured/900x600/?{query}";
        }
    }
}
