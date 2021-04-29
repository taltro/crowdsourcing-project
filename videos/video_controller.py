from .models import Video, Tagging, UserRating, TaggingValidator, UserRatingValidator, Comment
from typing import List


def get_all_videos():
    return Video.objects.all()


def get_tag_by_id(tag_id):
    return Tagging.objects.get(id=tag_id)


def get_video_by_id(video_id):
    return Video.objects.get(id=video_id)


def get_all_tags_for_video(video):
    return Tagging.objects.filter(video=video).order_by('start__hour', 'start__minute', 'start__second')


def get_all_ratings_for_tag(tagging):
    return UserRating.objects.filter(tagging=tagging)


def get_user_rating_for_tag(creator, tagging):
    return UserRating.objects.filter(creator=creator, tagging=tagging)


def get_rating_by_user_and_video(user, video):
    return UserRating.objects.filter(creator=user, tagging__video=video)


def get_tags_active_for_user(user, tags):
    user_rating_for_tags = []
    for tag in tags:
        try:
            is_upvote = get_user_rating_for_tag(user, tag)[0].is_upvote
            user_rating_for_tags.append(str(is_upvote))
        except IndexError:
            user_rating_for_tags.append("None")
    return user_rating_for_tags


def remove_user_rating_for_tag(creator, tagging):
    user_rating_list = get_user_rating_for_tag(creator=creator, tagging=tagging)
    if user_rating_list:
        user_rating = user_rating_list[0]
        if user_rating.is_upvote:
            tagging.rating_value -= 1
        else:
            tagging.rating_value += 1
        tagging.save()
        user_rating.delete()


def create_tagging(video, user, start_time, end_time, description):
    errors = TaggingValidator.get_errors(creator=user, start=start_time, end=end_time, description=description,
                                         video=video)
    if errors:
        return errors
    tag = Tagging.objects.create(creator=user, start=start_time, end=end_time,
                                 description=description, video=video)
    tag.save()


def create_user_rating(creator, tagging, is_upvote):
    errors = UserRatingValidator.get_errors(creator, tagging, is_upvote)
    if errors:
        return False
    remove_user_rating_for_tag(creator, tagging)
    user_rating = UserRating(creator=creator, tagging=tagging, is_upvote=is_upvote)
    if is_upvote:
        tagging.rating_value += 1
    else:
        tagging.rating_value -= 1
    tagging.save()
    user_rating.save()
    return True


# Comments controllers

def get_all_comments_for_tag(tag) -> List[Comment]:
    return Comment.objects.filter(tag=tag)

