from rest_framework.views import APIView
from .models import Category
from rest_framework.response import Response
from rest_framework import status, permissions

# Create your views here.

class ListCategoryView(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self, request, format=None):
        if Category.objects.all().count():
            result=[]
            categories=Category.objects.all()
            for category in categories:
                if not category.parent:
                    item={}
                    item["id"]=category.id
                    item["name"]=category.name
                    item["slug"]=category.slug
                    item["views"]=category.views
                    item["sub_category"]=[]

                for sub_category in categories:
                    
                    sub_item={}
                    if sub_category.parent and sub_category.id == category.id:
                        sub_item["id"]=sub_category.id
                        sub_item["name"]=sub_category.name
                        sub_item["slug"]=sub_category.slug
                        sub_item["views"]=sub_category.views
                        sub_item["parent"]=sub_category.parent
                        item["sub_category"].append(sub_item)

                result.append(item)

            return Response({"response":result}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"No categories found"}, status=status.HTTP_404_NOT_FOUND)

