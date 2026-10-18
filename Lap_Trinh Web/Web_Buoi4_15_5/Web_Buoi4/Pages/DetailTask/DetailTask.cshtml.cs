using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Web_Buoi4.Model;

namespace Web_Buoi4.Pages.DetailTask
{
    public class DetailTaskModel : PageModel
    {
        public TodoItem Task { get; set; } = new();

        public IActionResult OnGet(int id)
        {
            var item = TodoRepository.Tasks.FirstOrDefault(x => x.Id == id);

            if (item == null)
                return RedirectToPage("/ToDoList");

            Task = item;
            return Page();
        }
    }
}