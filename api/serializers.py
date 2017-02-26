from rest_framework import serializers

from base.models import ApplicationUser, Project, Task, Invite


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = ApplicationUser(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class RetrieveProjectSerializer(ProjectSerializer):
    managers = UserSerializer(many=True, read_only=True)
    developers = UserSerializer(many=True, read_only=True)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'project': {'read_only': True}
        }


class RetrieveTaskSerializer(TaskSerializer):
    assigned_to = UserSerializer(read_only=True)
    project = RetrieveProjectSerializer(read_only=True)


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ('pk', 'email', 'project')
        extra_kwargs = {
            'pk': {'read_only': True},
            'project': {'read_only': True},
        }
