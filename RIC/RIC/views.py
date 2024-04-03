from django.shortcuts import redirect
from msal import PublicClientApplication
from msal.contrib.django.auth import (
    MSALAuthenticator,
    login_required,
    logout,
)

# MSAL_INSTANCE = PublicClientApplication(MSAL_AUTH['CLIENT_ID'], authority=MSAL_AUTH['AUTHORITY'], )

# @login_required
# def microsoft_login(request):
#     # Get user data from Microsoft Graph API
#     graph_data = MSALAuthenticator(MSAL_INSTANCE, request).get('graph/me')
#     # Store the user data in the Django session
#     request.session['user_data'] = graph_data
#     return redirect('home:home')
