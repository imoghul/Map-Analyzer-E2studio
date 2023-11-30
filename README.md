# MAP Analyzer Script

## Setup
To setup the script, go to the e2studio build steps settings and add the command under post-build steps.
An example is shown below:
``` bash
python "absolute/script/path" --rom ".text" --ram ".bss" ".data" --identifiers "./src/" "./QCIOT009"
```
## Usage
To use the script, make sure you have built the project and exported the csv files for usage under the "Memory Usage" view in e2studio. Then, after building again, you will see the usage. To make this fully automated, configure e2studio to automatically export the csv files for usage (if that is possible)
### Arguments

* --identifiers: any path that contains one of the identifiers will be looked at. All others are ignored
* --rom : These are all the labels that are under rom
* --ram : These are all the labels that are under ram

Keep in mind arguments aren't required and are defaulted to:
- --identifiers : "./src/"
- --rom : ".text"
- --ram : ".bss" ".data"

Note: If an entry's label doesn't match rom nor ram, it will throw an error. Make sure your rom and ram labels cover all possibilities