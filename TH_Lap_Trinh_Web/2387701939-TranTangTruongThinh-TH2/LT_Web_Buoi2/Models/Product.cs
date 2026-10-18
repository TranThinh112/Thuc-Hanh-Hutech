using System.ComponentModel.DataAnnotations;

namespace LT_Web_Buoi2.Models
{
    public class Product
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Tên sản phẩm không được để trống")]
        [StringLength(100)]
        public string Name { get; set; }

        [Range(0.01, 100000000, ErrorMessage = "Giá phải lớn hơn 0")]
        public decimal Price { get; set; }

        public string Description { get; set; }

        [Display(Name = "Category")]
        public int CategoryId { get; set; }

        public string? ImageUrl { get; set; }
        public List<string> ImageUrls { get; set; } = new();

    }
}