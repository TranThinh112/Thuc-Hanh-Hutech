using Microsoft.EntityFrameworkCore;
using  Web_Buoi_5.Models;

namespace Web_Buoi_5.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<Student> Students { get; set; }

    public DbSet<Book> Books { get; set; }

    public DbSet<Category> Categories { get; set; }
}