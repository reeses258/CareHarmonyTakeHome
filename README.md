# CareHarmonyTakeHome

CareHarmony needs to work with many different health systems that each have hundreds of thousands of patients. Whenever CareHarmony onboards a new health system, they need to ingest the data for thousands of patients into their software. This data includes EHR data, claims data, communication data, marketing data, etc.

Q1 - How would you approach designing an API that the health systems could use to "push" the data into CareHarmony's software?

I would first approach this by researching the clients to understand how thier data is structured. 
- Since no specific client was specified, I researched what the top EHR systems use. The three largest EHR systems are Epic (38%), Oracle Cerner (22%) and Meditech (13%). All of these support FHIR's common data model. Any new system handling EHR and related data should support this commonly used data model. FHIR's design can be found on their website but essentially everything is broken into resources. Each resource can hold extensions 

Next I would look into thier use cases.
- The two biggest use cases that come to mind when pushing data to CareHarmony is the iniital onboarding and the second is periodic updates as new patients, or records for existing patients are added. The intial description appears to focus more on the onboarding case, so I will only deep dive into that one but provide an API to allow an external health system to push updates to CareHarmony. 

Then I would look into how to transfer this possibly large set of data from the client into a CareHarmony datastore that best holds the data.
- To understand the type of data that needs to be sent I downloaded some free EHR datasets. An example patient can be seen in example_patient.json. The samples I got my hands on are in JSON format. According to FHIR's documentation, FHIR also works well with XML but for the purpose of this assignment I will assume our client can send the data in a JSON format. One of the best ways to store JSON in a scalable way is with MongoDB.


The basis of my API design will focus on what appears to be the most commonly used version of FHIR, known as R4 (https://hl7.org/fhir/r4/). I will only discuss APIs that would be used for data ingestion from a health care system that already contains many patients.

PUSH API -
/api/authenticate( userID, timeStamp, personalKey ) 
/api/batch( ) // Primary API to begin ingestion.
/api/update( ) // Used for single periodic updates.


- Authentication
  I am not going to dive into this but any API needs security and an authentication method to prevent unwanted access.

- Batch
  


Q2 - Once the data is pushed, how would you design an automated system to process and ingest that data into CareHarmony's software so that its fully available for internal users?



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
