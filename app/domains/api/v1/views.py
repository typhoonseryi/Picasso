from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from domains.models import Domain


class DomainsListApi(BaseListView):
    model = Domain
    http_method_names = ["get"]

    def get_queryset(self):
        filter_dict = {}
        filter_url = self.request.GET.get("url_name", None)
        if filter_url:
            filter_dict["url_name"] = filter_url
        filter_country = self.request.GET.get("country", None)
        if filter_country:
            filter_dict["country"] = filter_country
        filter_state = self.request.GET.get("state", None)
        if filter_state == "alive":
            filter_dict["is_dead"] = False
        elif filter_state == "dead":
            filter_dict["is_dead"] = True

        order_by_field = self.request.GET.get("sort", "-create_date")

        if filter_dict:
            return Domain.objects.filter(**filter_dict).order_by(order_by_field)
        else:
            return Domain.objects.all().order_by(order_by_field)

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        paginate_by = self.request.GET.get("limit", 50)
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, int(paginate_by)
        )

        item_list = list(queryset)
        results = []
        for item in item_list:
            item = model_to_dict(item)
            results.append(item)

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": results,
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
