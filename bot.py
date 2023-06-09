import httpx
import tg_obj


class Bot:
    """The class of tg bot methods"""

    def __init__(self, tg_token: str, session: httpx.AsyncClient):
        self.url_start = f'https://api.telegram.org/bot{tg_token}/'
        self.session = session

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

        params = await self.__clean_params(locals())
        url = self.url_start + 'sendMessage'
        response = await self.session.get(url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        res = response.json().get('result')
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

        params = await self.__clean_params(locals())
        request_url = self.url_start + 'setWebhook'
        response = await self.session.post(request_url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        return response.json()

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

        request_url = self.url_start + 'deleteWebhook'
        params = None
        if drop_pending_updates:
            params = {'drop_pending_updates': drop_pending_updates}
        response = await self.session.post(request_url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        return response.json()

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

        params = await self.__clean_params(locals())
        url = self.url_start + 'sendPhoto'
        response = await self.session.get(url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        res = response.json().get('result')
        return tg_obj.Message.parse_obj(res)

    async def send_document(
            self,
            chat_id,
            document,
            message_thread_id=None,
            thumbnail=None,
            caption=None,
            parse_mode=None,
            caption_entities=None,
            disable_content_type_detection=None,
            disable_notification=None,
            protect_content=None,
            reply_to_message_id=None,
            allow_sending_without_reply=None,
            reply_markup=None
    ):
        """Use this method to send general files.
        On success, the sent Message is returned. Bots can currently send files
        of any type of up to 50 MB in size, this limit may be changed in the future.

        Args:
            See here: https://core.telegram.org/bots/api#senddocument
        Returns:
            On success, the sent message is returned as a Message instance
        """

        params = await self.__clean_params(locals())
        url = self.url_start + 'sendDocument'
        response = await self.session.get(url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        res = response.json().get('result')
        return tg_obj.Message.parse_obj(res)

    async def answer_callback_query(
            self,
            callback_query_id,
            text=None,
            show_alert=None,
            url=None,
            cache_time=None
    ):
        """Use this method to send answers to callback queries sent from inline keyboards.
        The answer will be displayed to the user as a notification at the top of the chat
        screen or as an alert. On success, True is returned.

        Args:
            See here: https://core.telegram.org/bots/api#answercallbackquery
        Returns:
            On success, True is returned
        """

        params = await self.__clean_params(locals())
        request_url = self.url_start + 'answerCallbackQuery'
        response = await self.session.get(request_url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        return response.json()

    async def edit_message_reply_markup(
            self,
            chat_id=None,
            message_id=None,
            inline_message_id=None,
            reply_markup=None
    ):
        """Use this method to edit only the reply markup of messages.

        Args:
            See here: https://core.telegram.org/bots/api#editmessagereplymarkup
        Return:
            On success, if the edited message is not an inline message,
            the edited Message is returned, otherwise True is returned.
        """

        params = await self.__clean_params(locals())
        url = self.url_start + 'editMessageReplyMarkup'
        response = await self.session.get(url, params=params, follow_redirects=True)
        await self.__tg_raise_for_status(response)
        res = response.json().get('result')
        return tg_obj.MessageReplyMarkup.parse_obj(res)

    async def send_location(self):
        pass

    @staticmethod
    async def __tg_raise_for_status(response: httpx._models.Response):
        """Raise the `TgHTTPStatusError` if one occurred.

        Args:
            response: httpx._models.Response instance
        """

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

    @staticmethod
    async def __clean_params(initial_params):
        """Getting clean parameters for a request.

        Args:
            initial_params (dict): initial parameters from functions arguments
        Returns:
            Clean parameters for request as dict
        """

        params = {key: value for key, value in initial_params.items() if value is not None}
        del params['self']
        if params.get('reply_markup'):
            params['reply_markup'] = params['reply_markup'].json()
        return params
