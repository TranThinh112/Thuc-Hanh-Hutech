using Microsoft.EntityFrameworkCore;
using THLTW_Buoi_6.Data;
using THLTW_Buoi_6.Models;

namespace THLTW_Buoi_6.Repositories;

public class ProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context;

    public ProductRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Product>> GetProductsAsync()
    {
        return await _context.Products
            .AsNoTracking()
            .ToListAsync();
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        return await _context.Products
            .AsNoTracking()
            .FirstOrDefaultAsync(product => product.Id == id);
    }

    public async Task AddProductAsync(Product product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
    }

    public async Task UpdateProductAsync(Product product)
    {
        _context.Entry(product).State = EntityState.Modified;
        await _context.SaveChangesAsync();
    }

    public async Task DeleteProductAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);

        if (product is null)
        {
            return;
        }

        _context.Products.Remove(product);
        await _context.SaveChangesAsync();
    }
}
