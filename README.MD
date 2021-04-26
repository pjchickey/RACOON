# Rice 2020-2021 ECE Senior Design Project

Project RACOON is a safe, affordable, and easy to use device to reduce contamination in recycling loads. 

##Code Structure

The Github is broken up into 4 main folders: 

- Algorithm: Contains the core functionality for our machine learning classifier and tensor flow lite model
- Scripts: Contains necessary program flow and testing scripts for the operation of the Raspberry Pi and handling of the data
- Sensors: Contains all Arduino and Raspberry Pi code needed to interface with the sensors of the device
- Images: Contains our custom 1500 image dataset which we have used for training our model

## Data Collection

During the course of our project, we developed a script (Scripts/image-taker.py) to allow our team to view, take, and classify pictures of objects rapidly. 
1. First, the ip address of the pi is needed
2. The script is then run, and the user navigates to the ip address of the pi on their web browser
3. The user can now see a viewfinder for the camera, take/retake pictures, and classify them according to our categories

## Images

Although we collected our data in backgrounds more similar to our device (gray/metal floor), we believe that this labeled data can be useful to projects aiming to accomplish similar goals. For that reason, all of the images in our dataset are free to use (with attribution) by future students, researchers, and organizations. 

The data is labeled as follows: 

<objectname><index>--<object weight in grams>.jpg (Ex: cokecan3--4_8.jpg for the 4th picture of a coke can (this one weighs 4.8grams))

All of our images are sorted into different categories, to allow training on more detailed descriptors of the objects, as well as allowing simple changing of model training should standards change (EX: If plastic bottles are no longer classified as Recycling)

### Recycleable Categories:
  - Paper-Newspapers
  - Paper-Office
  - Paper-Magazines
  - Paper-Junk_Mail
  - Paper-Other
  - Plastic-Bottles
  - Plastic-Other
  - Cardboard-Boxes
  - Cardboard-Other
  - Steel_and_Tin
  - Aluminum
  - Glass
 
### NonRecycleable Categories:
  - Plastic_Bags
  - Plastic_Wrap
  - No_6_Plastics
  - Plasticware
  - Plastic_Straws
  - Drink_Cartons
  - Paper_Cups
  - Food_Waste
  - Styrofoam
  - Pizza_Boxes
  - Dirty_Food_Containers
  - Other
