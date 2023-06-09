from __future__ import annotations

import httpx

from pydantic import BaseModel, root_validator
from typing import Dict, List, Any, Union


class GeneralBaseModel(BaseModel):
    """Class for @root_validator"""

    @root_validator()
    def remove_none_field(cls, values):
        for key, value in values.copy().items():
            if value is None:
                del values[key]
        return values


class User(GeneralBaseModel):
    """This model represents a Telegram user or bot

    See here: https://core.telegram.org/bots/api#user
    """

    id: int
    is_bot: bool
    first_name: str
    last_name: str = None
    username: str = None
    language_code: str = None
    is_premium: bool = None
    added_to_attachment_menu: bool = None
    can_join_groups: bool = None
    can_read_all_group_messages: bool = None
    supports_inline_queries: bool = None


class Chat(GeneralBaseModel):
    """This model represents a chat

    See here: https://core.telegram.org/bots/api#chat
    """

    id: int
    type: str
    title: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    is_forum: bool = None
    photo: Dict[str, Any] = None
    active_usernames: List[str] = None
    emoji_status_custom_emoji_id: str = None
    bio: str = None
    has_private_forwards: bool = None
    has_restricted_voice_and_video_messages: bool = None
    join_to_send_messages: bool = None
    join_by_request: bool = None
    description: str = None
    invite_link: str = None
    pinned_message: Message = None
    permissions: Dict[str, Any] = None
    slow_mode_delay: int = None
    message_auto_delete_time: int = None
    has_aggressive_anti_spam_enabled: bool = None
    has_hidden_members: bool = None
    has_protected_content: bool = None
    sticker_set_name: str = None
    can_set_sticker_set: bool = None
    linked_chat_id: int = None


class KeyboardButton(GeneralBaseModel):
    """This model represents one button of the reply keyboard.
    For simple text buttons, String can be used instead of this object to specify the button text.
    The optional fields web_app, request_user, request_chat, request_contact,
    request_location, and request_poll are mutually exclusive.

    See here: https://core.telegram.org/bots/api#keyboardbutton
    """

    text: str
    request_user: Dict[str, Any] = None
    request_chat: Dict[str, Any] = None
    request_contact: bool = None
    request_location: bool = None
    request_poll: Dict[str, Any] = None
    web_app: Any = None


class ReplyKeyboardMarkup(GeneralBaseModel):
    """This model represents a custom keyboard with reply options

    See here: https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    keyboard: List[List[KeyboardButton]]
    is_persistent: bool = None
    resize_keyboard: bool = None
    one_time_keyboard: bool = None
    input_field_placeholder: str = None
    selective: bool = None


class ReplyKeyboardRemove(GeneralBaseModel):
    """Upon receiving a message with this object, Telegram clients will remove the current
    custom keyboard and display the default letter-keyboard. By default, custom keyboards
    are displayed until a new keyboard is sent by a bot. An exception is made for one-time
    keyboards that are hidden immediately after the user presses a button

    See here: https://core.telegram.org/bots/api#replykeyboardremove
    """
    remove_keyboard: bool
    selective: bool = None


class ForceReply(GeneralBaseModel):
    """Upon receiving a message with this object, Telegram clients will display a reply
    interface to the user (act as if the user has selected the bot's message and tapped 'Reply').
    This can be extremely useful if you want to create user-friendly step-by-step interfaces
    without having to sacrifice privacy mode.

    See here: https://core.telegram.org/bots/api#forcereply
    """
    force_reply: bool
    input_field_placeholder: bool = None
    selective: bool = None


class InlineKeyboardButton(GeneralBaseModel):
    """This model represents one button of an inline keyboard.

    See here: https://core.telegram.org/bots/api#inlinekeyboardbutton
    """

    text: str
    url: str = None
    callback_data: str = None
    web_app: Dict[str, Any] = None
    login_url: Dict[str, Any] = None
    switch_inline_query: str = None
    switch_inline_query_current_chat: str = None
    switch_inline_query_chosen_chat: Dict[str, Any] = None
    callback_game: Dict[str, Any] = None
    pay: bool = None


class InlineKeyboardMarkup(BaseModel):
    """This model represents an inline keyboard that appears right next to the message it belongs to.

    See here: https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """

    inline_keyboard: List[List[InlineKeyboardButton]]


class Invoice(GeneralBaseModel):
    """This model contains basic information about an invoice

    See here: https://core.telegram.org/bots/api#invoice
    """

    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class SuccessfulPayment(GeneralBaseModel):
    """This object contains basic information about a successful payment.

    See here: https://core.telegram.org/bots/api#successfulpayment
    """

    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: str = None
    order_info: OrderInfo = None
    telegram_payment_charge_id: str = None
    provider_payment_charge_id: str = None


class OrderInfo(GeneralBaseModel):
    """This object represents information about an order.

    See here: https://core.telegram.org/bots/api#orderinfo
    """

    name: str = None
    phone_number: str = None
    email: str = None
    shipping_address: ShippingAddress = None


class ShippingAddress(GeneralBaseModel):
    """This object represents a shipping address.

    See here: https://core.telegram.org/bots/api#shippingaddress
    """

    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class Message(GeneralBaseModel):
    """This model represents a message.

    See here: https://core.telegram.org/bots/api#message
    """

    message_id: int
    message_thread_id: int = None
    from_: User = None
    sender_chat: Chat = None
    date: int
    chat: Chat
    forward_from: User = None
    forward_from_chat: Chat = None
    forward_from_message_id: int = None
    forward_signature: str = None
    forward_sender_name: str = None
    forward_date: int = None
    is_topic_message: Dict[str, Any] = None
    is_automatic_forward: bool = None
    reply_to_message: 'Message' = None
    via_bot: User = None
    edit_date: int = None
    has_protected_content: bool = None
    media_group_id: str = None
    author_signature: str = None
    text: str = None
    entities: List[MessageEntity] = None
    animation: Dict[str, Any] = None
    audio: Dict[str, Any] = None
    document: Dict[str, Any] = None
    photo: List[Dict[str, Any]] = None
    sticker: Dict[str, Any] = None
    video: Dict[str, Any] = None
    video_note: Dict[str, Any] = None
    voice: Dict[str, Any] = None
    caption: str = None
    caption_entities: List[MessageEntity] = None
    has_media_spoiler: bool = None
    contact: Dict[str, Any] = None
    dice: Dict[str, Any] = None
    game: Dict[str, Any] = None
    poll: Dict[str, Any] = None
    venue: Dict[str, Any] = None
    location: Dict[str, Any] = None
    new_chat_members: List[User] = None
    left_chat_member: User = None
    new_chat_title: str = None
    new_chat_photo: List[Dict[str, Any]] = None
    delete_chat_photo: bool = None
    group_chat_created: bool = None
    supergroup_chat_created: bool = None
    channel_chat_created: bool = None
    message_auto_delete_timer_changed: List[Dict[str, Any]] = None
    migrate_to_chat_id: int = None
    migrate_from_chat_id: int = None
    pinned_message: 'Message' = None
    invoice: Invoice = None
    successful_payment: SuccessfulPayment = None
    user_shared: Dict[str, Any] = None
    chat_shared: Dict[str, Any] = None
    connected_website: str = None
    write_access_allowed: Dict[str, Any] = None
    passport_data: Dict[str, Any] = None
    proximity_alert_triggered: Dict[str, Any] = None
    forum_topic_created: Dict[str, Any] = None
    forum_topic_edited: Dict[str, Any] = None
    forum_topic_closed: Dict[str, Any] = None
    forum_topic_reopened: Dict[str, Any] = None
    general_forum_topic_hidden: Dict[str, Any] = None
    general_forum_topic_unhidden: Dict[str, Any] = None
    video_chat_scheduled: Dict[str, Any] = None
    video_chat_started: Dict[str, Any] = None
    video_chat_ended: Dict[str, Any] = None
    video_chat_participants_invited: Dict[str, Any] = None
    web_app_data: Dict[str, Any] = None
    reply_markup: InlineKeyboardMarkup = None


class MessageEntity(GeneralBaseModel):
    """This model represents one special entity in a text message.
    For example, hashtags, usernames, URLs, etc.

    See here: https://core.telegram.org/bots/api#messageentity
    """

    type: str
    offset: int
    length: int
    url: str = None
    user: User = None
    language: str = None
    custom_emoji_id: str = None


class TgHTTPStatusError(httpx._exceptions.HTTPStatusError):
    pass


class TgRuntimeError(RuntimeError):
    pass
