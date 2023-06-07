import httpx

from response_validate import VerifyMessage


class Bot:

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

        """Message sending"""

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
            'reply_markup': reply_markup,

        }
        for param, value in params.copy().items():
            if value is None:
                del params[param]
        response = await self.session.get(url, params=params, follow_redirects=True)
        response.raise_for_status()
        res = response.json().get('result')
        res['from_'] = res.pop('from', None)
        clean_response = VerifyMessage(**res)
        await clean_response.clean_response()

        return clean_response

