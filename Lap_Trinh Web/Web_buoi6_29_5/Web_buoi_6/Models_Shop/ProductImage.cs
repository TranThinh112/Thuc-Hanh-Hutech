using System.ComponentModel.DataAnnotations.Schema;

namespace Web_buoi_6.Models_Shop
{
    public class ProductImage
    {
        public int Id { get; set; }
        public string Url { get; set; }

        [ForeignKey("Product")]
        public int ProductId { get; set; }

        public Product? Product { get; set; }

    }
}
