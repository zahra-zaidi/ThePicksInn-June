from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from django.http import JsonResponse


def get_real_top_20_players(year):
    if year == 2021:
        response = requests.get(f'https://newdjangobackend-b4845409485a.herokuapp.com/api/player_efficiency_ratings_hard_coded_{year}')
        print('Top 20 Players 2021 Status Code:', response.status_code)
        if response.status_code == 200:
            return response.json()
        return None
    elif year == 2022:
        response = requests.get(f'https://newdjangobackend-b4845409485a.herokuapp.com/api/player_efficiency_ratings_hard_coded_{year}')
        print('Top 20 Players 2022 Status Code:', response.status_code)
        if response.status_code == 200:
            return response.json()
        return None
    else:
        response = requests.get(f'https://newdjangobackend-b4845409485a.herokuapp.com/api/player_efficiency_ratings_hard_coded_{year}')
        print('Top 20 Players 2023 Status Code:', response.status_code)
        if response.status_code == 200:
            return response.json()
        return None



def get_top_20_players(year):
    response = requests.get(f'https://newdjangobackend-b4845409485a.herokuapp.com/advance-stats/{year}/')
    print('Top 20 Players Status Code:', response.status_code)
    if response.status_code == 200:
        return response.json()
    return None





def login(request):
    return render(request, 'myapp/login.html')


def get_scoutingPerformance(username='Jkern'):
    response = requests.get(f'https://newdjangobackend-b4845409485a.herokuapp.com/api/leaderboard/{username}/')
    print('Scouting Performance Status Code:', response.status_code)
    if response.status_code == 200:
        return response.json()
    return None



def capitalize_words(input_string):
    # This will capitalize the first letter of each word
    return ' '.join(word.capitalize() for word in input_string.split())



@login_required
def home(request):

    year = int(request.GET.get('draftYear', 2021))
    print("Selected Year:", year)
    
    # Get data for top 20 players
    # data1 = get_top_20_players(year)
    data1 = get_real_top_20_players(year)

    # print("i am data1",data1)

    # Get username from the request.GET dictionary
    username = request.GET.get('username', 'Jkern')

    if username:
       username = capitalize_words(username)

    # Get scouting performance data for the specified username
    data2 = get_scoutingPerformance(username)
    data3 = get_leaderboard_data()
    # Check if the response is successful
    # if data1 is not None and data2 is not None:
    if data1 is not None  or data3 is not None:
        data3 = sorted(data3, key=lambda k: (k['accuracy'], k['correct_picks_count'], k['per_percentage']), reverse=True)
      
        # Pass the data to the template
        context = {'data1': data1, 'data2': data2 , 'year': year , 'data3': data3}
        return render(request, 'myapp/index.html', context)
    else:
        # Pass status codes to the template for debugging
        context = {'status_code': f'Top 20 players data and scouting performance data retrieval failed'}
        return render(request, 'myapp/index.html', context)




def api_leaderboard(request, username):
    # Your logic to fetch data based on username
    if username:
       username = capitalize_words(username)
    data = get_scoutingPerformance(username)  # This should return JSON-friendly data

    print("i am data",data)
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Data not found'}, status=404)
    


def get_leaderboard_data():
    response = requests.get('https://newdjangobackend-b4845409485a.herokuapp.com/api/leaderboard-list/')
    print('Leaderboard Data Status Code:', response.status_code)
    if response.status_code == 200:
        return response.json()
    return None


@login_required
@api_view(['GET'])
def leaderboard(request):
    # Get data for leaderboard
    data2 = get_leaderboard_data()

    # Check if the response is successful
    if data2 is not None:
        # Sort the data2 by 'accuracy', 'correct_picks_count', and 'per_percentage'
        data2 = sorted(data2, key=lambda k: (k['accuracy'], k['correct_picks_count'], k['per_percentage']), reverse=True)

        # Pass the data to the template
        context = {'data2': data2}
        return render(request, 'myapp/leaderboard.html', context)
    else:
        # Pass status codes to the template for debugging
        context = {'status_code': f'Leaderboard data retrieval failed'}
        return render(request, 'myapp/leaderboard.html', context)




# def scoutingPerfomance(request):
    # url https://newdjangobackend-b4845409485a.herokuapp.com/api/leaderboard/Jkern/
    # return render(request, 'myapp/scoutingPerfomance.html')


# @login_required
# @api_view(['GET'])
# def top_20_players(request):
#     # Get data for top 20 players
#     data1 = get_top_20_players()

#     # Check if the response is successful
#     if data1 is not None:
#         # Pass the data to the template
#         context = {'data1': data1}
#         return render(request, 'myapp/index.html', context)
#     else:
#         # Pass status codes to the template for debugging
#         context = {'status_code': f'Top 20 players data retrieval failed'}
#         return render(request, 'myapp/index.html', context)


# for the scouting performance (not fully implemented)
# @login_required
# @api_view(['GET'])
# def player_efficiency_ratings(request, username):
#     # Construct the URL with the provided username
#     url = f'https://mybackendnba-e0bd8ae9accb.herokuapp.com/api/player_efficiency_ratings/{username}/'

#     # Make a request to the API
#     response = requests.get(url)

#     # Check the status code and process the data accordingly
#     if response.status_code == 200:
#         data = response.json()

#         # Pass the data to the template
#         context = {'data': data}
#         return render(request, 'myapp/player_efficiency_ratings.html', context)
#     else:
#         # Pass status codes to the template for debugging
#         context = {'status_code': f'Player efficiency ratings data retrieval failed'}
#         return render(request, 'myapp/player_efficiency_ratings.html', context)