# Usage: Run from root directory as scripts/run_db_commands.sh
# This will get the postgres container name
export DB_CONTAINER=`kubectl get pods | grep postgres | awk '{{print $1 }}'`
echo ${DB_CONTAINER}

# Set database configurations
export CT_DB_USERNAME=ct_admin
export CT_DB_NAME=geoconnections

cat ../db/remove-db-tables.sql | kubectl exec -i ${DB_CONTAINER} -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ../db/2020-08-15_init-db.sql | kubectl exec -i ${DB_CONTAINER} -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ../db/udaconnect_public_person.sql | kubectl exec -i ${DB_CONTAINER} -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ../db/udaconnect_public_location.sql | kubectl exec -i ${DB_CONTAINER} -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"
