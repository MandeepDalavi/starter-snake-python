import os
import random

import cherrypy

import server_logic

class Battlesnake(object):
    """
    This is a simple Battlesnake server written in Python using the CherryPy Web Framework.
    For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
    """

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        """
        This function is called when you register your Battlesnake on play.battlesnake.com
        See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake

        It controls your Battlesnake appearance and author permissions.
        For customization options, see https://docs.battlesnake.com/references/personalization
        
        TIP: If you open your Battlesnake URL in browser you should see this data.

        """
        return {
            "apiversion": "1",
            "tags": ["python", "starter-project"],  # Optional informational tags to describe your Battlesnake
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#888888",  # TODO: Personalize
            "head": "default",  # TODO: Personalize
            "tail": "default",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        """
        This function is called everytime your snake is entered into a game.
        cherrypy.request.json contains information about the game that's about to be played.
        """
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        """
        This function is called on every turn of a game. It's how your snake decides where to move.
        Valid moves are "up", "down", "left", or "right".
        
        Use the information in 'data' to decide your next move. The 'data' variable can be interacted
        with as a Python Dictionary, and contains all of the information about the Battlesnake board 
        for each move of the game.

        For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request
        """
        data = cherrypy.request.json
        my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
        my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

        # TODO: uncomment the lines below so you can see what this data looks like in your output!
        # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
        # print(f"All board data this turn: {data}")        
        # print(f"My Battlesnakes head this turn is: {my_head}")
        # print(f"My Battlesnakes body this turn is: {my_body}")

        possible_moves = ["up", "down", "left", "right"]

        # Don't allow your Battlesnake to move back in on it's own neck
        possible_moves = server_logic.avoid_my_neck(my_head, my_body, possible_moves)

        # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
        # board_height = ?
        # board_width = ?

        # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

        # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

        # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

        # Choose a random direction from the remaining possible_moves to move in, and then return that move
        move = random.choice(possible_moves)
        print(f"CHOOSING MOVE: {move} from all valid options in {possible_moves}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        """
        This function is called when a game your snake was in ends.
        It's purely for informational purposes, you don't have to make any decisions here.
        """
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
