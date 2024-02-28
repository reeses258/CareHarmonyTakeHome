# CareHarmonyTakeHome

The three largest EHR systems are Epic (38%), Oracle Cerner (22%) and Meditech (13%). All of these support FHIR's common data model. Any new EHR system should support this common data model to provide transfering information to and from entities.
The basis of my API design will focus on a commonly used version of R4 FHIR. The API for a new heath system to push the data will have two main entry points. Pushing data for a single patient, and pushing data 





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
