from rest_framework.serializers  import ModelSerializer
from accounts.models import Team  , CustomUser 


class AccountsSerializer(ModelSerializer):
    class Meta :
        model = CustomUser ,
        feilds = '__all__',
        read_only_fields = ['name']



