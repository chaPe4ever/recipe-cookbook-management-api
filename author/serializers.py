from author.models import Author


class AuthorSerializer:
    class Meta:
        model = Author
        fields = ["user", "recipes", "cookbooks"]
