from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from orders.models import Bootcamp, BootcampMembership , BootcampRegistrationRequest , BootcampCategory
from rest_framework import serializers


class BootcampCategorySerialzer(ModelSerializer):
    class Meta :
        model = BootcampCategory
        fields = ['id', 'name']


class BootcampSerilazer(ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = "__all__"


class BootcampRegisterSerilazer(serializers.ModelSerializer):
    class Meta:
        model = BootcampRegistrationRequest
        fields = ["bootcamp", "phone_number", "email"]

    def validate_bootcamp(self, bootcamp):
        if bootcamp.state != Bootcamp.State.REGISTRATION:
            raise serializers.ValidationError("بوتکمپ در وضعیت ثبت‌نام نیست.")
        return bootcamp

    def create(self, validated_data):
        # فقط درخواست رو ذخیره می‌کنیم. ظرفیت دست نمی‌خوره.
        return BootcampRegistrationRequest.objects.create(**validated_data)


class BootcampRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootcampRegistrationRequest
        fields = ['bootcamp', 'phone_number', 'email']


class BootcampDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)  # it will only give you more readable response 

    class Meta:
        model = Bootcamp
        fields = ['id', 'name', 'category_name', 'start_date', 'held_days', 'held_time', 'capacity', 'state']
        
        