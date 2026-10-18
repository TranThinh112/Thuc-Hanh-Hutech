namespace test.Models;

public class Students
{
    public int Id {get; set; }
    public string Name {get; set; } ="";
    public string Email {get; set; } = "";
    public int GradeId { get; set; }
    public Grade Grade { get; set; }
}