from rest_framework import viewsets


class ViewSetUtils(viewsets.ModelViewSet):
    @staticmethod
    def search_by_page(queryset, request, fields=None):
        """分页查询"""
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        if fields is None:
            fields = []
        start = (page - 1) * page_size
        end = page * page_size
        total = queryset.count()
        data = queryset.values(*fields)[start:end]
        return list(data), total
