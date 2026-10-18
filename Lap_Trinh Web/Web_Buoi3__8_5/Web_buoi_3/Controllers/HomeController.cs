using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using WebTestBuoi3.Models;

namespace WebTestBuoi3.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult BaiTap2()
        {
            var danhsachsanPham = new List<SanPhamViewModel>
            {
                new SanPhamViewModel
                {
                    TenSanPham = "Laptop Gaming",
                    GiaBan = 25000000,
                    AnhMoTa = "/images/laptop.jpg"
                },
                new SanPhamViewModel
                {
                    TenSanPham = "Macbook Giá Rẻ",
                    GiaBan = 1000000,
                    AnhMoTa = "/images/macbook.jpg"
                },

            };
                return View(danhsachsanPham);
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
}
