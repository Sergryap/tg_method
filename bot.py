import httpx
import tg_obj


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
            On success, the sent message is returned as a Message instance
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
        await self.__tg_raise_for_status(response)
        res = response.json().get('result')
        if res.get('from'):
            res['from_'] = res.pop('from', None)
        return tg_obj.Message.parse_obj(res)

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
        await self.__tg_raise_for_status(response)
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
        await self.__tg_raise_for_status(response)
        return response

    async def send_photo(
            self,
            chat_id,
            photo,
            message_thread_id=None,
            caption=None,
            parse_mode=None,
            caption_entities=None,
            has_spoiler=None,
            disable_notification=None,
            protect_content=None,
            reply_to_message_id=None,
            allow_sending_without_reply=None,
            reply_markup=None
    ):
        """Use this method to send photos. On success, the sent Message is returned

        Args:
            See here: https://core.telegram.org/bots/api#sendphoto
        Returns:
            On success, the sent message is returned as a Message instance
        """

        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        params = {
            'chat_id': chat_id,
            'message_thread_id': message_thread_id,
            'photo': photo,
            'caption': caption,
            'parse_mode': parse_mode,
            'caption_entities': caption_entities,
            'has_spoiler': has_spoiler,
            'disable_notification': disable_notification,
            'protect_content': protect_content,
            'reply_to_message_id': reply_to_message_id,
            'allow_sending_without_reply': allow_sending_without_reply,
            'reply_markup': None if not reply_markup else reply_markup.json()
        }
        for param, value in params.copy().items():
            if value is None:
                del params[param]
        response = await self.session.get(url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        res = response.json().get('result')
        if res.get('from'):
            res['from_'] = res.pop('from', None)
        return tg_obj.Message.parse_obj(res)

    async def send_location(self):
        pass

    @staticmethod
    async def __tg_raise_for_status(response: httpx._models.Response):

        request = response._request
        if request is None:
            raise tg_obj.TgRuntimeError(
                "Cannot call `raise_for_status` as the request "
                "instance has not been set on this response."
            )

        if response.is_success:
            return

        if response.has_redirect_location:
            message = (
                "{error_type} '{0.status_code} {0.reason_phrase}' for url '{0.url}'\n"
                "Redirect location: '{0.headers[location]}'\n"
                "For more information check: https://httpstatuses.com/{0.status_code}"
            )
        else:
            message = (
                "{error_type} '{0.status_code} {0.reason_phrase}' for url '{0.url}'\n"
                "For more information check: https://httpstatuses.com/{0.status_code}"
            )

        status_class = response.status_code // 100
        error_types = {
            1: "Informational response",
            3: "Redirect response",
            4: "Client error",
            5: "Server error",
        }
        error_type = error_types.get(status_class, "Invalid status code")
        message = message.format(response, error_type=error_type)
        raise tg_obj.TgHTTPStatusError(message, request=request, response=response)
