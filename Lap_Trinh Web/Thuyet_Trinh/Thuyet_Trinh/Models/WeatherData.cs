namespace Thuyet_Trinh.Models;

public class WeatherData
{
    public string City { get; set; }
    public string Country { get; set; }
    public double Temperature { get; set; }
    public double FeelsLike { get; set; }
    public double TempMin { get; set; }
    public double TempMax { get; set; }
    public int Humidity { get; set; }
    public int Pressure { get; set; }
    public string Description { get; set; }
    public string Icon { get; set; }
    public double WindSpeed { get; set; }
    public double Visibility { get; set; }
    public int Cloudiness { get; set; }
    public string SearchQuery { get; set; }
}
