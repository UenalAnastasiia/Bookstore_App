from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from .filters import BookFilter
from .serializers import BookSerializer
from .models import Book


class BooksListView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    renderer_classes = [JSONRenderer, XMLRenderer]
    
    
    def get(self, request, format=None):
        book_list = Book.objects.filter(publish=True)
        filtered_queryset = self.filter_queryset(book_list)
        serializer = BookSerializer(filtered_queryset, many=True)
        return Response(serializer.data)


    def filter_queryset(self, queryset):
        filter_backends = self.filter_backends
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    

class BookDetailsView(APIView):
    def get(self, request, pk):   
        try:
            book_object = Book.objects.get(id=pk)
            serializer = BookSerializer(book_object)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class BooksViewSet(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    renderer_classes = [JSONRenderer, XMLRenderer]

    def get(self, request, format=None):
        book_list = Book.objects.all()
        filtered_queryset = self.filter_queryset(book_list)
        serializer = BookSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def filter_queryset(self, queryset):
        filter_backends = self.filter_backends
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class BookDetailsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book_object = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        book_object = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book_object = get_object_or_404(Book, pk=pk)
        book_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)