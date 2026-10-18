using THLTW_Buoi_5.Extensions;
using THLTW_Buoi_5.Models;
using THLTW_Buoi_5.Services;
using Microsoft.AspNetCore.Mvc;

namespace THLTW_Buoi_5.Controllers;

public class ShoppingCartController : Controller
{
    private const string CartSessionKey = "Cart";
    private readonly StoreDataService _storeData;

    public ShoppingCartController(StoreDataService storeData)
    {
        _storeData = storeData;
    }

    public IActionResult Index()
    {
        return View(GetCart());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult AddToCart(int productId, int quantity = 1)
    {
        var product = _storeData.GetProductById(productId);

        if (product is null)
        {
            return NotFound();
        }

        if (quantity < 1)
        {
            quantity = 1;
        }

        var cart = GetCart();
        cart.AddItem(new CartItem
        {
            ProductId = product.Id,
            Name = product.Name,
            Price = product.Price,
            ImageUrl = product.ImageUrl,
            Quantity = quantity
        });
        SaveCart(cart);

        TempData["SuccessMessage"] = $"Đã thêm {product.Name} vào giỏ hàng.";
        return RedirectToAction(nameof(Index));
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult UpdateQuantity(int productId, int quantity)
    {
        var cart = GetCart();
        cart.UpdateQuantity(productId, quantity);
        SaveCart(cart);

        TempData["SuccessMessage"] = "Đã cập nhật giỏ hàng.";
        return RedirectToAction(nameof(Index));
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult RemoveFromCart(int productId)
    {
        var cart = GetCart();
        cart.RemoveItem(productId);
        SaveCart(cart);

        TempData["SuccessMessage"] = "Đã xóa sản phẩm khỏi giỏ hàng.";
        return RedirectToAction(nameof(Index));
    }

    public IActionResult Checkout()
    {
        var cart = GetCart();

        if (!cart.Items.Any())
        {
            TempData["ErrorMessage"] = "Giỏ hàng đang trống.";
            return RedirectToAction(nameof(Index));
        }

        return View(new Order());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Checkout([Bind("CustomerName,Phone,ShippingAddress,Notes")] Order order)
    {
        var cart = GetCart();

        if (!cart.Items.Any())
        {
            TempData["ErrorMessage"] = "Giỏ hàng đang trống.";
            return RedirectToAction(nameof(Index));
        }

        if (!ModelState.IsValid)
        {
            return View(order);
        }

        order.TotalPrice = cart.TotalPrice;
        order.OrderDetails = cart.Items.Select(item => new OrderDetail
        {
            ProductId = item.ProductId,
            ProductName = item.Name,
            Price = item.Price,
            Quantity = item.Quantity
        }).ToList();

        var savedOrder = _storeData.AddOrder(order);
        HttpContext.Session.Remove(CartSessionKey);

        return RedirectToAction(nameof(OrderCompleted), new { id = savedOrder.Id });
    }

    public IActionResult OrderCompleted(int id)
    {
        var order = _storeData.GetOrderById(id);

        if (order is null)
        {
            return NotFound();
        }

        return View(order);
    }

    private ShoppingCart GetCart()
    {
        return HttpContext.Session.GetObjectFromJson<ShoppingCart>(CartSessionKey) ?? new ShoppingCart();
    }

    private void SaveCart(ShoppingCart cart)
    {
        HttpContext.Session.SetObjectAsJson(CartSessionKey, cart);
    }
}
