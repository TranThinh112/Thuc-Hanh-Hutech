using Thuyet_Trinh.Models;

namespace Thuyet_Trinh.Services
{
    public interface IWeatherService
    {
        Task<WeatherViewModel?> GetCurrentWeatherAsync(string city);
    }
}
