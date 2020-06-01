import secrets


def get_random_question(redis_client) -> str:
    """Gets a random question from the quiz content."""
    return secrets.choice(list(redis_client.hkeys('Questions')))


def save_last_asked_question_to_redis(
    question: str, user_id: int, redis_client, social_network: str,
) -> None:
    """Saves the user's question number in the database."""
    redis_client.hset('Users', f'user_{social_network}_{user_id}', question)


def get_last_asked_question_from_redis(redis_client, user_id: int, social_network: str) -> str:
    """Gets the last asked question from redis."""
    return redis_client.hget('Users', f'user_{social_network}_{user_id}')


def get_answer_to_last_question_of_user(redis_client, last_asked_question: str) -> str:
    """Gets the text of the answer to the last question asked by the user."""
    return redis_client.hget('Questions', last_asked_question)
