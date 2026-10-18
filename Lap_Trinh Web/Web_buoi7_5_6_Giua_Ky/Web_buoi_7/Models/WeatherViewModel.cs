namespace Thuyet_Trinh.Models
{
    public class WeatherViewModel
    {
        public string City { get; set; } = string.Empty;
        public string Country { get; set; } = string.Empty;
        public double Temperature { get; set; }
        public string Condition { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string ImageUrl { get; set; } = string.Empty;
        public bool IsFavorite { get; set; } = false;
    }
}
