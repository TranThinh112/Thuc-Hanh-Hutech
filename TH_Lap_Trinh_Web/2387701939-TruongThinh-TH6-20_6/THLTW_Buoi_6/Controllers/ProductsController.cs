using Microsoft.AspNetCore.Mvc;
using THLTW_Buoi_6.Models;
using THLTW_Buoi_6.Repositories;

namespace THLTW_Buoi_6.Controllers;

public class ProductsController : Controller
{
    private readonly IProductRepository _productRepository;

    public ProductsController(IProductRepository productRepository)
    {
        _productRepository = productRepository;
    }

    public async Task<IActionResult> Index()
    {
        var products = await _productRepository.GetProductsAsync();
        return View(products);
    }

    public async Task<IActionResult> Details(int id)
    {
        var product = await _productRepository.GetProductByIdAsync(id);

        if (product is null)
        {
            return NotFound();
        }

        return View(product);
    }

    public IActionResult Create()
    {
        return View(new Product());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(Product product)
    {
        if (!ModelState.IsValid)
        {
            return View(product);
        }

        await _productRepository.AddProductAsync(product);
        TempData["SuccessMessage"] = "Da them san pham moi.";

        return RedirectToAction(nameof(Index));
    }

    public async Task<IActionResult> Edit(int id)
    {
        var product = await _productRepository.GetProductByIdAsync(id);

        if (product is null)
        {
            return NotFound();
        }

        return View(product);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, Product product)
    {
        if (id != product.Id)
        {
            return BadRequest();
        }

        if (!ModelState.IsValid)
        {
            return View(product);
        }

        var existingProduct = await _productRepository.GetProductByIdAsync(id);

        if (existingProduct is null)
        {
            return NotFound();
        }

        await _productRepository.UpdateProductAsync(product);
        TempData["SuccessMessage"] = "Da cap nhat san pham.";

        return RedirectToAction(nameof(Index));
    }

    public async Task<IActionResult> Delete(int id)
    {
        var product = await _productRepository.GetProductByIdAsync(id);

        if (product is null)
        {
            return NotFound();
        }

        return View(product);
    }

    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(int id)
    {
        var existingProduct = await _productRepository.GetProductByIdAsync(id);

        if (existingProduct is null)
        {
            return NotFound();
        }

        await _productRepository.DeleteProductAsync(id);
        TempData["SuccessMessage"] = "Da xoa san pham.";

        return RedirectToAction(nameof(Index));
    }
}
