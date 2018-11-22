# platinum-onboard

PoC for onboarding new users onto a network


## Business/Technical Challenge

Onboarding guest onto a network has been made simpler over the years by advances in identity solutions and wireless networks.   However, customers still experience pain points when adding users.   Some of these are:

* There still needs to be manual intervention to create the guest account.   This can be a lobby ambassador or guest sponsor.
* Some customers are unable to open up a captive portal due to customer restrictions.   This makes it impossible to log on to the network.
* Once a user has been successfuly onboarded, the host company has little visibility of what the user has been doing.
* Users get frustrated so they start using hotspots or cell phones for accessing networks.

These are just several of the problems that are associated with onboarding guest users.   Contractor access is even more problematic since they are onsite so infrequently, so IT departments often have to reenable the contractors credentials at each visit.  Even worse, IT departments attempt to avoid this by giving the contractor an account with credentials permanently enabled with no password 60 or 90 day age restrictions.  The problems are even made worse when the amount of guest users increase.   For example, at a customer trade show when there could be thousands of guest or contractor users. 

With the increase of technological features, there must be a better solution to address this problem!

## Proposed Solution

Cisco has already made tremendous strides in solving this problem through both its networking platforms as well as Identity Services Engine.  There are, however, a few ways that these platforms can still be brought together to better provisioning as well as increase the control and accountability system wide.

Our proposed solution is based upon Cisco's Intelligent Proximixty feature and Cisco WebEx Teams.   This solution allows endpoints to dynamically detect devices and users that are in range.   We are planning to leverage the proximity feature to serve as the backbone of our platinum onboarding solution.   This solution will automatically detect guest or contractor users and with that information we will begin to onboard the user onto the network.   

The core to the entire system will in fact be the Identity Services Engine (ISE).  It’s a powerful policy platform with an open API.  It’s PxGrid capabilities make it a great hub for control and policy in both Cisco and non-Cisco centric environments.  And to provide the visibility, Cisco Umbrella will be leveraged to monitor and keep track of what the user is doing.

The solution can be deployed in several different use cases:
* Conference Rooms - When guest users enter the conference room, they will be automatically onboarded as users on the network.
* Kiosks - Users can walk up to a kiosks and automatically be onboarded onto the network.
* Registration - Instead of registering for services by entering identification like SS#, the platinum onboard feature can be used to quickly register these users using the capabilities built into their mobile devices.

By combining these best of bread products together, customers can enjoy much more streamlined workflow to bring on new users.


### Cisco Products Technologies/ Services

Our solution will levegerage the following Cisco technologies

*[WebEx Teams] (https://www.webex.com/products/teams/index.html)
*  [WebEx Room Series] (https://www.cisco.com/c/en/us/products/collaboration-endpoints/webex-room-series/index.html)
*  [Cisco Intelligent Proximity] (https://www.cisco.com/c/en/us/products/collaboration-endpoints/intelligent-proximity.html)
*  [Identity Services Engine (ISE)] (http://cisco.com/go/ise)
*  [Cisco PxGrid] (http://www.cisco.com/go/pxgrid)
*  [Umbrella] (http://www.cisco.com/go/umbrella)

## Team Members


* Chris Bogdon <cbogdon@cisco.com> - Trans PNC Enterprise Account
* Jason Beltrame <jabeltra@cisco.com> - Greater Pennsylvania Territory
* Adam Schaeffer <adschaef@cisco.com> - Philadelphia Metro Territory


## Solution Components


<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of the components involved with this project. e.g Python /  -->


## Usage

<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of how to use the solution  -->



## Installation

How to install or setup the project for use.


## Documentation

Pointer to reference documentation for this project.


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
