using Web_Buoi4.Model;

namespace Web_Buoi4.Model
{
    public static class TodoRepository
    {
        public static List<TodoItem> Tasks = new()
        {
            new TodoItem { Id = 1, TaskName = "Đi chợ", IsCompleted = true },
            new TodoItem { Id = 2, TaskName = "Chơi thể thao", IsCompleted = false },
            new TodoItem { Id = 3, TaskName = "Chơi game", IsCompleted = false },
            new TodoItem { Id = 4, TaskName = "Học bài", IsCompleted = true }
        };
    }
}