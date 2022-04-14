# Administrator Tutorial

## Introduction 

The RIR platform is a situational awareness platform to monitor health, child protection, nutrition, wash and education in a geographic region. To fully understand the platform and the information you can obtain from it, you need to understand how it works.


## Important Links
[RIR Platform](https://staging.rir.kartoza.com/ "RIR Platform") <br>
[RIR Full Documentation](https://kartoza.github.io/rir-dashboard/pages/introduction.html "RIR Full Documentation")  <br> <br>

## Session outline
In this session, we will tour the RIR administration functions using examples and workflows that would be used by site administrators. 

![image](https://user-images.githubusercontent.com/77841514/163354387-91e9ca4a-503b-4b23-b970-39b18d97cf79.png)

### Platform Administration: <br>
• User Management: Creating and editing user profiles. <br>
• Managing Instances: Creating new and editing preexisting instances.<br> 
• Managing Context Layers: Using layers that you have uploaded to GeoNode or GeoServer to create a context layer in the platform. <br>
•         Geography management: Adding geography levels to your instance.<br>

![image](https://user-images.githubusercontent.com/77841514/163354685-26adab94-984a-4545-a69e-82a42f213480.png)
 
### Indicator Management: <br>
 •         Ingestors: Adding data to create indicators for an instance. <br>
◦  Map <br>
◦   Form <br>
◦  Single Upload <br>
◦   Meta Upload <br>
 
•         Harvesters: Pulling data from an external source to create indicators for an instance. <br><br>

Admin Documentation [**Here**](https://kartoza.github.io/rir-dashboard/pages/administration/index.html "**Here**") <br> <br>

# Session Tutorial: <br><br>
1. **Signing In**:
In the top right-hand corner of the screen is the sign-in button. Here, you will sign in using your admin username and password. This process is the same for a staff user 
and an admin user. 
<br>![Signing in](../../img/login.gif "Signing in")<br><br>

2. **Users and Permissions**:
Go to site administration. “click” on ‘+Add’ in the same row as ‘Users’. You can now create a profile for someone by adding a username and password. Once you have created the user profile, “click” ‘Save’.
<br>![New User](../../img/new-user.gif "New User")<br><br>
Once you have created the user account, go back to ‘Site Administration’ and “select” the ‘user’ option. “Select” the user you created and then you can edit their personal information as well as select or deselect their ‘Permissions’. Remember to ‘Save’ your changes. 
<br>![Permissions](../../img/permissions.gif "Permissions")<br>

3.  **Creating an instance**: 
Once you’ve signed in, you’ll be redirected back to the home page which contains the various instances that you can select. To create a new Instance, select the
dropdown arrow next to your username and “click” on ‘Django Admin’. Once you’re on the ‘Site Administration’ page, “scroll” down until you find ‘Instances’. 
“Click” on the ‘+Add’ option on the right-hand side of the ‘Instances’ row. “Add” the name of the new instance, a description as well as the icon files 
and then “click” ‘Save’.
<br>![Creating a New Instance](../../img/new-instance.gif "Creating a New Instance")<br><br>
4.   **Adding a new Context layer**: To add a context layer to the dashboard, you need to push the data from an online server. To do this you will first need to upload the data to GeoNode or GeoServer
as well as a styled layer descriptor file (SLD). Let’s start by creating the SLD in QGIS. Once you’ve opened QGIS or the mapping software of your choice, upload the 
data to your canvas as you would normally do. Once the layers are added, use the ‘Layer Styling’ panel to create an appropriate style for the data. You want to follow
the general theme of the layers that are already on the dashboard. Once you are happy with the style “right-click” on the layer and “select” ‘Properties’. 
Go to ‘Symbology’ and “click” on the drop-down ‘Style’ button. “Select” ‘Save Style’. “Click” on the ‘Save Style’ drop-down option and “select” ‘As SLD Style File’.
“Click” on the ellipse on the right-hand side of the ‘File’ line to choose a place to save the SLD. Do this for each file you want to upload.
<br>  ![SLD](../../img/sld.gif  "SLD") <br> <br>
Now we’re going to upload it to GeoNode. Log into your GeoNode or GeoServer account. “Click” on the ‘Data’ dropdown. “Select” ‘Upload Layer’. Please note that
you can only upload one layer at a time. “Drop” all the data for the layer into the grey box and “select” ‘Upload files’.  <br>
![Uploading to GeoNode](../../img/geonode_upload.gif  "Uploading to GeoNode") <br><br>
Once the data has uploaded, “click” on ‘Edit Metadata’. “Fill” in as much of the metadata information as you have and then “click” ‘Return to Layer’. <br>
![Metadata](../../img/metadata.gif  "Metadata") <br> <br>
“Click” on ‘Editing Tools’. “Click” on ‘Upload’ under ‘Styles’. “Choose” your SLD file and then return to layer once again. In ‘Editing tools’ you can also
change the thumbnail for the layer by uploading a screenshot of the layer. <br>
![Adding SLD File](../../img/adding_sld.gif  "Adding SLD File") <br><br>
“Right-click” on the layer and “Select” ‘Inspect’. “Select” ‘Network’ and hard refresh the page. “Select" the web address for a tile from the layer
(usually the third option) but if you click on the address, you’ll be able to see if it is the right one). <br>
![Finding Link](../../img/finding_link.gif  "Finding Link") <br> <br>
Copy the link address and paste it into a notepad and change all the words in full capital letters to lower case letters. Use this edited link address as the URL when adding a new layer.  <br>
"Click" on the user dropdown menu and open 'Django Admin'. "Click" on '+Add' on the 'Context layers' line. "Select" the instance you would like to add the context layer to.
We will use the existing Somalia instance and Flood Hazard layer as an example. The layer shows areas that are prone to flooding. Enter information in the input boxes as 
shown in the images below and save your data once you are happy with it. "Click" on veiw site to see your new layer. You will be able to see your new layer in the 'Layers' menu. There is also an option to add other parameters to this layer. 
<br>![Context Layers](../../img/context-layer.png "Context Layers")<br>
![Context Layers](../../img/context-layer.gif "Context Layers")
5. **Adding a Geography level**: Let’s start in  ‘Site Administration’. “Scroll” down to ‘Geometry Level Instances’ and “select” ‘+Add’. “Add” the name and description to your instance. Go back to the main page of your instance. Below the ‘Program Interventions’ panel are three icons; ‘Indicator Management’, ‘Geography Management’, and ‘Instance Management’. 
	  	 “Click” on the ‘Geography Management’ icon. You will be redirected to the ‘Geography View’ map page and you will see that in the top right corner there is an '+uploader' button. "Select" this button and start filling in the form. The first thing you need to do is "add" the data for the geography level. Once the data is uploaded, you will be able to fill in the rest of the form.  Please note that the country level does not have a parent level. <br><br>
6.	**Adding a New Indicator**:
To add an indicator, “click” on ‘Indicator Management’ and go to ‘Create New'. Fill in the necessary information about the indicator you would like to create. 
Once you have filled out the form, "scroll down" to 'Scenario Rules' and add the parameters to match the indicator. you can also change the colour for each rule
by clicking on the colour block. "Click" 'Submit' once you are happy with the added information and scenario rules. If you add a dashbord link, you will see 
a black dot in the centre of the cirlce that represents the scenario case on that indicator in the 'Program Interventions' panel. By clicking on the black dot,
you will be redirected to the dashboard link. 
<br>![New Indicator](../../img/new-indicator.gif "New Indicator")<br>

7.	**Value Manager Form**:
There are two ways to manually add data to indicators. The first is by using the 'Value Manager Form'. To access this form, go to 'Indicator Management' and 
"scroll" to the indicator that you would like to add data to. On the right-hand side of the indicator's name, there will be a small 'Settings' symbol.
"Click on 'Settings' for the desired indicator and then "click" on 'Value Manager Form'. You will be redirected to a form that gives you all the geographic 
locations within the instantce and spaces to add values. You can also add a file to fill in the data by clicking 'Use File to Refill Form'
<br>![Value Manager Form](../../img/data-form.gif "Value Manager Form")<br><br>

8. **Value Manager Map**:
The second way to add data to an indicator is through the 'Value Manager Map' option. Go to 'Indicator Management' and "scroll" to the indicator that you would
like to add data to. On the right-hand side of the indicator's name, there will be a small 'Settings' symbol. "Click on 'Settings' for the desired indicator and
then "click" on 'Value Manager  Map'. This will take you back to the map canvas. Now you will be able to "click" on any geographic location within the instantce 
and a popup window will appear which will allow you to fill in value data for that location.
<br>![Value Manager Map](../../img/value-manager-map.gif "Value Manager Map")<br>

9.	**Harvesters**:
The process of creating a harvester is for the total automation fetching of data. Go to 'Indicator Management' and if you haven't already created the indicator you want to work with, start by doing that. Once the necessary indicator exists, 
"click" on the little 'Settings' icon on the right-hand side of the indicator name. "Select" the 'Create Harvester' option. "Pick" the type of harvester you would
like to create from the drop-down 'Harvester' (you will be presented with three options: 'API With Geogrphay Using Today's Date'; 'API With Geography And Date'; and 
'Harvested Using Exposed API By External Client'). The first two options are for the harvester and the third one is for the ingestor. For the 'API With Geogrphay Using Today's Date' and 'API With Geography And Date' options,  "fill" in the 'Attributes' portion of the form and then a popup window with a list of 
keys will appear; "drag" the green labels to their corresponding criteria. Double-check that in 'Geometry Mapping', 'From' matches 'To. "Select" 'Harvest Now'. You can 
"scroll" down to the log to see if your harvest is running in the background. Go to 'Indicator Management' and "click" on the little settings icon that you just 
created a harvester for and "select" 'Value Manager Map' to view your progress.
<br>![Harvester](../../img/harvester.gif "Harvester")<br><br>
To create a 'Meta Harvester', go to 'Indicator Management' and in the top right-hand corner of the page, there will be a 'Meta Harvester' option that you will 
need to "select". "fill" in 'Sheet name', 'Column name: administration code', and add the appropriate file. "Submit" your work. "Click" 'Report File' to view your work.
<br>![Harvester](../../img/meta-harvester.gif "Harvester")<br><br>

10.	**Ingestors**:
The function of an ingestor is to manually upload data which is then automatically ingested or pushed from a remote side. To start, "click" on 'Create Harvester"
as you did for the harvester options. "change" the type of harvester to 'Harvested using exposed API by external client'. "Add" necessary notes and "submit".
You will now be presented with an 'API URL' and a 'Token' that has been received from an external source. You now need to "push" the data from outside to the RIR 
dashboard. "Open" the API platform that you use to build and use API's. We used Postman. "Copy" over the URL and token to push the data to the RIR dashboard.
<br>![Ingestor](../../img/ingestor.gif "Ingestor") 




