from rest_framework import serializers


class BaseSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class LocationSerializers(BaseSerializer):
    latitude = serializers.CharField(required=False)
    longitude = serializers.CharField(required=False)


class ChatSerializer(BaseSerializer):
    id = serializers.IntegerField(required=False)
    is_bot = serializers.BooleanField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    type = serializers.CharField(required=False)


class SenderSerializer(BaseSerializer):
    id = serializers.IntegerField()
    is_bot = serializers.BooleanField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    language = serializers.CharField()


class CommandSerializer(BaseSerializer):
    type = serializers.CharField()
    length = serializers.IntegerField()
    offset = serializers.IntegerField()


class MessageSerializer(BaseSerializer):
    message_id = serializers.IntegerField()
    # sender = SenderSerializer(source='from')
    chat = ChatSerializer(many=False)
    # date = serializers.DateTimeField(required=False)
    location = LocationSerializers(required=False)
    entities = CommandSerializer(many=True, required=False)
    text = serializers.CharField(required=False)


class UpdateSerializer(BaseSerializer):
    update_id = serializers.IntegerField()
    message = MessageSerializer()
