from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # a nested serializer within Projects to get the data from owner and tags
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)

    # create a new attribute by using a methodfield
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    # associated with SerializerMethodField(), gets the review data and serializes it into a json object
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data