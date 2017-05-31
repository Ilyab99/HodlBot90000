#!/bin/sh

while true; do
  nohup python text-requests.py >> test.out
done &
