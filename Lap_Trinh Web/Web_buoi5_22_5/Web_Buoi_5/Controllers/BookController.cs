using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using Web_Buoi_5.Data;
using Web_Buoi_5.Models;

namespace Web_Buoi_5.Controllers;

public class BookController : Controller
{
    private readonly AppDbContext _context;

    public BookController(AppDbContext context)
    {
        _context = context;
    }

    public IActionResult Index()
    {
        var books = _context.Books
            .Include(x => x.Category)
            .ToList();

        return View(books);
    }

    public IActionResult Create()
    {
        ViewBag.Categories = new SelectList(
            _context.Categories.ToList(),
            "CategoryId",
            "CategoryName"
        );

        return View();
    }

    [HttpPost]
    public IActionResult Create(Book book)
    {
        if (ModelState.IsValid)
        {
            _context.Books.Add(book);
            _context.SaveChanges();
            return RedirectToAction("Index");
        }

        ViewBag.Categories = new SelectList(
            _context.Categories.ToList(),
            "CategoryId",
            "CategoryName",
            book.CategoryId
        );

        return View(book);
    }

    public IActionResult Edit(int id)
    {
        var book = _context.Books.Find(id);

        if (book == null)
            return NotFound();

        ViewBag.Categories = new SelectList(
            _context.Categories.ToList(),
            "CategoryId",
            "CategoryName",
            book.CategoryId
        );

        return View(book);
    }

    [HttpPost]
    public IActionResult Edit(Book book)
    {
        if (ModelState.IsValid)
        {
            _context.Books.Update(book);
            _context.SaveChanges();
            return RedirectToAction("Index");
        }

        ViewBag.Categories = new SelectList(
            _context.Categories.ToList(),
            "CategoryId",
            "CategoryName",
            book.CategoryId
        );

        return View(book);
    }

    public IActionResult Delete(int id)
    {
        var book = _context.Books
            .Include(x => x.Category)
            .FirstOrDefault(x => x.Id == id);

        if (book == null)
            return NotFound();

        return View(book);
    }

    [HttpPost]
    public IActionResult DeleteConfirmed(int id)
    {
        var book = _context.Books.Find(id);

        if (book == null)
            return NotFound();

        _context.Books.Remove(book);
        _context.SaveChanges();

        return RedirectToAction("Index");
    }

    public IActionResult Details(int id)
    {
        var book = _context.Books
            .Include(x => x.Category)
            .FirstOrDefault(x => x.Id == id);

        if (book == null)
            return NotFound();

        return View(book);
    }
}