using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;

using Web_buoi_6.Models_Shop;


[Area("Admin")]
[Authorize(Roles = "Admin")]
public class CategoryController : Controller
{
    private readonly ApplicationDbContext _context;

    public CategoryController(ApplicationDbContext context)
    {
        _context = context;
    }

    public IActionResult Index()
    {
        var products = _context.Products.ToList();
        return View(products);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult DeleteConfirmed(int id)
    {
        var category = _context.Categories.Find(id);

        if (category == null)
        {
            return NotFound();
        }

        var products = _context.Products
            .Where(p => p.CategoryId == id)
            .ToList();

        _context.Products.RemoveRange(products);
        _context.Categories.Remove(category);

        _context.SaveChanges();

        return RedirectToAction(nameof(Index));
    }
}