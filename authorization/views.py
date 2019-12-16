import os
import secrets

from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from base import view_utils

def create(request):
    if request.method == 'GET':
        return render(request, 'authorization/create.html')

    if request.method == 'POST':
        username = request.POST.get('username')

        if not username:
            raise Exception('Not implemented')

        password = request.POST.get('password')

        if password:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect(reverse('home'))

            else:
                hidden_password = request.POST.get('hidden-password')
                return render(
                    request,
                    'authorization/create.html',
                    {
                        'username': username,
                        'password': hidden_password,
                    },
                )

        password = ' '.join(
            secrets.choice(settings.PASSWORD_WORD_LIST)
            for ignore in range(5)
        )

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
            )

        except IntegrityError as e:
            return render(
                request,
                'authorization/create.html',
                {
                    'uniqueness_error': True,
                }
            )

        return render(
            request,
            'authorization/create.html',
            {
                'username': username,
                'password': password,
            },
        )

    raise Exception('Not implemented')

@view_utils.require_auth
def delete(request):
    if request.method == 'GET':
        return render(request, 'authorization/delete_form.html')

    if request.method == 'POST':
        confirm_delete = request.POST.get('confirm-delete')

        if not confirm_delete:
            return render(
                request,
                'authorization/delete_form.html',
                {
                    'checkbox_not_checked_error': True,
                },
            )

        user = request.user
        logout(request)
        user.delete()
        return redirect(reverse('home'))

    raise Exception('Not implemented')

def log_in(request):
    if request.method == 'GET':
        redirect_uri = request.GET.get('redirect')

        return render(
            request,
            'authorization/login.html',
            {
                'redirect': redirect,
            },
        )

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirect_uri = request.POST.get('redirect')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if not redirect_uri:
                redirect_uri = reverse('home')

            return redirect(redirect_uri)

        return render(
            request,
            'authorization/login.html',
            {
                'redirect': redirect,
                'incorrect_username_or_password_error': True,
            },
        )

    raise Exception('Not implemented')

def log_out(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse('home'))

    raise Exception('Not implemented')
