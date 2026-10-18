using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Web_buoi_6.Models;

namespace Web_buoi_6.Controllers;

public class HomeController : Controller
{
    public IActionResult Index()
    {
        return Redirect("/Identity/Account/Login");
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
