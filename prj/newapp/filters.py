import django_filters
from django_filters import FilterSet,CharFilter, ModelChoiceFilter, DateFromToRangeFilter, ModelMultipleChoiceFilter, DateTimeFilter
from django.forms import DateInput
from .models import Post, Category, Comment
from django.contrib.auth.models import User


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'categoryType':['exact'],


        }



    Date = django_filters.DateTimeFilter(

    field_name='article',
    lookup_expr='gt',
    label='Date',
    widget=DateInput(
        format='%Y-%m-%dT%H:%M',
        attrs={'type': 'date'},
         ),
)


post_category = ModelMultipleChoiceFilter(
    field_name = 'post_category',
    queryset= Category.objects.all(),
    label = 'Категория поста',
    conjoined = True,

)

class F(FilterSet):
    username = CharFilter(method='my_filter')

    class Meta:
        model = User
        fields = ['username']

    def my_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })


class C(FilterSet):

        category = ModelChoiceFilter(queryset=Category.objects.all())

        class Meta:
            model = Post
            fields = ['category']


class X (FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = Comment
        fields = ['date']