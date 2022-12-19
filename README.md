# Coding Challenge: Energy Analyzer

This is a coding challenge for the Carbon Lighthouse interview process.

### Background

A core part of Carbon Lighthouse’s product offering is to recommend, implement,
and monitor various projects that reduce the energy usage of a building. We call
these projects "Energy Efficiency Measures," or EEMs. Examples of an EEM might
be replacing a piece of equipment with a more efficient one, changing the
schedule of a building, or a variety of other things.

We've built a number of machine learning and physics based models that predict
the expected energy usage of a building as well as the expected energy savings
of various measures. We have also built a backend service that can run these
models via an API. In this replit environment, we've provided a very slimmed
down / stubbed API for this service, which we will ask you to build on top of.

For this interview, we'll imagine we're building a new customer-facing
application, the "Energy Analyzer", that will leverage the results of running
these models.

### Agenda

First, let's briefly walk through the stubbed out API and other code we've
provided. That should give you a sense of the various domain concepts involved
as well as the capabilities of the stubbed API.

Next, we will provide a few high-level product requirements for the "Energy
Analyzer" application. At that point we'll then hand it over to you to:

-   Collaboratively sketch a very rough UI for a portion of the application to
    make sure we’re aligned on these requirements.
-   Have a quick conversation around technology choices for the application.
-   Discuss and design 2-3 of the core APIs that the backend would need to serve
    this application.
-   Pick one of those APIs and implement the relevant backend business logic in
    our pair-programming environment.

### Assumptions/Notes:

-   We can ignore all user login / authentication concerns.
-   The thermo and ML models output timeseries data on consistent intervals.

### High Level Product Requirements:

NOTE: For this section, your interviewer will be role-playing in a "PM" type
role. The product requirements are not super fleshed out, and may not be well
informed by the backend capabilities we actually have.

-   [MVP] As a building owner, I need to understand the how the energy usage of
    my building would change after certain EEMs were implemented, both on a
    monthly and annual basis.
-   [MVP] As a building owner, I can choose which EEMs are being used in the
    analyzer to help me decide which ones would have the most impact.
-   [v2] As a building owner, I need to understand how my utility bill would
    change as a result of implementing certain measures.
-   [v2] As a building owner, I need to know if implementing these measures in
    my building would be a smart financial investment. I need to know the return
    on investment / payback period to help me decide which measures to
    implement.

### Collaboratively sketch

Note to interviewee: For this section, I'll still be role-playing in a PM role,
and as someone who doesn't have wireframe / design experience (which is why
we're asking for your input on the UI). We'll focus on just the two MVP
requirements, and we can assume the user has already logged in, selected the
building the want to analyze, etc.

We'll hand it over to you to start sketching. The goal is not to have anything
close to complete wireframes, but simply to reach a shared understanding of the
data that needs to be presented, and what the major UI interactions need to be.
We've provided some templates in the system/UI libraries; free free to copy in
anything from there.

### Code overview

This project is managed with `poetry`. The project can be installed with
`poetry install`. Tests can be run with `poetry run pytest .`. The relevant
files are:

-   `energy_analyzer/models.py`: Provides a simple data model and business logic
    for the Energy Analyzer.
-   `energy_analyzer/energy_client.py`: Provides the stubbed API as mentioned
    above. It has two methods defined: 1) get the expected energy usage for a
    building and 2) get the expected energy savings for a measure. Read the doc
    string of `EnergyClient` methods for more detail.
-   `energy_analyzer/tests/test_biz.py`: Tests and Fixtures for the Energy
    Analyzer business logic.
