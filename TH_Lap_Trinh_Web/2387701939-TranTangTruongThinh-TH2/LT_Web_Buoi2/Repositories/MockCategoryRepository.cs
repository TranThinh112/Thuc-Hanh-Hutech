using LT_Web_Buoi2.Models;

namespace LT_Web_Buoi2.Repositories
{
    public class MockCategoryRepository : ICategoryRepository
    {
        private readonly List<Category> _categoryList;

        public MockCategoryRepository()
        {
            _categoryList = new List<Category>
            {
                new Category { Id = 1, Name = "Laptop" },
                new Category { Id = 2, Name = "Phone" },
                new Category { Id = 3, Name = "Ipad" },
                new Category { Id = 4, Name = "Thiet Bi Thong Minh" }
            };
        }

        public IEnumerable<Category> GetAllCategories()
        {
            return _categoryList;
        }
    }
}