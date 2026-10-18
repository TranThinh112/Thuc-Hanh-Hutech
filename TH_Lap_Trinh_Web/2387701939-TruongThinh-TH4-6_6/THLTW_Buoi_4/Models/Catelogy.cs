using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;


namespace THLTW_buoi_4.Models
{
    public class Category
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }

        [Required(ErrorMessage = "Tên danh mục không được để trống")]
        [StringLength(50, ErrorMessage = "Tên danh mục không được vượt quá 50 ký tự")]
        public string Name { get; set; }

        public List<Product> Products { get; set; }
    }
}