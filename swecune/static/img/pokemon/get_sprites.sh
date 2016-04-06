#!/bin/bash

for id in `seq $1 $2`; do
    wget "http://pokeapi.co/media/sprites/pokemon/${id}.png" -O "pokemon_${id}.png"
done

