using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Thuyet_Trinh.Models;
using Thuyet_Trinh.Data;

namespace Thuyet_Trinh.Controllers
{
    public class HomeController : Controller
    {
        private readonly ApplicationDbContext _context;

        public HomeController(ApplicationDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            return RedirectToAction("Index", "Weather");
        }
    }
}
