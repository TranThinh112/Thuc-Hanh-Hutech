namespace test.Models
{
    public class Grade
    {
        public int  GradeId { get; set; }
        public string GradeName { get; set; }
        public List<Students> Students { get; set; }
    }
}
