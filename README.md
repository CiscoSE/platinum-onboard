# platinum-onboard

PoC for onboarding new users onto a network


## Business/Technical Challenge

Onboarding guest or contractors onto a network has been made simpler over the years by advances in identity solutions and wireless networks.   However, customers still experience pain points when adding users.   Some of these are:

* There still needs to be manual intervention to create the guest account.   This can be a lobby ambassador or guest sponsor.
* Some customers are unable to open up a captive portal due to customer restrictions.   This makes it impossible to log on to the network.
* Once a user has been successfuly onboarded, does the host company has little visibility of what the user has been doing.
* Users get frustrated so they start using hotspots or cell phones for accessing networks.

These are just several of the problems that are associated with onboarding guest or contractor users.   They are mnade worse when the amount of guest users increase.   For example, at a customer trade show when there could be thousands of guest or contractor users.   Or on training or meetings where there is might be late additions to the roster.

With the increase of technological features, there must be a better solution to address this problem!

## Proposed Solution

Our proposed solution is based upon Cisco's Intelligent Proximixty feature and Cisco WebEx Teams.   This solution allows endpoints to dynamically detect devices and users that in range.   We are planning to leverage the proximity feature to serve as the backbone of our platinum onboarding solution.   This solution will automatically detect guest or contractor users and with that information we will begin to onboard the user onto the network.   Cisco's ISE can then be used to apply policies to that user when they are added to the network.    And to provide the visibility, Cisco Umbrella will be leveraged to monitor and keep track of what the user is doing.

The solution can be deployed in several different use cases:
* Conference Rooms - When guest users enter the conference room, they will be automatically onboarded as users on the network.
* Kiosks - Users can walk up to a kiosks and automatically be onboarded onto the network.
* Registration - Instead of registering for services by entering identification like SS#, the platinum onboard feature can be used to quickly register these users using the capabilities built into their mobile devices.

With the platinum onboarding capability deployed in a network, customers can enjoy much more streamlined workflow to bring on new users.


### Cisco Products Technologies/ Services

Our solution will levegerage the following Cisco technologies

* [WebEx Teams] (https://www.webex.com/products/teams/index.html)
* [WebEx Room Series] (https://www.cisco.com/c/en/us/products/collaboration-endpoints/webex-room-series/index.html)
* [Cisco Intelligent Proximity] (https://www.cisco.com/c/en/us/products/collaboration-endpoints/intelligent-proximity.html)
* [Identity Services Engine (ISE)] (http://cisco.com/go/ise)
* [Umbrella] (http://www.cisco.com/go/umbrella)

## Team Members


* Chris Bogdon <cbogdon@cisco.com> - Trans PNC Enterprise Account
* Jason Beltrame <jabeltra@cisco.com> - Greater Pennsylvania Territory
* Adam Schaeffer<adschaef@cisco.com> - Philadelphia Metro Territory


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
