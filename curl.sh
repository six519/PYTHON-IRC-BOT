#!/bin/bash
curl -K  curl.conf "http://www.phpugph.com/talk/index.php?action=login2"
grep URL curl.headers | cut -f 3 -d " " | sed s/URL=//g | xargs curl -K curl.conf > mk
#the last sed is a hack on a mac
grep topicseen mk  | html2text | sed s/.//g
rm mk curl.headers curl.cookie.jar
