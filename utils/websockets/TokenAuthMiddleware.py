
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user(token):
    token = Token.objects.get(key=token)
    return token.user

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            query = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
            token = query['token']
            scope['user'] = await get_user(token)
        except:
            scope['user'] = AnonymousUser()
        return await self.inner(scope, receive, send)