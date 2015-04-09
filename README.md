# PyDloader
  A download manager for BITS Goa students to download files faster for files with direct links.
Installation
------------
  Run the following command:
  
    sudo pip install scapy netifaces commands
## How does it work?
  It works basically on the concept that cyberoam limits bandwidth per-ip basis. Hence, the more ips you have,
  the more bandwidth you have. This download manager basically searches for free ips in the subnet and automatically 
  assigns them for your computer as per you requirements.
### Steps
#### Step 1
  Run the PyDloader.py file as sudo user:
    
    PyDloader.py <url> <filename> <numofchunks> [-p <chunknumber to re-download>] [--help]
  **Note:** Be sure that "num of chunks" is same as the previous failed download.
#### Step 2
  The script searches for <numofchunks> number of ips that are free in the subnet and starts assigning them.
  Here, make sure that <numofchunks> is the number of user ids (of you and your friends) you have.
#### Step 3
  After assigning the ips to the host, the main part is to login into cyberoam from each ip. Presently, this is
  being done by taking input from user and wrong password will be prompted.
#### Step 4
  Once all ips are logged in, the final step is that the file starts downloading. Once completed, the part files
  are joined into the single file and automatically logs out from cyberoam.
## Troubleshooting
  **Problem:** One of the ip's data was finished in between the download. What to do?
  
  **Solution:** No problem, the script rechecks all the files for status and if not finished, it asks the user what 
  to do.
 
  **Problem:** I accidentally quit the script in the middle of download, what to do?
 
  **Solution:** No problem, just run the script again with the same parameters as before. The script checks for any
  previous instances of the downloaded file.
  