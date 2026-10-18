namespace THLTW_Buoi_5.Models;

public class ShoppingCart
{
    public List<CartItem> Items { get; set; } = new();

    public decimal TotalPrice => Items.Sum(item => item.LineTotal);

    public int TotalQuantity => Items.Sum(item => item.Quantity);

    public void AddItem(CartItem item)
    {
        var existingItem = Items.FirstOrDefault(i => i.ProductId == item.ProductId);

        if (existingItem is null)
        {
            Items.Add(item);
            return;
        }

        existingItem.Quantity += item.Quantity;
    }

    public void UpdateQuantity(int productId, int quantity)
    {
        var item = Items.FirstOrDefault(i => i.ProductId == productId);

        if (item is null)
        {
            return;
        }

        if (quantity <= 0)
        {
            RemoveItem(productId);
            return;
        }

        item.Quantity = quantity;
    }

    public void RemoveItem(int productId)
    {
        Items.RemoveAll(i => i.ProductId == productId);
    }
}
