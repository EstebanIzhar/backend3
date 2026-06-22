from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Student, Course, Enrollment
from . import serializers 
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    # Buscar estudiantes por nombre (?name=Felipe)
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    # Cursos de un estudiante: /api/students/{id}/courses/
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        student = self.get_object()
        courses = student.courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    # Promedio mayor a 90: /api/students/high_achievers/
    @action(detail=False, methods=['get'])
    def high_achievers(self, request):
        students = Student.objects.annotate(avg_grade=Avg('enrollments__final_grade')).filter(avg_grade__gt=90)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

    # Estudiantes inscritos en un curso: /api/courses/{id}/students/
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        students = course.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    # Cursos con más de 5 estudiantes: /api/courses/popular/
    @action(detail=False, methods=['get'])
    def popular(self, request):
        courses = Course.objects.annotate(num_students=Count('students')).filter(num_students__gt=5)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer