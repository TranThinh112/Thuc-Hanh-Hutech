using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ApplicationModels;
using test.Models;

namespace test.Controllers
{
    public class GradeController : Controller
    {
        private readonly AppDbContext _context;
        public GradeController(AppDbContext context)
        {
            _context = context;
        }
        public IActionResult Index()
        {
            List<Grade> ListGrade = _context.Grades.ToList();
            return View(ListGrade);
        }
    }
}
