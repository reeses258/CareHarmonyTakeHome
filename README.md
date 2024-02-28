# CareHarmonyTakeHome

The three largest EHR systems are Epic (38%), Oracle Cerner (22%) and Meditech (13%). All of these support FHIR's common data model. Any new EHR system should support this common data model to provide transfering information to and from entities. 


However there are claims they do not support all of FHIR's functionality. So an API specific to CareHarmony will likely need to be tailored to speci

FHIR adapts modern, widely used RESTful practices. My implementation will use a RESTful api approach to transfer information to and from external healthcare institutions.


High Level API -
/api/authenticate
  Authenticate( userID, timeStamp, personalKey )

Ingest - ( To CareHarmony )
/api/
PUT 


Storage -

FHIR can be represented in two main ways. XML and JSON. 
