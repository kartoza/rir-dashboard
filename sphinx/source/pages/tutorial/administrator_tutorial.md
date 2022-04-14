# Administrator Tutorial

## Introduction

The RIR platform is a situational awareness platform to monitor health, child protection, nutrition, wash and education in a geographic region. To fully understand the platform and the information you can obtain from it, you need to understand how it works.


### Working with this documentation

Whenever you see a phrase in **bold**, it refers to a link or button on the user interface that you can interact with.

### Important Links

* [RIR Platform](https://staging.rir.kartoza.com/ "RIR Platform")
* [RIR Full Documentation](https://kartoza.github.io/rir-dashboard/pages/introduction.html "RIR Full Documentation")  

### Session Outline

In this session, we will tour the RIR administration functions using examples and workflows that would be used by site administrators. 

![image](https://user-images.githubusercontent.com/77841514/163354387-91e9ca4a-503b-4b23-b970-39b18d97cf79.png)

### Platform Administration

We will cover the following adminstrative tasks:

* User Management: Creating and editing user profiles. 
* Managing Instances: Creating new and editing preexisting instances. 
* Managing Context Layers: Using layers that you have uploaded to GeoNode or GeoServer to create a context layer in the platform. 
* Geography management: Adding geography levels to your instance.
* Indicator management: Adding indicators to the dashboard and harvesting data for indicators.


![image](https://user-images.githubusercontent.com/77841514/163354685-26adab94-984a-4545-a69e-82a42f213480.png)
 
## Session Tutorial

### **Signing In**

In the top right-hand corner of the screen is the **Sign In** button. Here, you will sign in using your admin username and password. This process is the same for a staff user and an admin user.

![Signing in](../../img/login.gif "Signing in")

### **Users and Permissions**

Next we will look at how to manage users. Go to site administration by clickng **Admin -> Django Admin**. Click on **+Add** in the same row as ‘Users’. You can now create a profile for someone by adding a username and password. Once you have created the user profile, “click” ‘Save’.

![New User](../../img/new-user.gif "New User")
Once you have created the user account, go back to ‘Site Administration’ and select the ‘user’ option. Select the user you created and then you can edit their personal information as well as select or deselect their ‘Permissions’. Remember to ‘Save’ your changes.

![Permissions](../../img/permissions.gif "Permissions")

### **Creating an instance**

Once you’ve signed in as an admin user, you will be redirected back to the home page which contains the various instances that you can select. To create a new instance, select the dropdown arrow next to your username and click on **Django Admin**. Once you’re on the ‘Site Administration’ page, scroll down until you find **Instances**. 
“Click” on the ‘+Add’ option on the right-hand side of the ‘Instances’ row. “Add” the name of the new instance, a description as well as the icon files 
and then “click” ‘Save’.
![Creating a New Instance](../../img/new-instance.gif "Creating a New Instance")
###   **Adding a new Context layer**

In this section we will explain how to create and manage context layers. Context layers are shown on the map to provide a sense of the conditions in the region. They can cover any topic - for example, security, food security, infrastructure etc. Context layers do not have indicator data attached, they are a visual aid in the dashboard map.

To add a context layer, you need a link to an online layer. This can be hosted as a Web Map Service layer or an ESRI ArcGIS Online Layer. For this exercise will use the data at this link:

> https://foo.bar

Now we can go ahead and create the context layer in the RIR platform. 
Copy the link address above and paste it into a notepad and change all the words in full capital letters to lower case letters. Use this edited link address as the URL when adding a new layer.  
"Click" on the user dropdown menu and open 'Django Admin'. "Click" on '+Add' on the 'Context layers' line. "Select" the instance you would like to add the context layer to.


We will use the existing Somalia instance and Flood Hazard layer as an example. The layer shows areas that are prone to flooding. Enter information in the input boxes as shown in the images below and save your data once you are happy with it. "Click" on veiw site to see your new layer. You will be able to see your new layer in the 'Layers' menu. There is also an option to add other parameters to this layer.

![Context Layers](../../img/context-layer.png "Context Layers")
![Context Layers](../../img/context-layer.gif "Context Layers")

## Geography Management

### **Adding a Geography level**

Let’s start in  ‘Site Administration’. “Scroll” down to ‘Geometry Level Instances’ and “select” ‘+Add’. “Add” the name and description to your instance. Go back to the main page of your instance. Below the ‘Program Interventions’ panel are three icons; ‘Indicator Management’, ‘Geography Management’, and ‘Instance Management’.

“Click” on the ‘Geography Management’ icon. You will be redirected to the ‘Geography View’ map page and you will see that in the top right corner there is an '+uploader' button. "Select" this button and start filling in the form. The first thing you need to do is "add" the data for the geography level. Once the data is uploaded, you will be able to fill in the rest of the form.  Please note that the country level does not have a parent level.

### **Adding a New Indicator**

To add an indicator, “click” on ‘Indicator Management’ and go to ‘Create New'. Fill in the necessary information about the indicator you would like to create.

Once you have filled out the form, "scroll down" to 'Scenario Rules' and add the parameters to match the indicator. you can also change the colour for each rule by clicking on the colour block. "Click" 'Submit' once you are happy with the added information and scenario rules. If you add a dashbord link, you will see a black dot in the centre of the cirlce that represents the scenario case on that indicator in the 'Program Interventions' panel. By clicking on the black dot, you will be redirected to the dashboard link.

![New Indicator](../../img/new-indicator.gif "New Indicator")

### **Value Manager Form**

There are two ways to manually add data to indicators. The first is by using the 'Value Manager Form'. To access this form, go to 'Indicator Management' and "scroll" to the indicator that you would like to add data to. On the right-hand side of the indicator's name, there will be a small 'Settings' symbol.
"Click on 'Settings' for the desired indicator and then "click" on 'Value Manager Form'. You will be redirected to a form that gives you all the geographic locations within the instantce and spaces to add values. You can also add a file to fill in the data by clicking 'Use File to Refill Form'

![Value Manager Form](../../img/data-form.gif "Value Manager Form")

### **Value Manager Map**

The second way to add data to an indicator is through the 'Value Manager Map' option. Go to 'Indicator Management' and "scroll" to the indicator that you would like to add data to. On the right-hand side of the indicator's name, there will be a small 'Settings' symbol. "Click on 'Settings' for the desired indicator and then "click" on 'Value Manager  Map'. This will take you back to the map canvas. Now you will be able to "click" on any geographic location within the instantce and a popup window will appear which will allow you to fill in value data for that location.

![Value Manager Map](../../img/value-manager-map.gif "Value Manager Map")

### **Ingestors**

The function of an ingestor is to manually upload data which is then automatically ingested or pushed from a remote side. To start, "click" on 'Create Harvester" as you did for the harvester options. "change" the type of harvester to 'Harvested using exposed API by external client'. "Add" necessary notes and "submit".
You will now be presented with an 'API URL' and a 'Token' that has been received from an external source. You now need to "push" the data from outside to the RIR dashboard. "Open" the API platform that you use to build and use API's. We used Postman. "Copy" over the URL and token to push the data to the RIR dashboard.

![Ingestor](../../img/ingestor.gif "Ingestor")

### **Harvesters**

The process of creating a harvester is for the total automation fetching of data. Go to 'Indicator Management' and if you haven't already created the indicator you want to work with, start by doing that. Once the necessary indicator exists, 
"click" on the little 'Settings' icon on the right-hand side of the indicator name. "Select" the 'Create Harvester' option. "Pick" the type of harvester you would
like to create from the drop-down 'Harvester' (you will be presented with three options: 'API With Geogrphay Using Today's Date'; 'API With Geography And Date'; and 
'Harvested Using Exposed API By External Client'). The first two options are for the harvester and the third one is for the ingestor. For the 'API With Geogrphay Using Today's Date' and 'API With Geography And Date' options,  "fill" in the 'Attributes' portion of the form and then a popup window with a list of 
keys will appear; "drag" the green labels to their corresponding criteria. Double-check that in 'Geometry Mapping', 'From' matches 'To. "Select" 'Harvest Now'. You can 
"scroll" down to the log to see if your harvest is running in the background. Go to 'Indicator Management' and "click" on the little settings icon that you just 
created a harvester for and "select" 'Value Manager Map' to view your progress.

![Harvester](../../img/harvester.gif "Harvester")
To create a 'Meta Harvester', go to 'Indicator Management' and in the top right-hand corner of the page, there will be a 'Meta Harvester' option that you will 
need to "select". "fill" in 'Sheet name', 'Column name: administration code', and add the appropriate file. "Submit" your work. "Click" 'Report File' to view your work.
![Harvester](../../img/meta-harvester.gif "Harvester")


