using System.ComponentModel.DataAnnotations;

namespace THLTW_Buoi_5.Models;

public class Product
{
    public int Id { get; set; }

    [Required]
    public string Name { get; set; } = string.Empty;

    public decimal Price { get; set; }

    public string Description { get; set; } = string.Empty;

    public string ImageUrl { get; set; } = string.Empty;
}
