using Microsoft.AspNetCore.Mvc;

public class WeatherController : Controller
{
    private readonly WeatherService _weatherService;

    public WeatherController(
        WeatherService weatherService)
    {
        _weatherService = weatherService;
    }
    [HttpGet]
    public IActionResult Index(){
        return View();
    }
    
    [HttpPost]

    public async Task<IActionResult> Index(String city)
    {
        if (string.IsNullOrWhiteSpace(city))
        {
            ViewBag.Error = "Vui lòng nhập tên thành phố";
            return View();
        }

        var weather = await _weatherService.GetWeatherAsync(city);

        if (weather == null)
        {
            ViewBag.Error = "Không tìm thấy thành phố";
            return View();
        }

        return View(weather);
    }
}