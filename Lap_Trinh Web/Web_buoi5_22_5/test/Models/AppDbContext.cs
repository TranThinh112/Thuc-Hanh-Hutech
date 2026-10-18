using test.Models;
using Microsoft.EntityFrameworkCore;

namespace test.Models
{
    public class AppDbContext: DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }
        public DbSet<Students> Students { get; set; }
        public DbSet<Grade> Grades { get; set; }
    }
}
