import json
from channels.generic.websocket import AsyncWebsocketConsumer

"""
Base WebSocket consumer, async version. Provides a general encapsulation
for the WebSocket handling model that other applications can build on.
"""


class chatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # At first we need to take room_id from
        # url and store it in some variable

        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # creating room group name from room id
        self.room_group_name = 'chat_%s' % self.room_name

        # we'll place or add users in a group with same room_id with await
        # pass two arguments to group_add first is room_group_name
        # and second is channel_name, channel_name attribute contains
        # a pointer to channel layer instance

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # we need to accept or reject during
        # handshaking or bedore sending message

        await self.accept()

    # to discard the group
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receove the message from the websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # now send the data to group

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # type chatroom_messages later will create the chatroom_message async def with event
                'type': 'chatroom_messages',
                'message': message,
                'username': username
            }
        )

    # this has to be same as type in channel layer group send
    # in order to send the data to web socket we have ti receive the
    # message from group and then sen it to websocket

    async def chatroom_messages(self, event):

        # get message from group
        message = event['message']
        username = event['username']

        # now send the data to websocket using
        # AsyncWebsocketConsumer's send method

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    pass
