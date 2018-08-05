#
# ~/.bashrc
#
[[ $- != *i* ]] && return

colors() {
	local fgc bgc vals seq0

	printf "Color escapes are %s\n" '\e[${value};...;${value}m'
	printf "Values 30..37 are \e[33mforeground colors\e[m\n"
	printf "Values 40..47 are \e[43mbackground colors\e[m\n"
	printf "Value  1 gives a  \e[1mbold-faced look\e[m\n\n"

	# foreground colors
	for fgc in {30..37}; do
		# background colors
		for bgc in {40..47}; do
			fgc=${fgc#37} # white
			bgc=${bgc#40} # black

			vals="${fgc:+$fgc;}${bgc}"
			vals=${vals%%;}

			seq0="${vals:+\e[${vals}m}"
			printf "  %-9s" "${seq0:-(default)}"
			printf " ${seq0}TEXT\e[m"
			printf " \e[${vals:+${vals+$vals;}}1mBOLD\e[m"
		done
		echo; echo
	done
}
source /usr/share/git/completion/git-prompt.sh
[[ -f ~/.extend.bashrc ]] && . ~/.extend.bashrc

#python ~/.config/scripts/bash_start_quote.py
alias fucking='sudo'
alias mount='sudo mount'
alias umount='sudo umount'
alias mountwin='sudo mount /dev/sda3 /mnt/windows'
alias umountwin='sudo umount /mnt/windows'
alias mountusb='sudo mount /dev/sdb1 /mnt/usb -o umask=000'
alias umountusb='sudo umount /mnt/usb'
alias music='ncmpcpp'
export HISTCONTROL=ignoredups
