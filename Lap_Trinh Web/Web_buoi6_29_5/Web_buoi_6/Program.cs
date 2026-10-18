using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Web_buoi_6.Models_Shop;
using Web_buoi_6.Repositories;
using Web_buoi_6.Data;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

builder.Services.AddScoped<IProductRepository, EFProductRepository>();
builder.Services.AddScoped<ICategoryRepository, EFCategoryRepository>();

// Add services to the container.
builder.Services.AddControllersWithViews();

builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"))
);

builder.Services.AddDefaultIdentity<ApplicationUser>(options =>
{
    options.SignIn.RequireConfirmedAccount = false;
})
.AddRoles<IdentityRole>()
.AddEntityFrameworkStores<ApplicationDbContext>();

//tao role cho addmin vba member
async Task SeedRolesAsync(IServiceProvider serviceProvider)
{
    var roleManager = serviceProvider.GetRequiredService<RoleManager<IdentityRole>>();
    var userManager = serviceProvider.GetRequiredService<UserManager<ApplicationUser>>();

    string[] roles = { "Admin", "Member" };

    foreach (var role in roles)
    {
        if (!await roleManager.RoleExistsAsync(role))
        {
            await roleManager.CreateAsync(new IdentityRole(role));
        }
    }

    var adminEmail = "admin@gmail.com";
    var adminPassword = "Admin@123";

    var adminUser = await userManager.FindByEmailAsync(adminEmail);

    if (adminUser == null)
    {
        adminUser = new ApplicationUser
        {
            UserName = adminEmail,
            Email = adminEmail,
            EmailConfirmed = true,
            FullName = "Administrator",
            Address = "Admin Address"
        };

        await userManager.CreateAsync(adminUser, adminPassword);
        await userManager.AddToRoleAsync(adminUser, "Admin");
    }

    var memberEmail = "member@gmail.com";
    var memberPassword = "Member@123";

    var memberUser = await userManager.FindByEmailAsync(memberEmail);

    if (memberUser == null)
    {
        memberUser = new ApplicationUser
        {
            UserName = memberEmail,
            Email = memberEmail,
            EmailConfirmed = true,
            FullName = "Member User",
            Address = "Member Address"
        };

        await userManager.CreateAsync(memberUser, memberPassword);
        await userManager.AddToRoleAsync(memberUser, "Member");
    }
}


builder.Services.AddRazorPages();

//add services to the container
builder.Services.AddControllersWithViews();

//add services for weather api
builder.Services.Configure<WeatherApiSettings>(
    builder.Configuration.GetSection("WeatherApi"));

builder.Services.AddHttpClient();

builder.Services.AddScoped<WeatherService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}


app.UseHttpsRedirection();
app.UseRouting();

app.UseAuthentication();

app.UseAuthorization();


app.MapStaticAssets();

app.MapControllerRoute(
    name: "areas",
    pattern: "{area:exists}/{controller}/{action=Index}/{id?}");

// app.MapControllerRoute(
//     name: "default",
//     pattern: "{controller=Shop}/{action=Index}/{id?}");

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Shop}/{action=Index}/{id?}")
    .WithStaticAssets();

app.MapRazorPages();

using (var scope = app.Services.CreateScope())
{
    await SeedRolesAsync(scope.ServiceProvider);
}

app.Run();
