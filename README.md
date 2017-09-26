# MongoDB_Stress_Demo
A brief demo how MongoDB process the different size of Document

# Scope
What is the maximum docment size that MongoDB can handle, and what if the
document size exceed that value. After that, what would happen? also, what can
be the optimal document size that MongoDB handles best? The purpose of this
project is to make a demostration of such a scenario.

# Set up
## Installation of MongoDB
You should have current version of MongoDB installed on your system already. To
install, check out the following instruction.
### Linux Installation
Can be easily done with apt. If you don't use apt, then you propably already
know how to do it ;)
```
sudo apt update
sudo apt install mongodb
```
### Mac Installation
Can be done in similar way. But by using Homebrew.
```
brew update
brew install mongodb
```
### Windows Installation
Go to MongoDB official website and download the installer.
[MongoDB Windows Installer](https://www.mongodb.com/download-center#community)

# Run Benchmark
Todo

# Goodies
To Run MongoDB and storing documents in a designated directory.
```
mongod --dbpath /the/directory/you/want
```
