### ToDo

-   [ ] Data Validation
-   [ ] Consider breaking each resource into its own python script
-   [ ] Have lex announce the available resources, actions.
-   [ ] A way to go back to a previous intent, disregard the previous request.
-   [ ] Download something from a website and store it in the S3 bucket.

### InProgress

-   [ ] Basic EC2 Operations
-   [ ] Basic S3 Operations

### Done

-   [x] Basic DynamoDB Operations


### Questions
-   [ ] EC2 operations, launch which operating system and avoid AMI. 
        Golend image. All instances are spawned using the golden AMI, immutable, apply tags.
        Tag: Golden_AMI. 
        How to find the AMI tagged Golden_AMI.
        Spawn it from a AMI that has the tag golden. 
        In general, for randomly generated string identifiers for resources, tags are used to 
        give more meaning to them.
        resource group tagging api, get resources.
-   [ ] Look into step functions for state transitions for ec2.
-   [ ] Call describe instance to determine whether the user can do something.
-   [ ] Async: implement promise. But this is bad. Don't use in lambda.
        Lambda should be quick. Step functions also can do this. 
        Write lambda as stateless functions.
-   [ ] Handle retry:
        1. Use step functions, configure each state in a step function.
        2. Different backoff strategies, exponential backoff strategies.
        3. item potency tokens, avoid kicking up too many instances. Fault tolerance. In Distributed systems.
-   [ ] Use a proper unit testing framework. 
        Itegration testing framework. 

        Canary?
                
        Unit testing works in isolation. 
                Mock every single services that uses this unit.
                Unit testing should be part of the build process. Framework triggered as soon as it is finished building.

        
