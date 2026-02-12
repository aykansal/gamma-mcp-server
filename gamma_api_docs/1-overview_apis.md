Title: Understand the API options

URL Source: https://developers.gamma.app/docs/understand-the-api-options

Markdown Content:
Overview of the different API offerings and when to use each.

> 🚧
> **Functionality, rate limits, and pricing are subject to change.**

There are two ways to create gammas using our APIs: generate from scratch ([Generate API](https://developers.gamma.app/v1.0/docs/generate-api-parameters-explained#/) and create based on an existing template ([Create from Template API](https://developers.gamma.app/v1.0/docs/create-from-template-parameters-explained#/)).

| Callouts | Generate API | Create from Template API |
| --- | --- | --- |
| When to use | * Create a net new gamma (without an existing template). * Users have maximum flexibility to specify parameters. * Gamma uses full range of tools within defined parameters to create the output. | * Create a new gamma based on an existing gamma template. * Allows users to define a good template with the Gamma app. * Gamma adapts new content to the existing template. |
| Important distinctions | * Has many parameters to provide users maximum flexibility. * Use `inputText` to pass in text content and image URLs. Use other parameters to pass in more guidance. | * Requires an existing gamma template and its gammaId. * Use `prompt` to pass in text content, image URLs, as well as instructions for how to use this content. |

Additionally, you can use [GET Themes and GET Folders APIs](https://developers.gamma.app/v1.0/docs/list-themes-and-list-folders-apis-explained#/) to retrieve all available options for themes and folders.

Updated 15 days ago

* * *

*   [Generate API parameters explained](https://developers.gamma.app/docs/generate-api-parameters-explained)

Did this page help you?