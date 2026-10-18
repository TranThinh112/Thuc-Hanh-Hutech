using System.ComponentModel.DataAnnotations;

namespace THLTW_Buoi_6.Models;

public class Product
{
    public int Id { get; set; }

    [Required]
    [StringLength(100)]
    public string Name { get; set; } = string.Empty;

    [Range(0, double.MaxValue)]
    public decimal Price { get; set; }

    [StringLength(500)]
    public string? Description { get; set; }
}
