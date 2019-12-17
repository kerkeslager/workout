from django.shortcuts import render

def profile(request):
    user = request.user

    user_exercises = [
        {
            'exercise': exercise,
            'most_recent_record': exercise.most_recent_exercise_record_for_user(user),
            'personal_best_record': exercise.personal_best_record_for_user(user),
        }
        for exercise in user.profile.exercises
    ]

    user_workout_records = [
        workout_record
        for workout_record in user.workout_records.filter(is_finished=True).order_by('-created')
    ]

    return render(
        request,
        'user/profile.html',
        {
            'user': user,
            'user_exercises': user_exercises,
            'user_workout_records': user_workout_records,
        },
    )

def settings(request):
    return render(request, 'user/settings.html')
