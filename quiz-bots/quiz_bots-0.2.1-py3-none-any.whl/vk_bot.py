from typing import List, Optional

import vk_api
from vk_api.keyboard import VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll

from quiz_bots import settings
from quiz_bots.bots_helpers import (
    BotKeyboardButton,
    make_keyboard_of_vk,
    send_message_to_vk_chat,
)
from quiz_bots.quiz_helpers import get_clean_text_of_answer
from quiz_bots.redis_utils import (
    get_answer_to_last_question_of_user,
    get_last_asked_question_from_redis,
    get_random_question,
    save_last_asked_question_to_redis,
)

BUTTON_NEW_QUESTION = BotKeyboardButton(text='Новый вопрос', color=VkKeyboardColor.PRIMARY)
BUTTON_GIVE_IN = BotKeyboardButton(text='Сдаться', color=VkKeyboardColor.NEGATIVE)
BUTTON_SCORE = BotKeyboardButton(text='Мой счет', color=VkKeyboardColor.POSITIVE)
BUTTON_QUESTION_IS_MADE_INCORRECTLY = BotKeyboardButton(text='Вопрос составлен неверно', color=VkKeyboardColor.DEFAULT)


def handle_new_question_request(vk, event, redis_client, button_give_in_flag: float = False) -> None:
    """Sends a random question to the user."""
    question = get_random_question(redis_client)
    user_id = event.user_id

    if button_give_in_flag:
        top_buttons = [BUTTON_GIVE_IN, BUTTON_SCORE]
        bottom_buttons: Optional[List[BotKeyboardButton]] = [BUTTON_QUESTION_IS_MADE_INCORRECTLY]
    else:
        top_buttons = [BUTTON_GIVE_IN, BUTTON_SCORE]
        bottom_buttons = None

    send_message_to_vk_chat(
        vk_session=vk,
        user_id=user_id,
        custom_keyboard=make_keyboard_of_vk(
            top_buttons=top_buttons,
            bottom_buttons=bottom_buttons,
        ),
        message_text=question.replace('\n', ' '),
    )

    save_last_asked_question_to_redis(
        question=question,
        user_id=user_id,
        redis_client=redis_client,
        social_network='vk',
    )


def handle_solution_attempt(vk, event, redis_client) -> None:
    """Checks answer of user."""
    user_id = event.user_id
    last_asked_question = get_last_asked_question_from_redis(
        redis_client=redis_client,
        user_id=user_id,
        social_network='vk',
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_client=redis_client,
        last_asked_question=last_asked_question,
    )
    if event.text.lower() == get_clean_text_of_answer(answer_to_last_question_of_user):
        top_buttons = [BUTTON_NEW_QUESTION]
        message_text = 'Правильно! Для следующего вопроса нажми «Новый вопрос»'
    else:
        top_buttons = [BUTTON_GIVE_IN, BUTTON_SCORE]
        message_text = 'Неправильно... Попробуешь ещё раз?'

    send_message_to_vk_chat(
        vk_session=vk,
        user_id=user_id,
        custom_keyboard=make_keyboard_of_vk(
            top_buttons=top_buttons,
            bottom_buttons=None,
        ),
        message_text=message_text,
    )


def handle_opportunity_to_give_in(vk, event, redis_client) -> None:
    """Handles clicking the "Surrender" button.

    The bot sends the user an answer to the question
    and sends the next question with the next message.
    """
    user_id = event.user_id
    last_asked_question = get_last_asked_question_from_redis(
        redis_client=redis_client,
        user_id=user_id,
        social_network='vk',
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_client=redis_client,
        last_asked_question=last_asked_question,
    )
    send_message_to_vk_chat(
        vk_session=vk,
        user_id=user_id,
        message_text=answer_to_last_question_of_user,
    )
    handle_new_question_request(vk, event, redis_client, button_give_in_flag=True)


def handler_question_is_incorrect(vk, event) -> None:
    """Handles clicking the button 'The question is incorrect'."""
    send_message_to_vk_chat(
        vk_session=vk,
        user_id=event.user_id,
        custom_keyboard=make_keyboard_of_vk(
            top_buttons=[BUTTON_GIVE_IN, BUTTON_SCORE],
            bottom_buttons=None,
        ),
        message_text='Спасибо за фидбек! Ждем ответ на предыдущий вопрос!',
    )


def start_vk_bot(args, redis_client):  # noqa: WPS210, WPS231
    """Launch the VK bot."""
    vk_group_token = settings.vk_group_token
    vk_session = vk_api.VkApi(token=vk_group_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос':
                handle_new_question_request(vk, event, redis_client)
            elif event.text == 'Сдаться':
                handle_opportunity_to_give_in(vk, event, redis_client)
            elif event.text == 'Вопрос составлен неверно':
                handler_question_is_incorrect(vk, event)
            else:
                handle_solution_attempt(vk, event, redis_client)
