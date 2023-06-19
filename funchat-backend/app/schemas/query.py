from . import ma


class QuerySchema(ma.Schema):
    class Meta:
        fields = ("query", "sort", "page", "size", "type", "search")
