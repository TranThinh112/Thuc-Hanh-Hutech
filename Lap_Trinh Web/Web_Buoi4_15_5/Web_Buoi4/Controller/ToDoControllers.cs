using Microsoft.AspNetCore.Mvc;
using Web_Buoi4.Model;



namespace Web_Buoi4.Controllers
{
public class TodoController : Controller
 {
     // Fake database
     private static List<TodoItem> todos = new List<TodoItem>()
     {
         new TodoItem{ Id=1, TaskName="Đi chợ", IsCompleted=true},
         new TodoItem{ Id=2, TaskName="Chơi thể thao", IsCompleted=false},
         new TodoItem{ Id=3, TaskName="Chơi game", IsCompleted=false},
         new TodoItem{ Id=4, TaskName="Học bài", IsCompleted=true},
     };

     // ================== LIST ==================
     public IActionResult Index()
     {
         return View(todos);
     }

     // ================== DETAILS ==================
     public IActionResult Details(int id)
     {
         var item = todos.FirstOrDefault(x => x.Id == id);
         return View(item);
     }

     // ================== CREATE ==================
     public IActionResult Create()
     {
         return View();
     }

     [HttpPost]
     public IActionResult Create(TodoItem model)
     {
         model.Id = todos.Max(x => x.Id) + 1;
         todos.Add(model);

         return RedirectToAction("Index");
     }

     // ================== EDIT ==================
     public IActionResult Edit(int id)
     {
         var item = todos.FirstOrDefault(x => x.Id == id);
         return View(item);
     }

     [HttpPost]
     public IActionResult Edit(TodoItem model)
     {
         var item = todos.FirstOrDefault(x => x.Id == model.Id);

         item.TaskName = model.TaskName;
         item.IsCompleted = model.IsCompleted;

         return RedirectToAction("Index");
     }

     // ================== DELETE ==================
     public IActionResult Delete(int id)
     {
         var item = todos.FirstOrDefault(x => x.Id == id);
         return View(item);
     }

     [HttpPost]
     public IActionResult DeleteConfirm(int id)
     {
         var item = todos.FirstOrDefault(x => x.Id == id);
         todos.Remove(item);

         return RedirectToAction("Index");
     }
 }
}