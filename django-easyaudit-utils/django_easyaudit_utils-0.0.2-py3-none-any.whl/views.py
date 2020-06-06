from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent

from cbs.apps.core.views import PaginationMixin


User = get_user_model


class UserDateSearchMixin(View):
    def get_queryset(self):
        queryset = super().get_queryset()

        user_query = self.request.GET.get("user", None)
        date_query = self.request.GET.get("date", None)
        date2_query = self.request.GET.get("date2", None)

        # USER
        if user_query:
            user_lookup = Q()

            user_lookup = user_lookup | Q(**{User.USERNAME_FIELD: user_query})

            for key in REQUIRED_FIELDS:
                user_lookup = user_lookup | Q(**{key: user_query})

            user = User.objects.filter(user_lookup)

            if user.exists():
                queryset = queryset.filter(user__in=user)

        # Date & Date2
        if date_query:
            date_lookup = Q()

            try:
                date_lookup = date_lookup | Q(datetime__date__gte=datetime.strptime(date_query, "%Y-%m-%d").date())

                queryset = queryset.filter(date_lookup)

                try:
                    if date_query2:
                        date_lookup = date_lookup & Q(
                            datetime__date__lte=datetime.strptime(date_query2, "%Y-%m-%d").date()
                        )
                except BaseException:
                    pass
            except BaseException:
                pass
        return queryset


class IndexView(LoginRequiredMixin, UserDateSearchMixin, TemplateView):
    template_name = "easyaudit/index.html"


class CRUDEventListView(LoginRequiredMixin, PaginationMixin, UserDateSearchMixin, ListView):
    model = CRUDEvent
    paginate_by = 50


class LoginEventListView(LoginRequiredMixin, PaginationMixin, UserDateSearchMixin, ListView):
    model = LoginEvent  # TODO : Use Django-defender
    paginate_by = 50


class RequestEventListView(LoginRequiredMixin, PaginationMixin, UserDateSearchMixin, ListView):
    model = RequestEvent
    paginate_by = 50
