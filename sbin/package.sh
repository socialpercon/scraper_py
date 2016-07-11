#!/bin/bash

NAME="package"

CURRENT_DIR=$(dirname "${BASH_SOURCE-$0}")
CURRENT_DIR=$(cd "${CURRENT_DIR}">/dev/null; pwd)


EXECUTIVE_FILE_PATH="${CURRENT_DIR}/../bin/${NAME}-rest"

PID_DIR="${ESI_HOME}/pids/"
LOG_DIR="${ESI_HOME}/log/"

PID_FILE="${PID_DIR}/${NAME}.pid"
LOG_FILE="${LOG_DIR}/${NAME}.log"


. "${CURRENT_DIR}/functions.sh"

function init_default_dirs() {
    if [[ ! -d "${LOG_DIR}" ]]; then
        #echo "Log dir doesn't exist, create ${LOG_DIR}"
        $(mkdir -p "${LOG_DIR}")
    fi

    if [[ ! -d "${PID_DIR}" ]]; then
        #echo "Pid dir doesn't exist, create ${PID_DIR}"
        $(mkdir -p "${PID_DIR}")
    fi
}

function start() {
    local pid

    if [[ -f "${PID_FILE}" ]]; then
        pid=$(cat ${PID_FILE})
        if kill -0 ${pid} >/dev/null 2>&1; then
            action_msg "${NAME}" " already running" "${SET_PASSED}"
            return 0;
        fi
    fi

    init_default_dirs
    printf "\n\n\n\n\n" >> ${LOG_FILE}
    nohup nice -n 0 ${EXECUTIVE_FILE_PATH} >> "${LOG_FILE}" 2>&1 < /dev/null &
    pid=$!

    if [[ -z "${pid}" ]]; then
        action_msg "${NAME}" " start" "${SET_ERROR}"
        return 1
    else
        action_msg "${NAME}" " start" "${SET_OK}"
        echo ${pid} > ${PID_FILE}
    fi
}

function wait_for_app_to_die()
{
    local pid
    local count
    pid=$1
    count=0

    while [[ "${count}" -lt 3 ]]; do
        $(kill -15 ${pid} > /dev/null 2> /dev/null)

        if kill -0 ${pid} > /dev/null 2>&1; then
            sleep 3
            let "count+=1"
        else
            return 0
        fi
#        if [[ "${count}" == 5 ]]; then
#            return 1
#        fi
    done

    return 1
}

function force-kill-process()
{
    local pid
    pid=$1

    sleep 2

    return $(kill -9 ${pid} > /dev/null 2> /dev/null)
}

function stop() {
    local pid

    if [[ ! -f "${PID_FILE}" ]]; then
        action_msg "${NAME} is not running" "${SET_STOPPED}"
        return 0
    fi
    pid=$(cat ${PID_FILE})
    if [[ -z "${pid}" ]]; then
        action_msg "${NAME} is not running" "${SET_OK}"
        echo "${NAME} is not running" >> ${LOG_FILE} 2>&1
    else
        if ! wait_for_app_to_die ${pid}; then
            action_msg "${NAME} cannot be killed" "${SET_ERROR}"
            echo "${NAME} could not be killed" >> ${LOG_FILE} 2>&1
        else
            $(rm -f ${PID_FILE})
            action_msg "${NAME} stopped" "${SET_OK}"
            echo "${NAME} is stopped" >> ${LOG_FILE} 2>&1
        fi
    fi
}


function status()
{
    PID=$( cat "${PID_FILE}" 2> /dev/null ) || true

	if test -n "${PID}" && kill -0 $PID 2> /dev/null; then
		action_msg "${NAME} (${PID}) is running" "${SET_OK}"
		state=0
    else
        action_msg "${NAME} is stopped" "${SET_STOPPED}"
        state=1
    fi
    echo "=========================== Latest 5 logs ==========================="
    tail -5 ${LOG_FILE}
    echo "====================================================================="
	exit $state
}

function kill_app()
{
    local pid

    if [[ ! -f "${PID_FILE}" ]]; then
        action_msg "${NAME} is not running" "${SET_OK}"
    else
        pid=$(cat ${PID_FILE})
        if  force-kill-process ${pid}; then
            action_msg "${NAME} is killed successfully." "${SET_OK}"
            echo "${NAME}  is killed successfully." >> ${LOG_FILE} 2>&1
        else
            action_msg "${NAME} cannot be killed." "${SET_ERROR}"
            echo "${NAME} could not be killed." >> ${LOG_FILE} 2>&1
        fi
        $(rm -f ${PID_FILE})
    fi
}

function force-reload()
{
    kill_app
    start
}

case "$1" in
start)
	start
;;
stop)
	stop
;;
kill)
    kill_app
;;
force-reload)
    force-reload
;;
status)
	status
;;
restart)
	echo "Restarting ${NAME}" >> ${LOG_FILE} 2>&1 < /dev/null
	stop
	sleep 1
	start
;;
*)
	echo "Usage: $0 {start|stop|kill|restart|force-reload|status}" >&2
	exit 1
;;
esac


