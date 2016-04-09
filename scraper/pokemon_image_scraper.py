#!/usr/bin/env python3
import sys
import os
import requests

from urllib import request

def main():
    l_bound = int(sys.argv[1])
    u_bound = int(sys.argv[2])

    # for i in range(l_bound, u_bound + 1):
    #     try: 
    #         request.urlretrieve("http://veekun.com/dex/media/pokemon/main-sprites/omegaruby-alphasapphire/" + str(i) + ".png", "pk_image/" + str(i) + ".png")
    #     except:
    #         print("Failed: " + str(i))

    #     try:
    #         request.urlretrieve("http://veekun.com/dex/media/pokemon/main-sprites/omegaruby-alphasapphire/" + str(i) + "-mega.png", "pk_image/" + str(i) + "-mega.png")
    #     except:
    #         pass

    m_l_bound = int(sys.argv[3])
    m_u_bound = int(sys.argv[4])

    for i in range(m_l_bound, m_u_bound + 1):
        try:
            print("Starting: " + str(i))
            pre_evolution_url = requests.get("http://pokeapi.co/api/v2/pokemon/" + str(i)).json()["species"]["url"]
            pre_evolution_pokemon_id = requests.get(pre_evolution_url).json()["id"]
            os.rename("pk_image/" + str(pre_evolution_pokemon_id) + "-mega.png", "pk_image/" + str(i) + ".png")
            print("Finished: " + str(i))
        except Exception as e:
            print("Failed: " + str(i))
            print("Error: " + str(e))


if __name__ == "__main__":
    main()