using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Web_Buoi4.Model;

namespace Web_Buoi4.Pages.CreateTask
{
    public class CreateTaskModel : PageModel
    {
        [BindProperty]
        public TodoItem Task { get; set; } = new();

        public void OnGet()
        {
        }

         public IActionResult OnPost()
        {
            Task.Id = TodoRepository.Tasks.Max(x => x.Id) + 1;
            TodoRepository.Tasks.Add(Task);

            return RedirectToPage("/ToDoList");
        }
    }
}