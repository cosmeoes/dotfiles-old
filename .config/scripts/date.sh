#!/bin/bash
IFS='#' read -r -a array <<< "$(date '+%d/%b/%y#%l:%M %p')"
echo " ${array[0]}   ${array[1]}"

