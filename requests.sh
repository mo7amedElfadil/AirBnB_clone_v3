#!/usr/bin/env bash
WHT='\e[0m' # No Color
RED='\e[0;31m'
GRN='\e[0;32m'
YLW='\e[1;33m'
BLU='\e[0;34m'

Run the server
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app > /dev/null 2>&1 &
echo $! > api.pid

sleep 2;

Run the tests

echo -e "${BLU}________________________________________________________${WHT}"
echo -e "${BLU}_____________________INFO____________________________${WHT}"
echo -e "${BLU}GET /api/v1/status${WHT}"
STATUS=$(curl -sX GET http://0.0.0.0:5000/api/v1/status)
echo -e "${YLW}${STATUS}${WHT}"
echo -e "\n"

echo -e "${BLU}GET /api/v1/stats${WHT}"
STATS=$(curl -sX GET http://0.0.0.0:5000/api/v1/stats)
echo -e "${YLW}${STATS}${WHT}"
echo -e "\n"

echo -e "${BLU}GET /api/v1/nop${WHT}"
NOP=$(curl -sX GET http://0.0.0.0:5000/api/v1/nop)
echo -e "${YLW}${NOP}${WHT}"
echo -e "\n"


echo -e "${BLU}________________________________________________________${WHT}"
echo -e "${BLU}_____________________STATES____________________________${WHT}"

echo -e "${GRN}GET /api/v1/states${WHT}"
STATES=$(curl -sX GET http://0.0.0.0:5000/api/v1/states/)
echo -e "${YLW}${STATES}${WHT}"
echo -e "\n"

STATE_ID=$(echo "$STATES" | grep -o '"id":"[^"]*' |  head -n1 | cut -d'"' -f4)
echo -e "${GRN}GET /api/v1/states/${STATE_ID}${WHT}"
STATE=$(curl -sX GET http://0.0.0.0:5000/api/v1/states/"${STATE_ID}")
echo -e "${YLW}${STATE}${WHT}"
echo -e "\n"

echo -e "${GRN}POST /api/v1/states${WHT}"
POST_STATE=$(curl -sX POST http://0.0.0.0:5000/api/v1/states/ -H "Content-Type: application/json" -d '{"name": "California"}' -vvv)
echo -e "${YLW}${POST_STATE}${WHT}"
echo -e "\n"

echo -e "${GRN}GET /api/v1/states/NotAValidID${WHT}"
STATE=$(curl -sX GET http://0.0.0.0:5000/api/v1/states/NotAValidID -H "Content-Type: application/json" -d '{"name": "California"}' -vvv)
echo -e "${RED}${STATE}${WHT}"
echo -e "\n"

STATE_ID_NEW=$(echo "$POST_STATE" | grep -o '"id":"[^"]*' |  tail -n1 | cut -d'"' -f4)
echo -e "${GRN}PUT /api/v1/states/${STATE_ID_NEW}${WHT}"
PUT_STATE=$(curl -sX PUT http://0.0.0.0:5000/api/v1/states/"${STATE_ID_NEW}" -H "Content-Type: application/json" -d '{"name": "California is so cool"}')
echo -e "${YLW}${PUT_STATE}${WHT}"
echo -e "\n"

echo -e "${GRN}PUT /api/v1/states/${STATE_ID_NEW}\nNotAValidJSON${WHT}"
PUT_STATE=$(curl -sX PUT http://0.0.0.0:5000/api/v1/states/"${STATE_ID_NEW}" -H "Content-Type: application/json" -d '{"name"}')
echo -e "${RED}${PUT_STATE}${WHT}"
echo -e "\n"

echo -e "${GRN}DELETE /api/v1/states/${STATE_ID_NEW}${WHT}"
DELETE_STATE=$(curl -sX DELETE http://0.0.0.0:5000/api/v1/states/"${STATE_ID_NEW}")
echo -e "${YLW}${DELETE_STATE}${WHT}"
echo -e "\n"
echo -e "${GRN}GET /api/v1/states/${STATE_ID}\nConfirm Delete. Expect Not Found${WHT}"
STATE=$(curl -sX GET http://0.0.0.0:5000/api/v1/states/"${STATE_ID_NEW}")
echo -e "${GRN}${STATE}${WHT}"
echo -e "\n"


kill the server	
kill -9 `cat api.pid` > /dev/null 2>&1;
rm api.pid;
sleep 2;
