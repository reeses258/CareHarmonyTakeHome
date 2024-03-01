# CareHarmonyTakeHome

CareHarmony needs to work with many different health systems that each have hundreds of thousands of patients. Whenever CareHarmony onboards a new health system, they need to ingest the data for thousands of patients into their software. This data includes EHR data, claims data, communication data, marketing data, etc.

Q1 - How would you approach designing an API that the health systems could use to "push" the data into CareHarmony's software?

I would first approach this by researching the clients to understand how thier data is structured. 
- Since no specific client was specified, I researched what the top EHR systems use. The three largest EHR systems are Epic (38%), Oracle Cerner (22%) and Meditech (13%). All of these support FHIR's common data model. Any new system handling EHR and related data should support this commonly used data model. FHIR's design can be found on their website but essentially everything is broken into resources. Each resource can hold extensions which allows nearly any kind of record to be used.

Next I would look into thier use cases.
- The two biggest use cases that come to mind when pushing data to CareHarmony is the iniital onboarding and the second is periodic updates as new patients, or records for existing patients are added. The intial description appears to focus more on the onboarding case, so I will only deep dive into that one but provide an API to allow an external health system to push updates to CareHarmony. 

Then I would look into how to transfer this possibly large set of data from the client into a CareHarmony datastore that best holds the data.
- To understand the type of data that needs to be sent I downloaded some free EHR FHIR datasets. An example patient can be seen in example_patient.json. The samples I got my hands on are in JSON format. According to FHIR's documentation, FHIR also works well with XML but for the purpose of this assignment I will assume our client can send the data in a JSON format.
- One of the best ways to store JSON in a scalable way is with MongoDB and use GraphQL to query it.
- FHIR's framework has defined an $export operation for bulk transfers. https://build.fhir.org/ig/HL7/bulk-data/export.html
  - This would be the ideal approach but it is more of a "pull" approach that CareHarmony would initiate.
- If the health system did not implement the export operation I would look break this into two primary steps.
  1. The health care system would need to generate output file(s) in FHIR format containing all the records needing to be transferred.
  2. Zip the FHIR (JSON) files to reduce the size.
  3. Implement a multipart file upload REST API (or pay for one like Amazon's AWS/S3) to transfer the files to a filesystem within CareHarmony. (See below)
- Once the export files containing the records are copied over, we can move to Q2 to process the data and make it readily available for internal CareHarmony users.


Multi Part File API -
- int InitiateMultiPartFile( string filename, int numParts )
  - Returns an uploadId.
- int UploadPart( int uploadId, int partNumber, char[] md5hash, int size )
  - Validates the md5hash of the file, and the size of the transfer.
- int CompleteUpload( int uploadId )
  - Validates that all the parts were succesful. Returns a non 0 value on error.
- vector<int> returnMissingParts( int uploadId )
  - Returns a list of part numbers that have not completed uploading

An API designed this way has a few advantages. First is that it can do asyncrounsly and be split across multiple servers to transfer multiple files and parts of files at the same time. The downside is the logic is not super simple and might require an app or script provided to the healthcare company.



Q2 - Once the data is pushed, how would you design an automated system to process and ingest that data into CareHarmony's software so that its fully available for internal users?

Once the data is pushed we will end up a set of very large JSON files using the FHIR content model. Our goal would be to process these files and insert the data contained in them into CareHarmony's database so that they can be queried by internal staff. For processing these files I would setup a queue based approach that uses a leader and a pool of workers. For this step, I will use the example records I found online. The leader would be a simple script that does the following steps.


Leader - 
1. Scan for new completed pushed files.
2. View the contents of the zip file.
3. Add each file inside the zip to the work queue.

Workers -
1. Grab the first file on the queue.
2. Using a JSON stream reader parse the json in pieces and add each piece to our mongoDB. 

Note -
In the example files I have, it is one giant zip with folders inside containing an individual json file for each patient. My design will be based off that. If the health care system provided only a single containing everything, the leader would need to use a stream reader (to avoid running out of memory) and queue up individual blocks of json to the queue. 






For the next part I am going to make some assumptions on the layout of CareHarmony's database so that I can code up an example of processing these files. 

Database Design -

Patients
  This database is designed to hold the most basic patient information. The ID can be used across most other database entries to query specific information related to the patient. In a health care system I'm assuming most queries will be either attempting to link a single patient to differnt record types across multiple databases or verify we have a record of the patient based on an unique identifier like Social Security Number (SSN), email or medical record number. The data here is very relational and the size of each entry can be fixed. We could use a relational DB like MySQL. However since we will be using MongoDB to store other records that need to be more flexible, we could put use MongoDB here if it saves on cost. 
  
- ID (string or FHIR Identifier type)
- SSN ( string )
- Email ( string )
- Medical Record Number ( string )
- FirstName ( string )
- LastName ( string )
- Telephone ( string )



The processing steps goal is straight forward, read each file and break it For processing JSON I usually like to use Python as it has some great base functionality for handling JSON. However the downside is the standard library for JSON will attempt to load the entire file in memory at once.  


However there are claims they do not support all of FHIR's functionality. So an API specific to CareHarmony will likely need to be tailored to speci

FHIR adapts modern, widely used RESTful practices. My implementation will use a RESTful api approach to transfer information to and from external healthcare institutions.


High Level API -
/api/authenticate ( userID, timeStamp, personalKey )
/api/EHR/

Ingest - ( To CareHarmony )
/api/
PUT 


Storage -

FHIR can be represented in two main ways. XML and JSON. 
