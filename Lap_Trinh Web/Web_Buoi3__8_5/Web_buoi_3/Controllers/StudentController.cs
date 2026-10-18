using Microsoft.AspNetCore.Mvc;
using WebTestBuoi3.Models;

namespace WebTestBuoi3.Controllers
{
    public class StudentController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult ShowKQ(StudentViewModel sv)
        {
            int soLuong = 0;
            List<string> dsDangKy = new List<string>
            {
                "CNPM",
                "TY",
                "QTKD",
                "KT",
                "OT",
            };

            foreach (var nganh in dsDangKy)
            {
                if (nganh == sv.ChuyenNganh)
                {
                    soLuong++;
                }
            }

            ViewBag.SoLuong = soLuong;

            return View(sv);
        }
    }
}