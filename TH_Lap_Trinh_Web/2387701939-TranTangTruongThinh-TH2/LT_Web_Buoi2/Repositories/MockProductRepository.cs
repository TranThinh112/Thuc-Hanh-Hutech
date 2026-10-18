using LT_Web_Buoi2.Models;

namespace LT_Web_Buoi2.Repositories
{
    public class MockProductRepository : IProductRepository
    {
        private readonly List<Product> _products;

        public MockProductRepository()
        {
            _products = new List<Product>
            {
                new Product
                {
                    Id = 1,
                    Name = "Laptop",
                    Price = 15000000,
                    Description = "Laptop học tập và làm việc",
                    CategoryId = 1,
                    ImageUrl = "/images/Laptop.png"
                },
                new Product
                {
                    Id = 2,
                    Name = "iPhone 15",
                    Price = 23000000,
                    Description = "Điện thoại iPhone 15",
                    CategoryId = 2,
                    ImageUrl = "/images/IP17.png"
                },
                new Product
                {
                    Id = 3,
                    Name = "Tai nghe Bluetooth",
                    Price = 500000,
                    Description = "Tai nghe không dây",
                    CategoryId = 3,
                    ImageUrl = "/images/taiNghe0day.png"
                }
            };
        }

        public IEnumerable<Product> GetAll()
        {
            return _products;
        }

        public Product GetById(int id)
        {
            return _products.FirstOrDefault(p => p.Id == id);
        }

        public void Add(Product product)
        {
            product.Id = _products.Max(p => p.Id) + 1;
            _products.Add(product);
        }

        public void Update(Product product)
        {
            var index = _products.FindIndex(p => p.Id == product.Id);

            if (index != -1)
            {
                _products[index] = product;
            }
        }

        public void Delete(int id)
        {
            var product = _products.FirstOrDefault(p => p.Id == id);

            if (product != null)
            {
                _products.Remove(product);
            }
        }
    }
}