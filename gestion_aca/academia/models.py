from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=150)
    credits = models.PositiveIntegerField()
    professor = models.CharField(max_length=150)
    students = models.ManyToManyField(Student, through='Enrollment', related_name='courses')

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    final_grade = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"