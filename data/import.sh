#!/bin/bash

CMD=../manage.py

$CMD import -f eur2usd/*.dat -p EUR/USD -l debug ;
$CMD import -f eur2chf/*.dat -p EUR/CHF -l debug ;
$CMD import -f usd2chf/*.dat -p USD/CHF -l debug ;
