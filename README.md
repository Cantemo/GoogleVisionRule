Google Cloud Vision API enables developers to **understand the content of an image** by encapsulating 
**powerful machine learning models** in an easy to use REST API. It quickly **classifies images** into 
thousands of categories (e.g., "sailboat", "lion", "Eiffel Tower"), **detects individual objects and 
faces within images**, and finds and reads printed words contained within images. You can read more about Google Vision 
here - https://cloud.google.com/vision/

This Python script for Cantemo Portal Rules Engine 3 allows you to run Google Vision image analysis 
on images in Cantemo Portal.


# Example Results

A picture is worth a thousand words, so here are some example results using this script. These show that Google's API 
is very good at generating relevant labels automatically from nothing more then the image data. Also text is recognized
with high accuracy.

![Example 1 Sunset](gv_example_1.png?raw=true)

![Example 2 Dog](gv_example_2.png?raw=true)

![Example 3 A Sign with Text](gv_example_3.png?raw=true)

![Example 4 Snowboarding](gv_example_4.png?raw=true)

![Example 5 Scuba Diving](gv_example_5.png?raw=true)

# Prerequisites

* Cantemo Portal 2.3.0 or later, with license for Rules Engine
* Google Cloud Platform account with billing enabled, see https://cloud.google.com/
* Google Vision API key, see https://cloud.google.com/vision/docs/auth-template/cloud-api-auth

Google Vision API is free for up to 1000 requests/month, but a credit card is required when registering the project.
See https://cloud.google.com/vision/docs/pricing

# Installation

## Create a Metadata Group for analysis output

This example uses an explicit metadata group to store the analysis results. You could also add these fields into an 
existing metadata group.

1. From Portal GUI, open *Manage > Metadata Groups*
1. Add a metadata group with the name `GoogleVision`
1. Add one *Tags*-field for Label Detection results
1. Add two *Textarea*-fields, one for Text Detection results and one for raw API JSON output
1. Set *Max Length* on the Textarea fields to 1000000 so the output fits in them

Feel free to rename the fields to your liking, and write descriptions. The resulting group should look like this:

![GoogleVision metadata group](gv_metadata_group.png?raw=true)

## Get and configure the script

Download [google_vision.py](google_vision.py?raw=true) to your computer. Modify the local script file:

Add your own Google Vision API key on the following line, in brackets:
  
```
VISION_API_KEY = ''
```

For example:

```
VISION_API_KEY = 'AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AA'
```

Replace the metadata Field Ids in the script with those from the GoogleVision group you created in Portal, 
modifying these rows:

```
TAGS_FIELD = 'portal_mf572883'
OCR_FIELD = 'portal_mf915296'
FULL_OUTPUT_FIELD = 'portal_mf700776'
```

The script is now ready to be used in your Portal system.

## Create an automatic Rule to execute the script

1. Open *Admin > Rules Engine 3* in Portal
1. Under *Add a new script:* select your local `google_vision.py` file and select *Upload*
1. Select *Create rule for new items* to have this applied an all ingested images (with GoogleVision metadata group)
1. Enter a descriptive name for the rule
1. Enable *Run Shell Script* and select *google_vision.py* from the *Script file* dropdown
1. *Create rule*

![Create rule form](gv_create_rule.png?raw=true)

The rule can also be created as a Manual Rule, so it can be executed for example on search results page.

# Executing the script

This uploads an image to Portal with the metadata group set. After the ingest is completed the rule will be executed
and the item metadata contains the analysis results.

1. Select *Ingest > Upload*
1. Add some files to be uploaded
1. Select *Add Metadata*
1. From *Show advanced > Change metadata form*, select `GoogleVision
1. Select *Start Upload*

![File upload screen](gv_upload_file.png?raw=true)

A Raw import Job should be visible in *Admin > Jobs* for the new file. After the job has finished, the rule will be
automatically executed on the new item. This can be monitored from the Rules Engine 3 UI.

After the rule has finished, it should show *1* in *Handled items*. A link to the handled item is under *Details*. 
Open the item page to view the analysis results:

![Item metadata after analysis](gv_item_after_analysis.png?raw=true)

To really test the power of this API, upload some more interesting photos!

# License

BSD 3-Clause License
