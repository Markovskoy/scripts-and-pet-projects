#!/bin/bash

. /home/oraupd/.bash_profile

bdauth=""
bduser=""
DBSID=""

ZBX_SENDER=$(which zabbix_sender)
ZBX_CONFIG="/etc/zabbix/zabbix_agentd.conf"
ZBX_HOST=$(hostname)

tmpfile=/tmp/$(uuidgen).tmp

$ORACLE_HOME/sqlplus -silent "$bduser/$bdauth@$DBSID" <<EOF
set echo off
set feedback off
set pagesize 0
set linesize 200
set trimspool on
set space 0
set truncate off
set colsep '|'

spool $tmpfile
------------------------
-- Проверка логов report_form_ora и уровня khd
SELECT 'report_form_ora' AS key,
       CASE 
         WHEN COUNT(*) = 0 THEN 'PROBLEM'
         ELSE 'OK'
       END AS value
FROM rpt)log
WHERE report_alias = 'level_etl'
  AND report_result IS NOT NULL
  AND REGEXP_LIKE(report_result, '^https?://')
  AND TRUNC(report_start_time) = TRUNC(SYSDATE)

UNION ALL

SELECT 'khd_ls' AS key,
       CASE 
         WHEN COUNT(*) = 0 THEN 'OK'
         ELSE 'PROBLEM'
       END AS value
FROM rpt_etl_tbl;

------------------------
spool off
EOF

while IFS='|' read -r key value; do
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | xargs)
  $ZBX_SENDER -s "$ZBX_HOST" -c "$ZBX_CONFIG" -k "$key" -o "$value"
done < "$tmpfile"

rm -f "$tmpfile"
exit 0
