using Microsoft.AspNetCore.Mvc;
using Thuyet_Trinh.Models;
using Thuyet_Trinh.Services;

namespace Thuyet_Trinh.Controllers
{
    public class WeatherController : Controller
    {
        private readonly IWeatherService _weather;

        private static readonly Dictionary<string, string> DefaultCities = new()
        {
            ["Ho Chi Minh City, VN"] = "Hồ Chí Minh",
            ["Hanoi, VN"] = "Hà Nội",
            ["Hue, VN"] = "Huế",
            ["Can Tho, VN"] = "Cần Thơ",
            ["Da Nang, VN"] = "Đà Nẵng"
        };

        private static readonly Dictionary<string, string> CityQueryAliases = new(StringComparer.OrdinalIgnoreCase)
        {
            ["Ho Chi Minh"] = "Ho Chi Minh City, VN",
            ["Hồ Chí Minh"] = "Ho Chi Minh City, VN",
            ["Ho Chi Minh City"] = "Ho Chi Minh City, VN",
            ["Hồ Chí Minh City"] = "Ho Chi Minh City, VN",
            ["HCMC"] = "Ho Chi Minh City, VN",
            ["Ha Noi"] = "Hanoi, VN",
            ["Hà Nội"] = "Hanoi, VN",
            ["Hanoi"] = "Hanoi, VN",
            ["Hue"] = "Hue, VN",
            ["Huế"] = "Hue, VN",
            ["Can Tho"] = "Can Tho, VN",
            ["Cần Thơ"] = "Can Tho, VN",
            ["Da Nang"] = "Da Nang, VN",
            ["Đà Nẵng"] = "Da Nang, VN",
            ["Hai Phong"] = "Hai Phong, VN",
            ["Hải Phòng"] = "Hai Phòng, VN"
        };

        private static readonly Dictionary<string, string> CityDisplayNames = new(StringComparer.OrdinalIgnoreCase)
        {
            ["Ho Chi Minh City, VN"] = "Hồ Chí Minh",
            ["Hanoi, VN"] = "Hà Nội",
            ["Hue, VN"] = "Huế",
            ["Can Tho, VN"] = "Cần Thơ",
            ["Da Nang, VN"] = "Đà Nẵng",
            ["Hai Phong, VN"] = "Hải Phòng"
        };

        public WeatherController(IWeatherService weather)
        {
            _weather = weather;
        }

        public async Task<IActionResult> Index()
        {
            var tasks = DefaultCities.Select(async kv =>
            {
                var weather = await _weather.GetCurrentWeatherAsync(kv.Key);
                if (weather == null) return null;
                weather.City = kv.Value;
                return weather;
            });

            var results = await Task.WhenAll(tasks);
            var viewModel = new WeatherIndexViewModel
            {
                Cities = results.Where(x => x != null).Select(x => x!).ToList()
            };

            return View(viewModel);
        }

        [HttpPost]
        public async Task<IActionResult> Search(string city)
        {
            if (string.IsNullOrWhiteSpace(city)) return BadRequest();

            var query = GetCityQuery(city.Trim());
            var model = await _weather.GetCurrentWeatherAsync(query);
            if (model == null) return NotFound();

            model.City = GetDisplayName(query) ?? GetDisplayName(city.Trim()) ?? model.City;
            return PartialView("_WeatherCard", model);
        }

        private static string GetCityQuery(string city)
        {
            if (CityQueryAliases.TryGetValue(city, out var query))
            {
                return query;
            }

            return city;
        }

        private static string? GetDisplayName(string city)
        {
            if (CityDisplayNames.TryGetValue(city, out var displayName))
            {
                return displayName;
            }

            return null;
        }
    }
}
