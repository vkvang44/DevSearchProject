# take python data and turn into JSON
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/projects/token'},
        {'POST': '/api/projects/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    # takes in the project queryset and turns it into a json object
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    # creating a new review object if it doesnt exist with authenticated owner and project
    # updates the review.value in the review model
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )
    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)