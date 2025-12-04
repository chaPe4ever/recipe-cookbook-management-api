from django.db.models import Q


class FilterMixin:
    filterset_fields = {}

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()

        for param, lookup in self.filterset_fields.items():
            if value := self.request.query_params.get(param):
                condition = {lookup: value}
                filters &= Q(**condition)

        return queryset.filter(filters)
