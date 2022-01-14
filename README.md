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

* `energy_analyzer/models.py`: Provides a simple data model and all business logic for the Energy Analyzer.
* `energy_analyzer/energy_client.py`: Provides the stubbed API as mentioned above. It has two methods defined: 1) get the expected energy usage for a building and 2) get the expected energy savings for a measure. Read the doc string of `EnergyClient` methods for more detail.
* `energy_analyzer/test_biz_logic.py`: Tests and Fixtures for the Energy Analyzer business logic.


### Challenge Task

We've provided some half-finished code for you to complete. On the `Building` model, the method `get_past_and_future_year_of_monthly_energy_usage`
returns data ranging from one year in the past to one year in the future. It sums the 15m data returned by the EnergyClient for each month.
In its current implementation, it is unable to calculate measure savings.

For this task, you will implement the missing code in the `Measure` model method `get_savings_for_date_range`. This method should return measure 
savings for a measure over the given date range in 15 minute intervals. These savings will then be applied to the usage data in 
`get_past_and_future_year_of_monthly_energy_usage`. A correct solution will take into account the start and end times for each measure.

Note: We have provided some failing tests for this task. However, those tests alone are not sufficient to guarantee a correct solution.
