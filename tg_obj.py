from __future__ import annotations

import httpx

from pydantic import BaseModel as GeneralBaseModel, root_validator, AnyHttpUrl, Field
from typing import Any, Union, TypeVar


class BaseModel(GeneralBaseModel):
    """Class for @root_validator"""

    @root_validator()
    def remove_none_field(cls, values):
        for key, value in values.copy().items():
            if value is None:
                del values[key]
        return values


class User(BaseModel):
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


class Chat(BaseModel):
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
    photo: dict[str, Any] = None
    active_usernames: list[str] = None
    emoji_status_custom_emoji_id: str = None
    bio: str = None
    has_private_forwards: bool = None
    has_restricted_voice_and_video_messages: bool = None
    join_to_send_messages: bool = None
    join_by_request: bool = None
    description: str = None
    invite_link: str = None
    pinned_message: Message = None
    permissions: dict[str, Any] = None
    slow_mode_delay: int = None
    message_auto_delete_time: int = None
    has_aggressive_anti_spam_enabled: bool = None
    has_hidden_members: bool = None
    has_protected_content: bool = None
    sticker_set_name: str = None
    can_set_sticker_set: bool = None
    linked_chat_id: int = None


class KeyboardButton(BaseModel):
    """This model represents one button of the reply keyboard.
    For simple text buttons, String can be used instead of this model to specify the button text.
    The optional fields web_app, request_user, request_chat, request_contact,
    request_location, and request_poll are mutually exclusive.

    See here: https://core.telegram.org/bots/api#keyboardbutton
    """

    text: str
    request_user: dict[str, Union[int, bool]] = None
    request_chat: dict[str, Union[int, bool, dict[str, bool]]] = None
    request_contact: bool = None
    request_location: bool = None
    request_poll: dict[str, str] = None
    web_app: dict[str, AnyHttpUrl] = None


class ReplyKeyboardMarkup(BaseModel):
    """This model represents a custom keyboard with reply options

    See here: https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    keyboard: list[list[KeyboardButton]]
    is_persistent: bool = None
    resize_keyboard: bool = None
    one_time_keyboard: bool = None
    input_field_placeholder: str = None
    selective: bool = None


class ReplyKeyboardRemove(BaseModel):
    """Upon receiving a message with this model, Telegram clients will remove the current
    custom keyboard and display the default letter-keyboard. By default, custom keyboards
    are displayed until a new keyboard is sent by a bot. An exception is made for one-time
    keyboards that are hidden immediately after the user presses a button

    See here: https://core.telegram.org/bots/api#replykeyboardremove
    """
    remove_keyboard: bool
    selective: bool = None


class ForceReply(BaseModel):
    """Upon receiving a message with this model, Telegram clients will display a reply
    interface to the user (act as if the user has selected the bot's message and tapped 'Reply').
    This can be extremely useful if you want to create user-friendly step-by-step interfaces
    without having to sacrifice privacy mode.

    See here: https://core.telegram.org/bots/api#forcereply
    """
    force_reply: bool
    input_field_placeholder: bool = None
    selective: bool = None


class InlineKeyboardButton(BaseModel):
    """This model represents one button of an inline keyboard.

    See here: https://core.telegram.org/bots/api#inlinekeyboardbutton
    """

    text: str
    url: str = None
    callback_data: str = None
    web_app: dict[str, AnyHttpUrl] = None
    login_url: dict[str, Union[str, bool]] = None
    switch_inline_query: str = None
    switch_inline_query_current_chat: str = None
    switch_inline_query_chosen_chat: dict[str, Union[str, bool]] = None
    callback_game: Any = None
    pay: bool = None


class InlineKeyboardMarkup(BaseModel):
    """This model represents an inline keyboard that appears right next to the message it belongs to.

    See here: https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """

    inline_keyboard: list[list[InlineKeyboardButton]]


class Invoice(BaseModel):
    """This model contains basic information about an invoice

    See here: https://core.telegram.org/bots/api#invoice
    """

    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class SuccessfulPayment(BaseModel):
    """This model contains basic information about a successful payment.

    See here: https://core.telegram.org/bots/api#successfulpayment
    """

    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: str = None
    order_info: OrderInfo = None
    telegram_payment_charge_id: str = None
    provider_payment_charge_id: str = None


class OrderInfo(BaseModel):
    """This model represents information about an order.

    See here: https://core.telegram.org/bots/api#orderinfo
    """

    name: str = None
    phone_number: str = None
    email: str = None
    shipping_address: ShippingAddress = None


class ShippingAddress(BaseModel):
    """This model represents a shipping address.

    See here: https://core.telegram.org/bots/api#shippingaddress
    """

    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class Message(BaseModel):
    """This model represents a message.

    See here: https://core.telegram.org/bots/api#message
    """

    message_id: int
    message_thread_id: int = None
    from_: User = Field(default=None, alias='from')
    sender_chat: Chat = None
    date: int
    chat: Chat
    forward_from: User = None
    forward_from_chat: Chat = None
    forward_from_message_id: int = None
    forward_signature: str = None
    forward_sender_name: str = None
    forward_date: int = None
    is_topic_message: dict[str, Any] = None
    is_automatic_forward: bool = None
    reply_to_message: 'Message' = None
    via_bot: User = None
    edit_date: int = None
    has_protected_content: bool = None
    media_group_id: str = None
    author_signature: str = None
    text: str = None
    entities: list[MessageEntity] = None
    animation: dict[str, Any] = None
    audio: dict[str, Any] = None
    document: dict[str, Any] = None
    photo: list[dict[str, Any]] = None
    sticker: dict[str, Any] = None
    video: dict[str, Any] = None
    video_note: dict[str, Any] = None
    voice: dict[str, Any] = None
    caption: str = None
    caption_entities: list[MessageEntity] = None
    has_media_spoiler: bool = None
    contact: dict[str, Any] = None
    dice: dict[str, Any] = None
    game: dict[str, Any] = None
    poll: dict[str, Any] = None
    venue: dict[str, Any] = None
    location: dict[str, Any] = None
    new_chat_members: list[User] = None
    left_chat_member: User = None
    new_chat_title: str = None
    new_chat_photo: list[dict[str, Any]] = None
    delete_chat_photo: bool = None
    group_chat_created: bool = None
    supergroup_chat_created: bool = None
    channel_chat_created: bool = None
    message_auto_delete_timer_changed: list[dict[str, Any]] = None
    migrate_to_chat_id: int = None
    migrate_from_chat_id: int = None
    pinned_message: 'Message' = None
    invoice: Invoice = None
    successful_payment: SuccessfulPayment = None
    user_shared: dict[str, Any] = None
    chat_shared: dict[str, Any] = None
    connected_website: str = None
    write_access_allowed: dict[str, Any] = None
    passport_data: dict[str, Any] = None
    proximity_alert_triggered: dict[str, Any] = None
    forum_topic_created: dict[str, Any] = None
    forum_topic_edited: dict[str, Any] = None
    forum_topic_closed: dict[str, Any] = None
    forum_topic_reopened: dict[str, Any] = None
    general_forum_topic_hidden: dict[str, Any] = None
    general_forum_topic_unhidden: dict[str, Any] = None
    video_chat_scheduled: dict[str, Any] = None
    video_chat_started: dict[str, Any] = None
    video_chat_ended: dict[str, Any] = None
    video_chat_participants_invited: dict[str, Any] = None
    web_app_data: dict[str, Any] = None
    reply_markup: InlineKeyboardMarkup = None


class MessageEntity(BaseModel):
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


class Update(BaseModel):
    """This model represents an incoming update.
    At most one of the optional parameters can be present in any given update.

    See here: https://core.telegram.org/bots/api#update
    """

    update_id: int
    message: Message = None
    edited_message: Message = None
    edited_channel_post: Message = None
    inline_query: InlineQuery = None
    chosen_inline_result: ChosenInlineResult = None
    callback_query: CallbackQuery = None
    shipping_query: ShippingQuery = None
    pre_checkout_query: PreCheckoutQuery = None
    poll: Poll = None
    poll_answer: PollAnswer = None
    my_chat_member: ChatMemberUpdated = None
    chat_member: ChatMemberUpdated = None
    chat_join_request: ChatJoinRequest = None


class InlineQuery(BaseModel):
    """This model represents an incoming inline query.
    When the user sends an empty query, your bot could return some default or trending results.

    See here: https://core.telegram.org/bots/api#inlinequery
    """

    id: str
    from_: User = Field(alias='from')
    query: str = Field(max_length=256)
    offset: str
    chat_type: str = None
    location: Location = None


class Location(BaseModel):
    """This model represents a point on the map.

    See here: https://core.telegram.org/bots/api#location
    """

    longitude: float
    latitude: float
    horizontal_accuracy: float = Field(default=None, ge=0, le=1500)
    live_period: int = None
    heading: int = Field(default=None, ge=1, le=360)
    proximity_alert_radius: int = None


class ChosenInlineResult(BaseModel):
    """Represents a result of an inline query that was chosen by the user and sent to their chat partner.

    See here: https://core.telegram.org/bots/api#choseninlineresult
    """

    result_id: int
    from_: User = Field(alias='from')
    location: Location = None
    inline_message_id: str = None
    query: str = None


class CallbackQuery(BaseModel):
    """This model represents an incoming callback query from a callback button in an inline keyboard.
    If the button that originated the query was attached to a message sent by the bot,
    the field message will be present. If the button was attached to a message sent via the bot (in inline mode),
    the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.

    See here: https://core.telegram.org/bots/api#callbackquery
    """

    id: str
    from_: User = Field(alias='from')
    message: Message = None
    inline_message_id: str = None
    chat_instance: str = None
    data: str = None
    game_short_name: str = None


class ShippingQuery(BaseModel):
    """This model contains information about an incoming shipping query.

    See here: https://core.telegram.org/bots/api#shippingquery
    """

    id: str = None
    from_: User = Field(alias='from')
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQuery(BaseModel):
    """This model contains information about an incoming pre-checkout query.

    See here: https://core.telegram.org/bots/api#precheckoutquery
    """

    id: str
    from_: User = Field(alias='from')
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: str = None
    order_info: OrderInfo = None


class Poll(BaseModel):
    """This model contains information about a poll.

    See here: https://core.telegram.org/bots/api#poll
    """

    id: str
    question: str
    options: list[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: int = None
    explanation: str = None
    explanation_entities: list[MessageEntity] = None
    open_period: int = None
    close_date: int = None


class PollOption(BaseModel):
    """This model contains information about one answer option in a poll.

    See here: https://core.telegram.org/bots/api#polloption
    """

    text: str = Field(min_length=1, max_length=100)
    voter_count: int = Field(ge=0)


class PollAnswer(BaseModel):
    """This model represents an answer of a user in a non-anonymous poll.

    See here: https://core.telegram.org/bots/api#pollanswer
    """

    poll_id: str
    user: User
    option_ids: list[Union[int, None]]


class ChatMemberUpdated(BaseModel):
    """This model represents changes in the status of a chat member.

    See here: https://core.telegram.org/bots/api#chatmemberupdated
    """

    chat: Chat
    from_: User = Field(alias='from')
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: ChatInviteLink = None
    via_chat_folder_invite_link: bool = None


class ChatInviteLink(BaseModel):
    """Represents an invite link for a chat.

    See here: https://core.telegram.org/bots/api#chatinvitelink
    """

    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: str = None
    expire_date: int = None
    member_limit: int = None
    pending_join_request_count: int = None


class ChatJoinRequest(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatjoinrequest
    """

    chat: Chat
    from_: User = Field(alias='from')
    user_chat_id: int
    date: int
    bio: str = None
    invite_link: ChatInviteLink = None


class ChatMemberOwner(BaseModel):
    """Represents a chat member that owns the chat and has all administrator privileges.

    See here: https://core.telegram.org/bots/api#chatmemberowner
    """

    status: str
    user: User
    is_anonymous: bool
    custom_title: str = None


class ChatMemberAdministrator(BaseModel):
    """Represents a chat member that has some additional privileges.

    See here: https://core.telegram.org/bots/api#chatmemberadministrator
    """

    status: str
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: bool = None
    can_edit_messages: bool = None
    can_pin_messages: bool = None
    can_manage_topics: bool = None
    custom_title: str = None


class ChatMemberMember(BaseModel):
    """Represents a chat member that has no additional privileges or restrictions.

    See here: https://core.telegram.org/bots/api#chatmembermember
    """

    status: str
    user: User


class ChatMemberRestricted(BaseModel):
    """Represents a chat member that is under certain restrictions in the chat. Supergroups only.

    See here: https://core.telegram.org/bots/api#chatmemberrestricted
    """

    status: str
    user: User
    is_member: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: int


class ChatMemberLeft(BaseModel):
    """Represents a chat member that isn't currently a member of the chat, but may join it themselves.

    See here: https://core.telegram.org/bots/api#chatmemberleft
    """

    status: str
    user: User


class ChatMemberBanned(BaseModel):
    """Represents a chat member that was banned in the chat and can't return to the chat or view chat messages.

    See here: https://core.telegram.org/bots/api#chatmemberbanned
    """

    status: str
    user: User
    until_date: int


ChatMember = TypeVar(
    'ChatMember',
    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
    ChatMemberLeft,
    ChatMemberBanned
)


class MessageReplyMarkup(BaseModel):
    message_reply_markup: Union[Message, bool]


class TgHTTPStatusError(httpx._exceptions.HTTPStatusError):
    pass


class TgRuntimeError(RuntimeError):
    pass
