Title: Create from Template API parameters explained

URL Source: https://developers.gamma.app/docs/create-from-template-parameters-explained

Markdown Content:
What Create from Template API parameters represent and how they affect your Gamma creation. Read this before heading to the API Reference page.

> 🚧
> **Functionality, rate limits, and pricing are subject to change.**

The sample API requests below shows all required and optional API parameters, as well as sample responses.

```
curl --request POST \
     --url https://public-api.gamma.app/v1.0/generations/from-template \
     --header 'Content-Type: application/json' \
     --header 'X-API-KEY: sk-gamma-xxxxxxxx' \
     --data '
{
  "gammaId": "g_abcdef123456ghi",
  "prompt": "Rework this pitch deck for a non-technical audience.",
  "themeId": "Chisel",
  "folderIds": ["123abc456", "456def789"],
  "exportAs": "pdf"
  "imageOptions": {
    "model": "imagen-4-pro",
    "style": "photorealistic"
  },
  "sharingOptions": {
    "workspaceAccess": "view",
    "externalAccess": "noAccess",
    "emailOptions": {
      "recipients": ["email@example.com"],
      "access": "comment"
    }
  },
}
'
```

```
{
  "generationId": "yyyyyyyyyy"
}
```

```
{
  "message": "Input validation errors: 1. …",
  "statusCode": 400
}
```

```
{
  "message": "Forbidden",
  "statusCode": 403
}
```

```
curl --request GET \
     --url https://public-api.gamma.app/v1.0/generations/yyyyyyyyyy \
     --header 'X-API-KEY: sk-gamma-xxxxxxxx' \
     --header 'accept: application/json'
```

```
{
  "status": "pending",
  "generationId": "XXXXXXXXXXX"
}
```

```
{
  "generationId": "XXXXXXXXXXX",
  "status": "completed",
  "gammaUrl": "https://gamma.app/docs/yyyyyyyyyy",
  "credits":{"deducted":150,"remaining":3000}
}
```

```
{
  "message": "Generation ID not found. generationId: xxxxxx",
  "statusCode": 404,
  "credits":{"deducted":0,"remaining":3000}
}
```

Identifies the template you want to modify. You can find and copy the gammaId for a template as shown in the screenshots below.

![Image 1](https://files.readme.io/9464bbfb332e5c5798be313563bb9e0c91153fbb28bc88d4da79ac7a2faf865b-CleanShot_2025-11-03_at_15.10.362x.png)

![Image 2](https://files.readme.io/a5a8861282b3bf86679595b2cf684fce46ac54c0059f9ff19d7dcfd411e8aed7-CleanShot_2025-11-03_at_15.16.562x.png)

Use this parameter to send text content, image URLs, as well as instructions for how to use this content in relation to the template gamma.

**Add images to the input**

You can provide URLs for specific images you want to include. Simply insert the URLs into your content where you want each image to appear (see example below). You can also add instructions for how to display the images, eg, "Group the last 10 images into a gallery to showcase them together."

**Token limits**

The total token limit is 100,000, which is approximately 400,000 characters, but because part of your input is the gamma template, in practice, the token limit for your prompt becomes shorter. We highly recommend keeping your prompt well below 100,000 tokens and testing out a variety of inputs to get a good sense of what works for your use case.

**Other tips**

*   Text can be as little as a few words that describe the topic of the content you want to generate.
*   You can also input longer text -- pages of messy notes or highly structured, detailed text.
*   You may need to apply JSON escaping to your text. Find out more about JSON escaping and [try it out here](https://www.devtoolsdaily.com/json/escape/).

`"prompt": "Change this pitch deck about deep sea exploration into one about space exploration."`

`"prompt": "Change this pitch deck about deep sea exploration into one about space exploration. Use this quote and this image in the title card: That's one small step for man, one giant leap for mankind - Neil Armstrong, https://www.global-aero.com/wp-content/uploads/2020/06/ga-iss.jpg"`

Defines which theme from Gamma will be used for the output. Themes determine the look and feel of the gamma, including colors and fonts.

*   You can use the [GET Themes](https://developers.gamma.app/v1.0/update/docs/list-themes-and-folders-apis#/) endpoint to pull a list of themes from your workspace. Or you can copy over the themeId from the app directly.

![Image 3](https://files.readme.io/d01171ca7562e427d8469ee2d0391e54400235ca558d6da8e61cf35e957d8833-CleanShot_2025-11-03_at_14.24.272x.png)

`"themeId": "abc123def456ghi"`

Defines which folder(s) your gamma is stored in.

*   You can use the [GET Folders](https://developers.gamma.app/v1.0/update/docs/list-themes-and-folders-apis#/) endpoint to pull a list of folders. Or you can copy over the folderIds from the app directly.

![Image 4](https://files.readme.io/eefcb9b3f6404e96978f1a92aed2820c178ed1dbf550873c6e3da0538c466740-CleanShot_2025-11-03_at_14.27.362x.png)

*   You must be a member of a folder to be able to add gammas to that folder.

`"folderIds": ["123abc456", "def456789"]`

Indicates if you'd like to return the generated gamma as a PDF or PPTX file as well as a Gamma URL.

*   Options are `pdf` or `pptx`
*   Download the files once generated as the links will become invalid after a period of time.
*   If you do not wish to directly export to a PDF or PPTX via the API, you may always do so later via the app.

`"exportAs": "pdf"`

When you create content from a Gamma template, new images automatically match the image source used in the original template. For example if you used Pictographic images to generate your original template, any new images will be sourced from Pictographic.

For templates with AI-generated images, you can override the default AI image settings using the optional parameters below.

This field is relevant if the original template was created using AI generated images. The `imageOptions.model` parameter determines which model is used to generate new images.

*   You can choose from the models listed [here](https://developers.gamma.app/reference/image-model-accepted-values).
*   If no value is specified for this parameter, Gamma automatically selects a model for you.

```
"imageOptions": {
	"model": "flux-1-pro"
  }
```

This field is relevant if the original template was created using AI generated images. The `imageOptions.style` parameter influences the artistic style of the images generated.

*   You can add one or multiple words to define the visual style of the images you want.
*   Adding some direction -- even a simple one word like "photorealistic" -- can create visual consistency among the generated images.
*   Character limits: 1-500.

```
"imageOptions": {
	"style": "minimal, black and white, line art"
  }
```

Determines level of access members in your workspace will have to your generated gamma.

*   Options are: `noAccess`, `view`, `comment`, `edit`, `fullAccess`
*   `fullAccess`allows members from your workspace to view, comment, edit, and share with others.

```
"sharingOptions": {
	"workspaceAccess": "comment"
}
```

Determines level of access members **outside your workspace** will have to your generated gamma.

*   Options are: `noAccess`, `view`, `comment`, or `edit`

```
"sharingOptions": {
	"externalAccess": "noAccess"
}
```

Allows users to share gamma with specific recipients via their email.

```
"sharingOptions": {
  "emailOptions": {
    "recipients": ["ceo@example.com", "cto@example.com"]
}
```

Determines level of access users defined in `sharingOptions.emailOptions.recipients` have to your generated gamma.

*   Options are: `view`, `comment`, `edit`, or `fullAccess`

```
"sharingOptions": {
  "emailOptions": {
    "access": "comment"
}
```

Updated 15 days ago

* * *

*   [List Themes and List Folders APIs explained](https://developers.gamma.app/docs/list-themes-and-list-folders-apis-explained)