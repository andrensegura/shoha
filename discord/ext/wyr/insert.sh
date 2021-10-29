#!/bin/bash

while read p; do
	PROMPT=`echo $p | cut -d';' -f1`
	SFW=`echo $p | cut -d';' -f2`
	sqlite3 wyrdb "insert into prompts (prompt, sfw) values (\"$PROMPT\", $SFW);"
done < wyr.txt
