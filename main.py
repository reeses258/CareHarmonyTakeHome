import asyncio
import json_stream
import os
import db

"""
    Process functions. These simply store each value in a dict allowing for quick look up or handling later.

    These should also be extended to support any FHIR resource extensions.
"""
def process_patient(item, path, patient_details):
    if path[len(path)-1] == 'id':
        # Store patient_id outside of data so it can be accessed by other resources
        patient_details['patient_id'] = item
    patient_details['data'][path[len(path)-1]] = item


def process_organization(item, path, organization_details):
    organization_details['data'][path[len(path)-1]] = item


def process_observation(item, path, process_details):
    process_details['data'][path[len(path)-1]] = item


def process_practitioner(item, path, practitioner_details):
    practitioner_details['data'][path[len(path)-1]] = item


def process_encounter(item, path, encounter_details):
    encounter_details['data'][path[len(path)-1]] = item


def process_condition(item, path, condition_details):
    condition_details['data'][path[len(path)-1]] = item


def process_procedure(item, path, procedure_details):
    procedure_details['data'][path[len(path)-1]] = item


def process_claim(item, path, process_details):
    process_details['data'][path[len(path)-1]] = item


def process_explanation_of_benefit(item, path, benefit_details):
    benefit_details['data'][path[len(path)-1]] = item


g_state = {
    'total_patients' : 0,
    'total_organizations' : 0,
    'total_observations' : 0,
    'total_practitioners' : 0,
    'total_encounters' : 0,
    'total_conditions' : 0,
    'total_procedures' : 0,
    'total_claims' : 0,
    'total_explanation_of_benefits' : 0,
}

g_resource_lookup = { 
    'Patient': process_patient,
    'Organization' : process_organization,
    'Observation' : process_observation,
    'Practitioner' : process_practitioner,
    'Encounter' : process_encounter,
    'Condition' : process_condition,
    'Procedure' : process_procedure,
    'Claim' : process_claim,
    'ExplanationOfBenefit' : process_explanation_of_benefit,
    #Add additional resources that need processing
}


async def process_next_file(patientFileName):
    resource_details = {'currentResource': 'Initial', 'patient_id': None, 'data' : {} }

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
                resource_details['data'] = {}

            elif ( resource_details['currentResource'] == 'Organization'):
                g_state['total_organizations'] = g_state['total_organizations'] + 1;
                db.add_organization( resource_details )
                resource_details['data'] = {}

            elif ( resource_details['currentResource'] == 'Observation'):
                g_state['total_observations'] = g_state['total_observations'] + 1;
                db.add_observation( resource_details )
                resource_details['data'] = {}
            
            elif ( resource_details['currentResource'] == 'Practitioner'):
                g_state['total_practitioners'] = g_state['total_practitioners'] + 1;
                db.add_practitioner( resource_details )
                resource_details['data'] = {}
            
            elif ( resource_details['currentResource'] == 'Encounter'):
                g_state['total_encounters'] = g_state['total_encounters'] + 1;
                db.add_encounter( resource_details )
                resource_details['data'] = {}

            elif ( resource_details['currentResource'] == 'Condition'):
                g_state['total_conditions'] = g_state['total_conditions'] + 1;
                db.add_condition( resource_details )
                resource_details['data'] = {}
            
            elif ( resource_details['currentResource'] == 'Procedure'):
                g_state['total_procedures'] = g_state['total_procedures'] + 1;
                db.add_procedure( resource_details )
                resource_details['data'] = {}
            
            elif ( resource_details['currentResource'] == 'Claim'):
                g_state['total_claims'] = g_state['total_claims'] + 1;
                db.add_claim( resource_details )
                resource_details['data'] = {}
            
            elif ( resource_details['currentResource'] == 'ExplanationOfBenefit'):
                g_state['total_explanation_of_benefits'] = g_state['total_explanation_of_benefits'] + 1;
                db.add_explanation_of_benefit( resource_details )
                resource_details['data'] = {}
            
            resource_details['currentResource'] = item
        
        # Build resource_details
        elif g_resource_lookup.get(resource_details['currentResource'], None) != None:
            g_resource_lookup[resource_details['currentResource']](item, path, resource_details)

    
    # Ideally this stream would support asyncio. However I discovered it did not too late in the process,
    # otherwise we could make this entire file async to opitmize it for any slow database transactions. 
    json_stream.visit(open(patientFileName), visitor) # Stream JSON one line at a time.


"""
    Primary entry point. Will run over the ./patients/ directory and add each resource it finds to a database defined in db.py.
"""
async def main():
    directory = './patients'
    contents = os.listdir('./patients')

    print(f"Processing {len(contents)} files in {directory}")
    for item in contents:
        patientFileName = directory + '/' + item
        await process_next_file(patientFileName)


    print(f"Found and Added {g_state['total_patients']} Patients to Database")
    print(f"Found and Added {g_state['total_organizations']} Organizations to Database")
    print(f"Found and Added {g_state['total_observations']} Observations to Database")
    print(f"Found and Added {g_state['total_practitioners']} Practitioners to Database")
    print(f"Found and Added {g_state['total_encounters']} Encounters to Database")
    print(f"Found and Added {g_state['total_conditions']} Conditions to Database")
    print(f"Found and Added {g_state['total_procedures']} Procedures to Database")
    print(f"Found and Added {g_state['total_claims']} Claims to Database")
    print(f"Found and Added {g_state['total_explanation_of_benefits']} Explanation of Benefits to Database")


asyncio.run(main())