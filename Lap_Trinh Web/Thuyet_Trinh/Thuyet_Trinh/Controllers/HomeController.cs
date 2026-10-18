using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Thuyet_Trinh.Models;
using Thuyet_Trinh.Services;

namespace Thuyet_Trinh.Controllers;

public class HomeController : Controller
{
    private readonly IWeatherService _weatherService;

    public HomeController(IWeatherService weatherService)
    {
        _weatherService = weatherService;
    }

    public async Task<IActionResult> Index(string city = "Hanoi")
    {
        var weatherData = await _weatherService.GetWeatherByCityAsync(city);
        return View(weatherData);
    }

    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}
