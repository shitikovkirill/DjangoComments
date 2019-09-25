from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from apps.user.accounts.channel import channel

application = ProtocolTypeRouter({"channel": ChannelNameRouter(channel)})
