#!/usr/bin/env bash
WHT='\e[0m' # No Color
RED='\e[0;31m'
GRN='\e[0;32m'
YLW='\e[1;33m'
BLU='\e[0;34m'
# kill the server	

# Run the server
# run;
PORT=5000
HOST="http://0.0.0.0:$PORT/api/v1"




function run {
	echo "${BLU}---------------------Running server-----------------------${WHT}"
	HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=$PORT python3 -m api.v1.app > /dev/null 2>&1 &
	echo $! > api.pid
	sleep 2;
}

function cleanup {
	echo "${BLU}---------------------Killing Server-----------------------${WHT}"
	kill -9 `cat api.pid` > /dev/null 2>&1;
	rm api.pid;
	exit 0;
}

# Run the tests

function info {

	echo -e "${BLU}________________________________________________________${WHT}"
	echo -e "${BLU}_____________________INFO____________________________${WHT}"
	echo -e "${BLU}GET /api/v1/status${WHT}"
	STATUS=$(curl -sX GET $HOST/status)
	echo -e "${YLW}${STATUS}${WHT}"
	echo -e "\n"

	echo -e "${BLU}GET /api/v1/stats${WHT}"
	STATS=$(curl -sX GET $HOST/stats)
	echo -e "${YLW}${STATS}${WHT}"
	echo -e "\n"

	echo -e "${BLU}GET /api/v1/nop${WHT}"
	NOP=$(curl -sX GET $HOST/nop)
	echo -e "${YLW}${NOP}${WHT}"
	echo -e "\n"
}


function states {
	echo -e "${BLU}________________________________________________________${WHT}"
	echo -e "${BLU}_____________________STATES____________________________${WHT}"

	echo -e "${GRN}GET /api/v1/states${WHT}"
	STATES=$(curl -sX GET $HOST/states/)
	echo -e "${YLW}${STATES}${WHT}"
	echo -e "\n"

	STATE_ID=$(echo "$STATES" | grep -o '"id":"[^"]*' |  head -n1 | cut -d'"' -f4)
	echo -e "${GRN}GET /api/v1/states/${STATE_ID}${WHT}"
	STATE=$(curl -sX GET $HOST/states/"${STATE_ID}")
	echo -e "${YLW}${STATE}${WHT}"
	echo -e "\n"

	echo -e "${GRN}POST /api/v1/states${WHT}"
	POST_STATE=$(curl -sX POST $HOST/states/ -H "Content-Type: application/json" -d '{"name": "California"}' -vvv)
	echo -e "${YLW}${POST_STATE}${WHT}"
	echo -e "\n"
	
	# missing name
	echo -e "${GRN}POST /api/v1/states\nMissingName${WHT}"
	POST_STATE_NOT_NAME=$(curl -sX POST $HOST/states/ -H "Content-Type: application/json" -d '{"Location": "State"}' -vvv)
	echo -e "${RED}${POST_STATE_NOT_NAME}${WHT}"
	echo -e "\n"

	echo -e "${GRN}GET /api/v1/states/NotAValidID${WHT}"
	STATE_NOT_ID=$(curl -sX GET $HOST/states/NotAValidID -H "Content-Type: application/json" -d '{"name": "California"}' -vvv)
	echo -e "${RED}${STATE_NOT_ID}${WHT}"
	echo -e "\n"

	STATE_ID_NEW=$(echo "$POST_STATE" | grep -o '"id":"[^"]*' |  tail -n1 | cut -d'"' -f4)
	echo -e "${GRN}PUT /api/v1/states/${STATE_ID_NEW}${WHT}"
	PUT_STATE=$(curl -sX PUT $HOST/states/"${STATE_ID_NEW}" -H "Content-Type: application/json" -d '{"name": "California is so cool"}')
	echo -e "${YLW}${PUT_STATE}${WHT}"
	echo -e "\n"

	echo -e "${GRN}PUT /api/v1/states/${STATE_ID_NEW}\nNotAValidJSON${WHT}"
	PUT_STATE=$(curl -sX PUT $HOST/states/"${STATE_ID_NEW}" -H "Content-Type: application/json" -d '{"name"}')
	echo -e "${RED}${PUT_STATE}${WHT}"
	echo -e "\n"

	echo -e "${GRN}DELETE /api/v1/states/${STATE_ID_NEW}${WHT}"
	DELETE_STATE=$(curl -sX DELETE $HOST/states/"${STATE_ID_NEW}")
	echo -e "${YLW}${DELETE_STATE}${WHT}"
	echo -e "\n"
	echo -e "${GRN}GET /api/v1/states/${STATE_ID}\nConfirm Delete. Expect Not Found${WHT}"
	STATE_NOT_FOUND=$(curl -sX GET $HOST/states/"${STATE_ID_NEW}")
	echo -e "${GRN}${STATE_NOT_FOUND}${WHT}"
	echo -e "\n"
}

function cities {
	echo -e "${BLU}________________________________________________________${WHT}"
	echo -e "${BLU}_____________________CITIES____________________________${WHT}"

	STATES=$(curl -sX GET $HOST/states/)
	STATE_ID=$(echo "$STATES" | grep -o '"id":"[^"]*' |  head -n1 | cut -d'"' -f4)
	echo -e "${GRN}GET /api/v1/states/$STATE_ID/cities${WHT}"
	CITIES=$(curl -sX GET $HOST/states/$STATE_ID/cities/)
	echo -e "${YLW}${CITIES}${WHT}"
	echo -e "\n"

	CITY_ID=$(echo "$CITIES" | grep -o '"id":"[^"]*' |  head -n1 | cut -d'"' -f4)
	echo -e "${GRN}GET /api/v1/cities/${CITY_ID}${WHT}"
	CITY=$(curl -sX GET $HOST/cities/"${CITY_ID}")
	echo -e "${YLW}${CITY}${WHT}"
	echo -e "\n"

	# not a state
	echo -e "${GRN}GET /api/v1/states/NotAState/cities${WHT}"
	CITIES=$(curl -sX GET $HOST/states/NotAState/cities/)
	echo -e "${RED}${CITIES}${WHT}"
	echo -e "\n"

	echo -e "${GRN}POST /api/v1/states/$STATE/cities${WHT}"
	POST_CITY=$(curl -sX POST $HOST/states/$STATE_ID/cities/ -H "Content-Type: application/json" -d '{"name": "San Francisco"}' -vvv)
	echo -e "${YLW}${POST_CITY}${WHT}"
	echo -e "\n"	

	# missing name
	echo -e "${GRN}POST /api/v1/states/$STATE/cities\nMissingName${WHT}"
	POST_CITY_NOT_NAME=$(curl -sX POST $HOST/states/$STATE_ID/cities/ -H "Content-Type: application/json" -d '{"Location": "State"}' -vvv)
	echo -e "${RED}${POST_CITY_NOT_NAME}${WHT}"
	echo -e "\n"

	# not a json
	echo -e "${GRN}POST /api/v1/states/$STATE/cities\nNotAValidJSON${WHT}"
	POST_CITY_NOT_JSON=$(curl -sX POST $HOST/states/$STATE_ID/cities/ -H "Content-Type: application/json" -d '{"name"}' -vvv)
	echo -e "${RED}${POST_CITY_NOT_JSON}${WHT}"
	echo -e "\n"

	CITY_ID_NEW=$(echo "$POST_CITY" | grep -o '"id":"[^"]*' |  tail -n1 | cut -d'"' -f4)
	echo -e "${GRN}PUT /api/v1/cities/${CITY_ID_NEW}${WHT}"
	PUT_CITY=$(curl -sX PUT $HOST/cities/"${CITY_ID_NEW}" -H "Content-Type: application/json" -d '{"name": "San Francisco is so cool"}')
	echo -e "${YLW}${PUT_CITY}${WHT}"
	echo -e "\n"

	echo -e "${GRN}DELETE /api/v1/cities/${CITY_ID_NEW}${WHT}"
	DELETE_CITY=$(curl -sX DELETE $HOST/cities/"${CITY_ID_NEW}")
	echo -e "${YLW}${DELETE_CITY}${WHT}"
	echo -e "\n"

	echo -e "${GRN}GET /api/v1/cities/${CITY_ID_NEW}\nConfirm Delete. Expect Not Found${WHT}"
	CITY=$(curl -sX GET $HOST/cities/"${CITY_ID_NEW}")
	echo -e "${GRN}${CITY}${WHT}"
	echo -e "\n"

}


function amenities {
	echo -e "${BLU}________________________________________________________${WHT}"
	echo -e "${BLU}_____________________AMENITIES____________________________${WHT}"

	echo -e "${GRN}GET /api/v1/amenities${WHT}"
	AMENITIES=$(curl -sX GET $HOST/amenities/)
	echo -e "${YLW}${AMENITIES}${WHT}"
	echo -e "\n"

	AMENITY_ID=$(echo "$AMENITIES" | grep -o '"id":"[^"]*' |  head -n1 | cut -d'"' -f4)
	echo -e "${GRN}GET /api/v1/amenities/${AMENITY_ID}${WHT}"
	AMENITY=$(curl -sX GET $HOST/amenities/"${AMENITY_ID}")
	echo -e "${YLW}${AMENITY}${WHT}"
	echo -e "\n"

	echo -e "${GRN}POST /api/v1/amenities${WHT}"
	POST_AMENITY=$(curl -sX POST $HOST/amenities/ -H "Content-Type: application/json" -d '{"name": "Wifi"}' -vvv)
	echo -e "${YLW}${POST_AMENITY}${WHT}"
	echo -e "\n"


	# missing name
	echo -e "${GRN}POST /api/v1/amenities\nMissingName${WHT}"
	POST_AMENITY_NOT_NAME=$(curl -sX POST $HOST/amenities/ -H "Content-Type: application/json" -d '{"Location": "State"}' -vvv)
	echo -e "${RED}${POST_AMENITY_NOT_NAME}${WHT}"
	echo -e "\n"


	# not a json
	echo -e "${GRN}POST /api/v1/amenities\nNotAValidJSON${WHT}"
	POST_AMENITY_NOT_JSON=$(curl -sX POST $HOST/amenities/ -H "Content-Type: application/json" -d '{"name"}' -vvv)
	echo -e "${RED}${POST_AMENITY_NOT_JSON}${WHT}"
	echo -e "\n"

	AMENITY_ID_NEW=$(echo "$POST_AMENITY" | grep -o '"id":"[^"]*' |  tail -n1 | cut -d'"' -f4)
	echo -e "${GRN}PUT /api/v1/amenities/${AMENITY_ID_NEW}${WHT}"
	PUT_AMENITY=$(curl -sX PUT $HOST/amenities/"${AMENITY_ID_NEW}" -H "Content-Type: application/json" -d '{"name": "Wifi is so cool"}')
	echo -e "${YLW}${PUT_AMENITY}${WHT}"
	echo -e "\n"

	echo -e "${GRN}DELETE /api/v1/amenities/${AMENITY_ID_NEW}${WHT}"
	DELETE_AMENITY=$(curl -sX DELETE $HOST/amenities/"${AMENITY_ID_NEW}")
	echo -e "${YLW}${DELETE_AMENITY}${WHT}"
	echo -e "\n"
		
	echo -e "${GRN}GET /api/v1/amenities/${AMENITY_ID_NEW}\nConfirm Delete. Expect Not Found${WHT}"
	AMENITY_NOT_FOUND=$(curl -sX GET $HOST/amenities/"${AMENITY_ID_NEW}")
	echo -e "${GRN}${AMENITY_NOT_FOUND}${WHT}"
	echo -e "\n"

}



run;
case $1 in
	"info")
	
	info;
	;;
	"states")
	states;
	;;
	"cities")
	cities;
	;;
	"cleanup")
	cleanup;
	;;
	"amenities")
	amenities;
	;;
	*)
	info;
	states;
	cities;
	amenities;
	;;
esac
cleanup;


