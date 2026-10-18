using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Web_buoi_6.Models_Shop;

namespace Web_buoi_6.Models_Shop
{
    public class Product
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        [DisplayName("Mã sản phẩm")]
        public int Id { get; set; }

        [Required(ErrorMessage = "Tên sản phẩm không được để trống")]
        [StringLength(100, ErrorMessage = "Tên sản phẩm không được vượt quá 100 ký tự")]
        [DisplayName( "Tên sản phẩm")]
        public string Name { get; set; }

        [Range(0.01, 100000000, ErrorMessage = "Giá phải lớn hơn 0")]
        [DisplayName("Giá sản phẩm")]
        public decimal Price { get; set; }


        [DisplayName("Mô tả sản phẩm")]
        public string Description { get; set; }


        [DisplayName("Ảnh sản phẩm")]
        public string? ImageUrl { get; set; }
        public List<ProductImage>? Images { get; set; }

        [ForeignKey("Category")]
        [DisplayName("Mã danh mục")]
        public int CategoryId { get; set; }

        [DisplayName("Danh mục sản phẩm")]
        public Category? Category { get; set; }
    }
}
