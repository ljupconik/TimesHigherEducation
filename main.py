import pandas as pd
import json
import glob
import jaydebeapi as jdbc

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def bulk_load(df, connection, schema, table, chunksize):
    connection.jconn.setAutoCommit(False)
    cursor = connection.cursor()
    sql_exceptions = []
    row_nbr = 0
    df_length = df.shape[0]
    schema_table = '{0}.{1}'.format(schema,table)
    list_columns = list(df.columns)
    cols_names = '('+",".join(list_columns)+')'

    while row_nbr < df_length:
        beginrow = row_nbr
        endrow = df_length if (row_nbr+chunksize) > df_length else row_nbr + chunksize

        list_tuples = [tuple(x) for x in df.values[beginrow : endrow]]
        question_marks_values = '('+",".join('?' for i in list_columns)+')'
        sql = '''INSERT INTO {0} {1} VALUES {2}'''.format(schema_table, cols_names, question_marks_values)
        print(sql)

        try:
            cursor.executemany(sql, list_tuples)
            connection.commit()
        except Exception as e:
            connection.rollback()
            sql_exceptions.append((beginrow,endrow, e))

        row_nbr = endrow

    cursor.close()
    print(sql_exceptions)
    return sql_exceptions


def read_json_file(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def read_and_insert_submissions(filename, connection):
    data = read_json_file(filename)
    df_submissions = pd.json_normalize(
        data,
        record_path =['subjects'],
        meta=['id', 'institution', 'year', 'staff_total']
    )
    df_submissions = df_submissions[['id', 'institution', 'year', 'staff_total', 'name', 'academic_papers', 'students_total', 'student_rating' ]]
    df_submissions.rename(columns = {'name':'subject_name', 'id':'submission_id', 'institution':'institution_id'}, inplace = True)
    bulk_load(df_submissions, connection, 'public', 'submission',  1000)


def delete_processed_file(file):
    pass


def log_success(filename):
    pass
    delete_processed_file(filename)


def log_failure(filename, sql_exceptions):
    pass


def run_it():
    conn = jdbc.connect("org.postgresql.Driver", "jdbc:postgresql://localhost:5432/education" , ['postgres', ''], jars="driver/postgresql-42.2.5.jar")
    df_institutions = pd.read_json('data/institutions.json')
    sql_exceptions = bulk_load(df_institutions, conn, 'public', 'institution',  1000)

    log_success('data/institutions.json') if not sql_exceptions else log_failure('data/institutions.json', sql_exceptions)

    submissionsFilenamesList = glob.glob('data/submissions*.json')
    for file in submissionsFilenamesList:
        sql_exceptions = read_and_insert_submissions(file, conn)
        log_success(file) if not sql_exceptions else log_failure(file,sql_exceptions)

    conn.close()


if __name__ == "__main__":
    run_it()
