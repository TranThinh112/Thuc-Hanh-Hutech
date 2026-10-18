using THLTW_Buoi_5.Services;
using Microsoft.AspNetCore.Mvc;

namespace THLTW_Buoi_5.Controllers;

public class ProductsController : Controller
{
    private readonly StoreDataService _storeData;

    public ProductsController(StoreDataService storeData)
    {
        _storeData = storeData;
    }

    public IActionResult Index()
    {
        return View(_storeData.GetProducts());
    }

    public IActionResult Details(int id)
    {
        var product = _storeData.GetProductById(id);

        if (product is null)
        {
            return NotFound();
        }

        return View(product);
    }
}
