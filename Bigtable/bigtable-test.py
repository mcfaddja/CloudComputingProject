"""
Code to connect to big table and perform some basic create,delete operations

Prerequisites:
    Assuming that you have a bigtable cluster up and running with all the requisite permissions appropriately.

Referred from https://cloud.google.com/bigtable/docs
"""

import argparse

from google.cloud import bigtable


def main(project_id, instance_id, table_id):
    # Establish a connection to the big table.
    # specify admin as True for any admin related operations including 'create'.
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)

    print('Creating the {} table.'.format(table_id))
    # New table
    table = instance.table(table_id)
    table.create()
    # declaring column id
    # Since Bigtable tables are sparse, its okay to create empty columns
    column_family_id = 'c1'
    c1 = table.column_family(column_family_id)
    c1.create()

    print('Writing data to the table.')
    column_id = 'data'.encode('utf-8')
    data = [
        'Data entry 1',
        'Data entry random',
        'Data entry 2',
        'Data entry is not ordered :)',
    ]

    # To read the data we use a simple data_number as an ID. Not an optimal way of ordering the keys
    # we can even store timestamps as row key for better.
    for i, value in enumerate(data):
        row_key = 'data{}'.format(i)
        row = table.row(row_key)
        row.set_cell(
            column_family_id,
            column_id,
            value.encode('utf-8'))
        row.commit()

    # Retrieving single data
    print('Getting a data entry by row key.')
    key = 'data0'
    row = table.read_row(key.encode('utf-8'))
    value = row.cells[column_family_id][column_id][0].value
    print('\t{}: {}'.format(key, value.decode('utf-8')))

    # Retrieving entire data
    print('Scanning for all data entries:')
    scan_rows = table.read_rows()
    scan_rows.consume_all()

    for row_key, row in scan_rows.rows.items():
        key = row_key.decode('utf-8')
        cell = row.cells[column_family_id][column_id][0]
        value = cell.value.decode('utf-8')
        print('\t{}: {}'.format(key, value))

    # # Uncomment this if you want to delete the table at the end of operation
    # # to avoid any needless charges.
    # print('Deleting the {} table.'.format(table_id))
    # table.delete()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument(
        'instance_id', help='ID of the Cloud Bigtable instance to connect to.')
    parser.add_argument(
        '--table',
        help='Table to create and destroy.',
        default='Bigtable-Test')

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.table)