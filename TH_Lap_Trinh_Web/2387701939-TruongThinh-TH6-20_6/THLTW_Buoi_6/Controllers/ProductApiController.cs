using Microsoft.AspNetCore.Mvc;
using THLTW_Buoi_6.Models;
using THLTW_Buoi_6.Repositories;

namespace THLTW_Buoi_6.Controllers;

[ApiController]
[Route("api/products")]
public class ProductApiController : ControllerBase
{
    private readonly IProductRepository _productRepository;

    public ProductApiController(IProductRepository productRepository)
    {
        _productRepository = productRepository;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<Product>>> GetProducts()
    {
        var products = await _productRepository.GetProductsAsync();
        return Ok(products);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<Product>> GetProductById(int id)
    {
        var product = await _productRepository.GetProductByIdAsync(id);

        if (product is null)
        {
            return NotFound();
        }

        return Ok(product);
    }

    [HttpPost]
    public async Task<ActionResult<Product>> AddProduct([FromBody] Product product)
    {
        await _productRepository.AddProductAsync(product);

        return CreatedAtAction(
            nameof(GetProductById),
            new { id = product.Id },
            product);
    }

    [HttpPut("{id:int}")]
    public async Task<IActionResult> UpdateProduct(int id, [FromBody] Product product)
    {
        if (id != product.Id)
        {
            return BadRequest();
        }

        var existingProduct = await _productRepository.GetProductByIdAsync(id);

        if (existingProduct is null)
        {
            return NotFound();
        }

        await _productRepository.UpdateProductAsync(product);

        return NoContent();
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> DeleteProduct(int id)
    {
        var existingProduct = await _productRepository.GetProductByIdAsync(id);

        if (existingProduct is null)
        {
            return NotFound();
        }

        await _productRepository.DeleteProductAsync(id);

        return NoContent();
    }
}
