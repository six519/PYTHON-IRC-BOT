#!/bin/bash
cmd1="`sed -e s/user=.*/user=$1/ curl.conf > curl.conf.tmp`"
cmd2="`sed -e s/passwrd=.*/passwrd=$2/ curl.conf.tmp > curl.conf.tmp1`"

curl -K  curl.conf.tmp1 "http://www.phpugph.com/talk/index.php?action=login2"
grep URL curl.headers | cut -f 3 -d " " | sed s/URL=//g | xargs curl -K curl.conf.tmp1 > mk
#the last sed is a hack on a mac
grep topicseen mk  | html2text | sed s/.//g
rm mk curl.headers curl.cookie.jar curl.conf.tmp*
