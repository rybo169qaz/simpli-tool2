# HOW TO TEST


## Approach


## Testing with pytest

### Setting up the environment


### PYTEST

#### Structure

For a module/class in a file called wanted_feature
This would contain a class called WantedFeature

In a file called test_wanted_feature
@pytest.mark.wantedtestcategory
class TestPullFromNetwork:


#### Runnnind tests

Running the main applications unit tests
cd ~/SIMPLI-TOOL/GIT-REPO/simpli-tool2/MySimpleApp/pyplay
clear ; pytest -v -x -m wantedtestcategory

where wantedtestcategory if in the code as 





To increase the logging level use additional x i.e.
clear ; pytest -v -xx -m wantedtestcategory

Running the utility tests:
cd ~/PROJ2/SIMPLI-TOOL/GIT-REPO/simpli-tool2/Deployment-Info/util
clear ; pytest -v -x -m legacy




