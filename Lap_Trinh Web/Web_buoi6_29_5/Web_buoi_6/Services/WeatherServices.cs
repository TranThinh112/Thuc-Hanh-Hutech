using System.Text.Json;
using Microsoft.Extensions.Options;
using System.Globalization;

public class WeatherService
{
    private readonly HttpClient _httpClient;
    private readonly WeatherApiSettings _settings;

    public WeatherService(
        HttpClient httpClient,
        IOptions<WeatherApiSettings> options)
    {
        _httpClient = httpClient;
        _settings = options.Value;
    }
    

    public async Task<WeatherDto?> GetWeatherAsync(string city)
    {

        var url =
            $"{_settings.BaseUrl}/weather" +
            $"?q={city}" +
            $"&appid={_settings.ApiKey}" +
            $"&units=metric" +
            $"&lang=vi";


        var response = await _httpClient.GetAsync(url);

        if (!response.IsSuccessStatusCode)
            return null;

        var json = await response.Content.ReadAsStringAsync();

        using JsonDocument doc = JsonDocument.Parse(json);

        
        var countryCode = doc.RootElement
                    .GetProperty("sys")
                    .GetProperty("country")
                    .GetString()!;

        var countryName =
            new RegionInfo(countryCode).EnglishName;

        return new WeatherDto
        {
            City = doc.RootElement.GetProperty("name").GetString()!,

            Country = countryName,

            Temperature = doc.RootElement
                .GetProperty("main")
                .GetProperty("temp")
                .GetDouble(),


            Humidity = doc.RootElement
                .GetProperty("main")
                .GetProperty("humidity")
                .GetInt32(),

            Description = doc.RootElement
                .GetProperty("weather")[0]
                .GetProperty("description")
                .GetString()!

           
        };
    }
}