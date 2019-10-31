#!/bin/bash
until python -m scrolls_bot >/dev/null; do
    sleep 5
done
