from .models import Video, Tagging, UserRating, TaggingValidator, UserRatingValidator


def get_all_videos():
    return Video.objects.all()


def get_tag_by_id(tag_id):
    return Tagging.objects.filter(id=tag_id)


def get_video_by_id(video_id):
    return Video.objects.get(id=video_id)


def get_all_tags_for_video(video):
    return Tagging.objects.filter(video=video).order_by('start__hour', 'start__minute', 'start__second')


def get_all_ratings_for_tagging(tagging):
    return UserRating.objects.filter(tagging=tagging)


def get_user_rating_for_tagging(creator, tagging):
    return UserRating.objects.filter(creator=creator, tagging=tagging)


def remove_user_rating_for_tagging(creator, tagging):
    user_rating_list = get_user_rating_for_tagging(creator=creator, tagging=tagging)
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
        return errors
    remove_user_rating_for_tagging(creator, tagging)
    user_rating = UserRating(creator=creator, tagging=tagging, is_upvote=is_upvote)
    if is_upvote:
        tagging.rating_value += 1
    else:
        tagging.rating_value -= 1
    tagging.save()
    user_rating.save()
