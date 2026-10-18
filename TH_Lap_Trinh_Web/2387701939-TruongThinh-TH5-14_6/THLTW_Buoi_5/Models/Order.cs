using System.ComponentModel.DataAnnotations;

namespace THLTW_Buoi_5.Models;

public class Order
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Vui lòng nhập tên người nhận.")]
    [Display(Name = "Người nhận")]
    public string CustomerName { get; set; } = string.Empty;

    [Required(ErrorMessage = "Vui lòng nhập số điện thoại.")]
    [Display(Name = "Số điện thoại")]
    public string Phone { get; set; } = string.Empty;

    [Required(ErrorMessage = "Vui lòng nhập địa chỉ giao hàng.")]
    [Display(Name = "Địa chỉ giao hàng")]
    public string ShippingAddress { get; set; } = string.Empty;

    [Display(Name = "Note")]
    public string? Notes { get; set; }

    public DateTime OrderDate { get; set; }

    public decimal TotalPrice { get; set; }

    public List<OrderDetail> OrderDetails { get; set; } = new();
}
