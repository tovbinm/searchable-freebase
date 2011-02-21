'''
Created on Feb 20, 2011

@author: matthew
'''

class _gamesRelationsMapper(object):
 
    def __init__(self):
        self.relations = {'game': {'designer':'game_designer', 
                                   'expansions':'game_expansion', 
                                   'genre':'game_genre',
                                   'publisher':'game_publisher',
                                   'name': 'game'},
                          
                          'game_designer': {'games_designed':'game'},
                          
                          'game_expansion': {'standalone':'game'},
                          
                          'game_genre':{'boardgames':'game'},
                          
                          'game_publisher': {'games_published':'game'},
                          
                          'playing_card_game': {'deck_type':'playing_card_deck_type',
                                                'play_direction':'playing_card_game_play_direction'},
                          
                          'playing_card_game_play_direction' : {'card_games':'playing_card_game'},
                          
                          'playing_card_deck_type' : {'card_games':'playing_card_game'}
                          }
        
       
        