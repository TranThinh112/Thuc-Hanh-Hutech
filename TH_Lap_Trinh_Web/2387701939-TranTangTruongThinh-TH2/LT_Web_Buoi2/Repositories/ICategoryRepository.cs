using LT_Web_Buoi2.Models;

namespace LT_Web_Buoi2.Repositories
{
    public interface ICategoryRepository
    {
        IEnumerable<Category> GetAllCategories();
    }
}