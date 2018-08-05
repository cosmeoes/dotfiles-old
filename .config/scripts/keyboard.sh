layout=$(setxkbmap -query | grep "layout:     " | sed 's|layout:     ||g')
if [ $layout = "us" ]; then 
   setxkbmap latam
   notify-send Keyboard latam -t 1000
else
   setxkbmap us
   notify-send Keyboard us -t 1000
fi

