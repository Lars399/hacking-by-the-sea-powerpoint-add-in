# PowerPoint Add-in (Future)

This will use Office Add-ins (JavaScript + Office JS) for in-app accessibility checking.

## Setup
1. `npm init`
2. Use Yeoman generator for Office Add-in or manual manifest.xml

Key APIs:
- `Office.context.document` to access slides/shapes
- Check properties like altText, titles, etc.

See: https://learn.microsoft.com/en-us/office/dev/add-ins/
