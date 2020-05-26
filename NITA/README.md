# Toby Shared Library
> Repository for shared libraries and engines of the Toby test automation framework

Directories in this repository hold the Python libraries and associated files which implement the shared infrastructure of the Toby project.
These are the main components:
 - **HLDCL** - High Level Device Control Library.  
 - **Init Engine**
 - **Config Engine**
 - **Verification Engine**
 - **Monitoring Engine**
 - **Logging**
 - **Traffic Generators**
 - **Robot Keywords**

## Directory structure

The `lib/jnpr/toby` directory holds the Python code for these different modules.
 - `lib/jnpr/toby/hldcl` : HLDCL
 - `lib/jnpr/toby/init` : Init Engine
 - `lib/jnpr/toby/engines/config` : Config Engine
 - `lib/jnpr/toby/engines/verification` : Verification Engine
 - `lib/jnpr/toby/engines/monitor` : Monitoring Engine
 - `lib/jnpr/toby/logger` : Logger
 - `lib/jnpr/toby/trafficgen` : Spirent and Ixia Traffic Generators
 - `lib/jnpr/toby/utils` : Various utility functions and common variables

The Robot Keywords which implement test modules for different Junos features are organized according to the Pathfinder/Feature Navigator taxonomy.  
The top level directories `cos`, `firewall`, `hardware`, interfaces`, `protocols`, `security`, `services`, `software`, `switching` and `system`.

The `tests/unit` directory holds the unit tests for the different python code modules under lib/jnpr/toby.
The tests under `tests/unit` should be organized in parallel with the source modules under `lib/jnpr/toby`.
It is Mandatory to have a UT file for all python libary being committed to toby repo.
Please refer to [Python Unit Test Development Document](https://junipernetworks.sharepoint.com/sites/Projects1/toby/_layouts/15/DocIdRedir.aspx?ID=PROJ1DOCID-25970584-123) and sample UT files in repo.

## Creating a code module

- Clone this repository
- Create a branch on the cloned reposiotry to commit your changes.
- Its also recommended to use Sparse Checkout to checkout specific files/folders to work with, without checking out whole repo. The instructions for the same can be found [here](https://junipernetworks.sharepoint.com/sites/Projects1/toby/controlled/Forms/AllItems.aspx?id=%2Fsites%2FProjects1%2Ftoby%2Fcontrolled%2Fgit_sparse_checkout%2Etxt&parent=%2Fsites%2FProjects1%2Ftoby%2Fcontrolled&p=5)
- API Design guidelines for the same are [here](https://junipernetworks.sharepoint.com/sites/Projects1/toby/_layouts/15/WopiFrame.aspx?sourcedoc=%7b40BA4EC9-ED2A-43AA-903F-240646A4AF5F%7d&file=Toby_api_guidelines.docx&action=default)
- If needed, create suitable sub-directories to hold the modules you are creating
- Be sure to write unit tests, **targeting 100% code coverage**, for all Python code modules you are adding to this repository
- Be sure to follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) when writing your code

_There are also [instructions for using Git with the test-suites repo](https://git.juniper.net/Juniper/test-suites/wikis/git-step-by-step) that can be easily adapted to work with this repository._

## Checking correctness and readiness

The below list describes the steps you should take to run the CI pipeline stages in your sandbox.
The quoted commands will run all tests, run pylint over the entire file, etc.
You may choose to run the equivalent commands by first establishing a development environment with `tox -e devenv; cd devenv` and then running the specific commands..
- Run your unit tests and ensure there are no errors or failures
  - `tox -e pytest` or `tox -e nose`
- Ensure 100% line coverage for all code you have added
  - `tox -e coverage`
- Run pylint ove your code, and achieve a score of 9.5 with no warning or error flags supressed. We’ve set character width to 120 in our pylintrc, so please do use the same
  - `pylint --rcfile=/volume/labtools/lib/pylintrc <filename>`
- Ensure that all public APIs have [appropriate docstrings](https://google.github.io/styleguide/pyguide.html#Comments). 
  - `tox -e docs; open docs/build/html/index.html`
- In particular, you must document:
  - All input params, including type information
  - All return values
  - Any exceptions that may be generated

## Review process
A merge request will be raised to merge the code from your branch to master branch.You need to add one or more reviewers to review the code. Reviewers will be the respective area's SMEs listed at [technology ownership](https://rbu.juniper.net/jdi-test-dashboard/#/technology-ownership-sme)


More Toby documentation can be foung at [Sharepoint page](https://junipernetworks.sharepoint.com/sites/Projects1/toby/_layouts/15/start.aspx#/Wiki)