for i in `seq $1 $2`; do
    wget http://ggmate.me/api/games/$i
done
