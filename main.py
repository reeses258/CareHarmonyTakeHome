import asyncio
import json_stream
import ijson #Use a json stream reader instead of the standard json library to avoid memory limitations
import os
import time

async def process_bundle( patientFileName ):
    patientFile = ijson.parse(open(patientFileName))
    for prefix, event, value in patientFile:
        print( prefix, event, value )

async def process_patient():
    print ("patient")


g_resource_lookup = { 
    'Bundle' : process_bundle,
    'Patient': process_patient,
}

def process_patient_line( item, path, patientDetails ):
    print( f"{item} at path {path}" )
   # if( path[len(path)-1] == 'id' ):
    patientDetails[path[len(path)-1]] = item
    print(patientDetails )


async def process_next_file(patientFileName):
    currentDetails = {'currentResource': ''}
    currentEntry = -1
    patientDetails = {}
    currentOrganizationDetails = {}

    def visitor( item, path ):
        if item == 'Bundle':
            pass
        
        elif path[len(path)-1] == 'resourceType':
            currentDetails['currentResource'] = item
        
        elif currentDetails['currentResource'] == 'Patient':
            process_patient_line( item, path, patientDetails )
            print( "two:" , patientDetails )
        print( item, path )
        time.sleep(1)


    json_stream.visit(open(patientFileName), visitor)


async def main():
    directory = './patients'
    contents = os.listdir('./patients')

    for item in contents:
        patientFileName = directory + '/' + item
        print('Opening File:', patientFileName)
        await process_next_file(patientFileName)
        break


asyncio.run(main())