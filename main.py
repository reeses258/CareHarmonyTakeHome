import asyncio
import json_stream
import ijson #Use a json stream reader instead of the standard json library to avoid memory limitations
import os
import time
import db


def process_patient(item, path, patientDetails):
    patientDetails[path[len(path)-1]] = item


def process_organization(item, path, organizationDetails):
    organizationDetails[path[len(path)-1]] = item


g_state = {
    'total_patients' : 0,
    'total_organizations' : 0
}

g_resource_lookup = { 
    'Patient': process_patient,
    'Organization' : process_organization
    #Add additional resources that need processing
}


async def process_next_file(patientFileName):
    resource_details = {'currentResource': 'Initial', 'data' : {} }

    """
    Ex: If we were on the last line of the below code, the parameters would look like:
        item = 'Patient', 
        path = ('entry', # in the list, 'resource', 'resourceType' )
    {
        "entry": [
            {
            "resource": {
                "resourceType": "Patient",
    """
    def visitor( item, path ):     
        # We enoucountered a new resource. Increment counts and save to database
        if path[len(path)-1] == 'resourceType':
            if( resource_details['currentResource'] == 'Patient'):
                g_state['total_patients'] = g_state['total_patients'] + 1
                db.add_patient(resource_details)
                resourceDetails = {}

            elif ( resource_details['currentResource'] == 'Organization'):
                g_state['total_organizations'] = g_state['total_organizations'] + 1;
                db.add_organization( resource_details )
                resourceDetails = {}
            
            resource_details['currentResource'] = item
        
        elif g_resource_lookup.get(item, None) != None:
            g_resource_lookup[item](item, path, resource_details)

    #Stream JSON one line at a time. 
    json_stream.visit(open(patientFileName), visitor)


async def main():
    directory = './patients'
    contents = os.listdir('./patients')

    for item in contents:
        patientFileName = directory + '/' + item
        print('Opening File:', patientFileName)
        await process_next_file(patientFileName)

    print(f"Found and Added {g_state['total_patients']} Patients to Database")
    print(f"Found and Added {g_state['total_organizations']} Organizations to Database")


asyncio.run(main())