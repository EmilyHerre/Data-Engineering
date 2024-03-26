import pandas as pd
import sqlite3

# Read CSV files into DataFrames
projects_df = pd.read_csv('projects.csv', encoding='latin-1', delimiter=';')
employees_df = pd.read_csv('employees.csv', encoding='iso-8859-1', delimiter=';')
specialties_df = pd.read_csv('specialty.csv', encoding='iso-8859-1', delimiter=';')
hours_df = pd.read_csv('hours_worked.csv', encoding='iso-8859-1', delimiter=';')

projects_df.rename(columns={'codigo': 'proyecto', 'descripcion':'descripcion_proyecto'}, inplace=True)

# # # Merge DataFrames to combine relevant information
merged_df = pd.merge(hours_df, employees_df, on='cedula')
merged_df = pd.merge(merged_df, projects_df, on='proyecto')

merged_df = merged_df.drop_duplicates(subset=['fecha','proyecto' ,'cedula', 'horas'])

# # Connect to SQLite database
conn = sqlite3.connect('building_data.db')
cursor = conn.cursor()

# # # # Create tables for each project and insert datas
for project_name, project_data in merged_df.groupby('descripcion_proyecto'):
    project_table_name = f'proyecto_{project_name}'

    project_data = project_data[['fecha', 'cedula', 'nombre', 'apellidos','horas','especialidad']]

    # Verify that the table exists
    table_empty = pd.read_sql(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{project_table_name}'", conn).empty
    
    if table_empty:
        project_data.to_sql(project_table_name, conn, index=False)
        print(f"Se creo la tabla '{project_table_name}' y se ingresaron los datos.")
    else:
        existing_data_query = f"SELECT * FROM '{project_table_name}'"
        existing_data_df = pd.read_sql(existing_data_query, conn)

        # Combine existing data with df 
        merged_data = pd.merge(existing_data_df, project_data, how='outer', indicator=True)

        # Filter data that is only in the current project and add it to the existing table
        new_data_to_insert = merged_data[merged_data['_merge'] == 'right_only'].drop(columns='_merge')
        
        if not new_data_to_insert.empty:
            # Insert the new data into the database
            new_data_to_insert.to_sql(project_table_name, conn, index=False, if_exists='append')
            print(f"Se agregaron datos adicionales al proyecto '{project_name}''.")
        else:
            print(f"No se encontraron datos nuevos para agregar al proyecto '{project_name}''.")

# # Commit changes and close connection 
conn.commit()
conn.close()