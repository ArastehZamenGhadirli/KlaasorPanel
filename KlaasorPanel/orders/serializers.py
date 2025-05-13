from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from orders.models import Bootcamp, BootcampMembership , BootcampRegistrationRequest
from rest_framework import serializers


class BootcampCreate(ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = "__all__"


class BootcampRegister(serializers.ModelSerializer):
    class Meta:
        model = BootcampMembership
        fields = ["bootcamp"]

    def validate_bootcamp(self, bootcamp):
        if bootcamp.state != Bootcamp.State.REGISTRATION:
            raise serializers.ValidationError("Bootcamp is not open for registration.")
        if bootcamp.capacity <= 0:
            raise serializers.ValidationError("Bootcamp is full.")
        return bootcamp

    def create(self, validated_data):
        user = self.context["request"].user     # context give us current user
        bootcamp = validated_data["bootcamp"]

        if BootcampMembership.objects.filter(
            user=user, bootcamp=bootcamp, role=BootcampMembership.Role.STUDENT
        ).exists():
            raise serializers.ValidationError(
                "You are already registered in this bootcamp."
            )

        
        bootcamp.capacity -= 1
        bootcamp.save()

        return BootcampMembership.objects.create(
            user=user, bootcamp=bootcamp, role=BootcampMembership.Role.STUDENT
        )



class BootcampRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootcampRegistrationRequest
        fields = ['bootcamp', 'phone_number', 'email']