#!/usr/bin/env bash

# Now this code not work now, because i encapsulate etl code in a function. Im lazy,
# i dont want to add arg parse function to etl.py
# i use to populate the database tables

for i in {1..100}
do
 python python etl.py &
done