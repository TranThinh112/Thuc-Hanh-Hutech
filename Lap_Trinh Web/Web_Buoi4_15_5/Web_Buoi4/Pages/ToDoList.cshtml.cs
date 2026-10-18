using Microsoft.AspNetCore.Mvc.RazorPages;
using Web_Buoi4.Model;

namespace Web_Buoi4.Pages
{
    public class TodoListModel : PageModel
    {
        public List<TodoItem> Tasks = new List<TodoItem>();

        public void OnGet()
        {
               Tasks = TodoRepository.Tasks;
        }
    }
}