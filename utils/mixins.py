from django.http import Http404


class AllowRegularUserMixin(object):

    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.is_superuser:
                return super(AllowRegularUserMixin, self).dispatch(request, *args, **kwargs)
            raise Http404()
        except:
            raise Http404()
