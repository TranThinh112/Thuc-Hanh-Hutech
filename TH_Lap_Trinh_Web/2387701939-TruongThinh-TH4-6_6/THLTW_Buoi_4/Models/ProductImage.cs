using System.ComponentModel.DataAnnotations.Schema;

namespace THLTW_buoi_4.Models
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
