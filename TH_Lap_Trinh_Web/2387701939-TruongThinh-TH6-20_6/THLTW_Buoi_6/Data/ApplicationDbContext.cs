using Microsoft.EntityFrameworkCore;
using THLTW_Buoi_6.Models;

namespace THLTW_Buoi_6.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Product>().HasData(
            new Product
            {
                Id = 1,
                Name = "Laptop Dell Inspiron",
                Price = 15990000,
                Description = "Laptop van phong cau hinh tot"
            },
            new Product
            {
                Id = 2,
                Name = "Ban phim co",
                Price = 850000,
                Description = "Ban phim co led trang"
            },
            new Product
            {
                Id = 3,
                Name = "Chuot khong day",
                Price = 320000,
                Description = "Chuot khong day nho gon"
            });
    }
}
