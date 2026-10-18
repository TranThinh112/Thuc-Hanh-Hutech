using Microsoft.AspNetCore.Mvc;
using test.Models;

namespace test.Controllers
{
    public class StudentController : Controller
    {
        private readonly AppDbContext _context;
        public StudentController(AppDbContext context)
        {
            _context = context;
        }
        public IActionResult Index()
        {
            List<Students> ListStudents = _context.Students.ToList();
            return View(ListStudents);
        }
    }
}
