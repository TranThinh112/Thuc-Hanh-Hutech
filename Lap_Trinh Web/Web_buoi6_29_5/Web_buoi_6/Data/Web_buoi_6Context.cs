using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

public class Web_buoi_6Context(DbContextOptions<Web_buoi_6Context> options) : IdentityDbContext<Web_buoi_6.Data.ApplicationUser>(options)
{
}
