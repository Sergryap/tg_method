from pydantic import BaseModel
from typing import Dict, Union, List


class VerifyMessage(BaseModel):
    message_id: int
    message_thread_id: int = None
    from_: Dict[str, Union[str, int, bool]] = None
    sender_chat: Dict[str, Union[str, int]] = None
    date: int
    chat: Dict[str, Union[str, int]]
    forward_from: Dict[str, Union[str, int, bool]] = None
    forward_from_chat: Dict[str, Union[str, int, bool]] = None
    forward_from_message_id: int = None
    forward_signature: str = None
    forward_sender_name: str = None
    forward_date: int = None
    is_topic_message: Dict = None
    is_automatic_forward: bool = None
    reply_to_message: Dict = None
    via_bot: Dict = None
    edit_date: int = None
    has_protected_content: bool = None
    media_group_id: str = None
    author_signature: str = None
    text: str = None
    entities: List[Dict] = None
    animation: Dict = None
    audio: Dict = None
    document: Dict = None
    photo: List[Dict] = None
    sticker: Dict = None
    video: Dict = None
    video_note: Dict = None
    voice: Dict = None
    caption: str = None
    caption_entities: List[Dict] = None
    has_media_spoiler: bool = None
    contact: Dict = None
    dice: Dict = None
    game: Dict = None
    poll: Dict = None
    venue: Dict = None
    location: Dict = None
    new_chat_members: List[Dict] = None
    left_chat_member: Dict = None
    new_chat_title: str = None
    new_chat_photo: List[Dict] = None
    delete_chat_photo: bool = None
    group_chat_created: bool = None
    supergroup_chat_created: bool = None
    channel_chat_created: bool = None
    message_auto_delete_timer_changed: List[Dict] = None
    migrate_to_chat_id: int = None
    migrate_from_chat_id: int = None
    pinned_message: Dict = None
    invoice: Dict = None
    successful_payment: Dict = None
    user_shared: Dict = None
    chat_shared: Dict = None
    connected_website: str = None
    write_access_allowed: Dict = None
    passport_data: Dict = None
    proximity_alert_triggered: Dict = None
    forum_topic_created: Dict = None
    forum_topic_edited: Dict = None
    forum_topic_closed: Dict = None
    forum_topic_reopened: Dict = None
    general_forum_topic_hidden: Dict = None
    general_forum_topic_unhidden: Dict = None
    video_chat_scheduled: Dict = None
    video_chat_started: Dict = None
    video_chat_ended: Dict = None
    video_chat_participants_invited: Dict = None
    web_app_data: Dict = None
    reply_markup: Dict = None

    async def clean_response(self):
        for key, value in self.dict().items():
            if value is None:
                delattr(self, key)
