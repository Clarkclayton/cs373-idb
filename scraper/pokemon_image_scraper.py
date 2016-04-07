#!/usr/bin/env python3
import sys
from urllib import request

def main():
    l_bound = int(sys.argv[1])
    u_bound = int(sys.argv[2])

    for i in range(l_bound, u_bound + 1):
        try: 
            request.urlretrieve("http://veekun.com/dex/media/pokemon/main-sprites/omegaruby-alphasapphire/" + str(i) + ".png", "pk_image/" + str(i) + ".png")
        except:
            print("Failed: " + str(i))

        try:
            request.urlretrieve("http://veekun.com/dex/media/pokemon/main-sprites/omegaruby-alphasapphire/" + str(i) + "-mega.png", "pk_image/" + str(i) + "-mega.png")
        except:
            pass

if __name__ == "__main__":
    main()