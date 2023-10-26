import factory

from social.models import SiteComment
from user.factories import UserFactory


class SiteCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SiteComment

    user = factory.SubFactory(UserFactory)
    message = factory.Faker('text')
