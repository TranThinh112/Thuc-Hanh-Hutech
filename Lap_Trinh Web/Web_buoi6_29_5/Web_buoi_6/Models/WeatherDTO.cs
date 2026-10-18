public class WeatherDto
{
    public string City { get; set; } = string.Empty;
    public string Country { get; set; } = string.Empty;

    public double Temperature { get; set; }

    public int Humidity { get; set; }

    public string Description { get; set; } = string.Empty;
}