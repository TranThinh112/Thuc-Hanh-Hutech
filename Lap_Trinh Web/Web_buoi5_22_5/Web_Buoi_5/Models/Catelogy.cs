namespace Web_Buoi_5.Models;


public class Category
{
    public int CategoryId { get; set; }
    public string CategoryName { get; set; }

    public List<Book> Books { get; set; } = new();
}