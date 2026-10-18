namespace THLTW_Buoi_5.Models;

public class OrderDetail
{
    public int Id { get; set; }

    public int ProductId { get; set; }

    public string ProductName { get; set; } = string.Empty;

    public decimal Price { get; set; }

    public int Quantity { get; set; }

    public decimal LineTotal => Price * Quantity;
}
