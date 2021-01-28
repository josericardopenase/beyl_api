from .models import Article
from rest_framework.serializers import ModelSerializer
from users.serializers.profile import ProfileSerializer


class ArticleSerializer(ModelSerializer):

    author = ProfileSerializer()

    class Meta:
        model = Article
        fields = ('title', 'texto', 'image', 'author', 'created')
