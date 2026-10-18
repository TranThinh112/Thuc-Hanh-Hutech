using THLTW_Buoi_5.Models;

namespace THLTW_Buoi_5.Services;

public class StoreDataService
{
    private readonly object _syncRoot = new();
    private readonly List<Order> _orders = new();
    private int _nextOrderId = 1;
    private int _nextOrderDetailId = 1;

    private readonly List<Product> _products =
    [
        new Product
        {
            Id = 1,
            Name = "Laptop học lập tập dành cho sinh viên",
            Price = 20500000,
            Description = "Máy gọn nhẹ, phù hợp học lập trình và làm bài thực hành.",
            ImageUrl = "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80"
        },
        new Product
        {
            Id = 2,
            Name = "Tai nghe Bluetooth",
            Price = 500000,
            Description = "Tai nghe không dây dùng khi học online, họp nhóm và giải trí.",
            ImageUrl = "https://www.google.com/aclk?sa=L&ai=DChsSEwiw98vJppWVAxVRfw8CHW88JdAYACICCAEQFxoCdGI&co=1&ase=2&gclid=CjwKCAjw9NjRBhATEiwA_p2J8fGTtM5cAg-up1LECq3N0U02_dJfRbB6a2815o-QN5y799QYvErF_hoCt-oQAvD_BwE&ei=CkI2atrBDd3R2roPhoyT0QY&cid=CAAS3gHkaA4ARY9xJblhBvenS0gqA-hL4_ng7-_y20Vs6GIWCMec-WTeWBEB85TEtlxu7MgX7mrvhC8Nmh8ZvpjUlfH4B80gTZLE8QV8LMdTDbANtvMUBTz6YPCHJdESHeUADKhZSs5m9thEEpEaeKzgNZ7VOHtU4eGvcYhLyUYRwI3wAgpA1OoNJl9whDf09zikenCdMYQF6Sn6XWDvRbqjU3lH7zHN8-WDskU45f3jRGUptV4p9u_HuQTJDCvCJPHKl9DHyMad0wGXkOfNHX5xM0heOEZZWtLxEyzq-kiKUos&cce=2&category=acrcp_v1_32&sig=AOD64_0p1nt1Wc4YjKwedWaDBFomJZhzDw&ctype=5&q=&nis=4&sqi=2&ved=2ahUKEwja7sHJppWVAxXdqFYBHQbGJGoQwg8oAXoECAwQEg&adurl="
        },
        new Product
        {
            Id = 3,
            Name = "Balo sinh viên",
            Price = 700000,
            Description = "Balo nhiều ngăn, có khoang laptop, chất liệu chống nước nhẹ.",
            ImageUrl = "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80"
        },
        new Product
        {
            Id = 4,
            Name = "Chuột không dây",
            Price = 500000,
            Description = "Chuột nhỏ gọn, thích hợp dùng cùng laptop.",
            ImageUrl = "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&q=80"
        },
        new Product
        {
            Id = 5,
            Name = "Đèn học",
            Price = 1500000,
            Description = "thiết kế nhỏ gọn, đơn giản và tính năng hiện đại.",
            ImageUrl = "https://phanduongminh.com/wp-content/uploads/2023/09/Den-hoc-de-ban-Nanoco-NDKC02B-den-600x600.jpg"
        }
    ];

    public IReadOnlyList<Product> GetProducts()
    {
        return _products;
    }

    public Product? GetProductById(int id)
    {
        return _products.FirstOrDefault(product => product.Id == id);
    }

    public Order AddOrder(Order order)
    {
        lock (_syncRoot)
        {
            order.Id = _nextOrderId++;
            order.OrderDate = DateTime.Now;

            foreach (var detail in order.OrderDetails)
            {
                detail.Id = _nextOrderDetailId++;
            }

            _orders.Add(order);
            return order;
        }
    }

    public Order? GetOrderById(int id)
    {
        lock (_syncRoot)
        {
            return _orders.FirstOrDefault(order => order.Id == id);
        }
    }
}
