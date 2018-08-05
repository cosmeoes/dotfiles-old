mpcout=$(mpc $1)
IFS="\n" read -ra song <<< "$mpcout"
echo "${song[@]}"
notify-send "music" "${song[@]}"
