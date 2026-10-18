using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Web_Buoi4.Model;

namespace Web_Buoi4.Pages.EditTask
{
    public class EditTaskModel : PageModel
    {
        [BindProperty]
        public TodoItem Task { get; set; } = new();

        public IActionResult OnGet(int id)
        {
            var item = TodoRepository.Tasks.FirstOrDefault(x => x.Id == id);

            if (item == null)
                return RedirectToPage("/ToDoList");

            Task = item;
            return Page();
        }


         public IActionResult OnPost()
        {
            var item = TodoRepository.Tasks.FirstOrDefault(x => x.Id == Task.Id);

            if (item != null)
            {
                item.TaskName = Task.TaskName;
                item.IsCompleted = Task.IsCompleted;
            }

            return RedirectToPage("/ToDoList");
        }
    }
}