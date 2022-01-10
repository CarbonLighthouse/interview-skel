# Coding Challenge: Energy Analyzer

This is an at-home coding challenge for the Carbon Lighthouse interview process.

Instructions:
* Clone this repo, and run the `install.sh` script. This will set up a virtual environment for you, and install the required dependencies. 
* Review the background information and overview of the provided code.
* Review the Sample Task to see how we would like you to format your solution.
* Provide your solution to the Challenge Task by implementing required backend functionality and tests.
* Create a zip archive of your code and return to Carbon Lighthouse.

**Recommended time limit: 2 hours**

### Background

A core part of Carbon Lighthouse’s product is to recommend, implement, and monitor various projects that reduce the energy usage of a building. We call these projects "Energy Efficiency Measures." A Measure can be replacing a piece of equipment with a more efficient one, changing the schedule of a building, or a variety of other things.

We have built a number of machine learning and physics based models that can predict the expected energy usage of various building types as well as the expected energy savings of various measures.
We have also built a backend service that can run these models via an API. This repo provides a stubbed API for this service, and we will ask you to build on top of it

For this coding challenge, imagine we are building a new customer-facing application, the “Energy Analyzer”, that can present the results of running these models. 
We will ask you to implement some backend business logic, not a full backend system or a full application with a UI.
In this example, we model a generic year's worth of savings for each Measure, which can be used to predict future energy savings.

### Code overview

* `energy_analyzer/models.py`: Provides a simple data model and all business logic for the Energy Analyzer. Also contains fixtures to facilitate running tests.
* `energy_analyzer/energy_client.py`: Provides the stubbed API as mentioned above. It has two methods defined: 1) get the expected energy usage for a building and 2) get the expected energy savings for a measure. Read the doc string of `EnergyClient` methods for more detail.
* `energy_analyzer/test_biz_logic.py`: Tests for the Energy Analyzer business logic.

### Sample Task

This task has already been completed for you.

Implement a method on the Building model, called `get_past_and_future_year_of_monthly_energy_usage_without_measures` that returns monthly expected energy usage data. It should return data ranging from one year in the past to one year in the future. This method should sum the 15m data returned by the EnergyClient for each month. It will ignore any measure present.

### Challenge Task

Implement a method on the Building model, called `get_past_and_future_year_of_monthly_energy_usage_with_measures` that returns monthly expected energy usage data. It should return data ranging from one year in the past to one year in the future. This method should sum the 15m data returned by the EnergyClient for each month. Unlike the last task, it should also see what measures are attached to the building and reduce the returned energy usage accordingly. A correct solution will take into account the start and end times for each measure.

Note: We have provided some failing tests for this task. However, those tests alone are not sufficient to guarantee a correct solution.
