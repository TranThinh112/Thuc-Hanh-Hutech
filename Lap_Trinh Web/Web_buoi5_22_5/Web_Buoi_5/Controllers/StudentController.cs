using Microsoft.AspNetCore.Mvc;
using Web_Buoi_5.Data;
using Web_Buoi_5.Models;

namespace Web_Buoi_5.Controllers;

public class StudentsController : Controller
{
    private readonly AppDbContext _context;

    public StudentsController(AppDbContext context)
    {
        _context = context;
    }

    public IActionResult Index()
    {
        var students = _context.Students.ToList();
        return View(students);
    }

    [HttpGet]
    public IActionResult Create()
    {
        return View();
    }

    [HttpPost]
    public IActionResult Create(Student student)
    {
        if (!ModelState.IsValid)
            return View(student);

        _context.Students.Add(student);
        _context.SaveChanges();

        return RedirectToAction(nameof(Index));
    }
}