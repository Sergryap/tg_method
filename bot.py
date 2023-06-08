import httpx

from response_obj import Message


class Bot:
    """The class of tg bot methods"""

    def __init__(self, tg_token: str, session: httpx.AsyncClient, loop=None):
        self.token = tg_token
        self.session = session
        self.loop = loop

    async def send_message(
            self,
            chat_id,
            text,
            parse_mode=None,
            entities=None,
            disable_web_page_preview=None,
            disable_notification=None,
            protect_content=None,
            message_thread_id=None,
            allow_sending_without_reply=None,
            reply_markup=None,
    ):

        """Use this method to send text messages.

        Args:
            See here https://core.telegram.org/bots/api#sendmessage
        Returns:
            On success, the sent Message is returned

        """

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'entities': entities,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'protect_content': protect_content,
            'message_thread_id': message_thread_id,
            'allow_sending_without_reply': allow_sending_without_reply,
            'reply_markup': None if not reply_markup else reply_markup.json()
        }
        for param, value in params.copy().items():
            if value is None:
                del params[param]
        response = await self.session.get(url, params=params, follow_redirects=True)
        response.raise_for_status()
        res = response.json().get('result')
        if res.get('from'):
            res['from_'] = res.pop('from', None)
        return Message.parse_obj(res)

    async def set_webhook(
            self,
            url,
            certificate=None,
            ip_address=None,
            max_connections=None,
            allowed_updates=None,
            drop_pending_updates=None,
            secret_token=None
    ):
        """Use this method to specify a URL and receive incoming updates via an outgoing webhook.

        Whenever there is an update for the bot, we will send an HTTPS POST request to the specified URL,
        containing a JSON-serialized Update.
        In case of an unsuccessful request, we will give up after a reasonable amount of attempts.

        Args:
            See here https://core.telegram.org/bots/api#setwebhook
        Returns:
            True on success

        """

        request_url = f"https://api.telegram.org/bot{self.token}/setWebhook"
        params = {
            'url': url,
            'certificate': certificate,
            'ip_address': ip_address,
            'max_connections': max_connections,
            'allowed_updates': allowed_updates,
            'drop_pending_updates': drop_pending_updates,
            'secret_token': secret_token
        }
        for param, value in params.copy().items():
            if value is None:
                del params[param]
        response = await self.session.post(request_url, params=params, follow_redirects=True)
        response.raise_for_status()
        return response

    async def delete_webhook(
            self,
            drop_pending_updates=None
    ):
        """Use this method to remove webhook integration if you decide to switch back to getUpdates.
        See here: https://core.telegram.org/bots/api#deletewebhook

        Args:
            drop_pending_updates (bool): Pass True to drop all pending updates
        Returns:
            True on success.

        """

        request_url = f"https://api.telegram.org/bot{self.token}/deleteWebhook"
        params = None
        if drop_pending_updates:
            params = {'drop_pending_updates': drop_pending_updates}
        response = await self.session.post(request_url, params=params, follow_redirects=True)
        response.raise_for_status()
        return response

    async def send_photo(self):
        pass

    async def send_location(self):
        pass
