# Design Language

## The Paper Doesn't Introduce Itself

A page should not waste space identifying itself.

Information already known by the application should remain outside the page.

Only information that changes from page to page belongs on the page.

This principle applies consistently across the entire framework.

### Examples

- A template name is application metadata and should not be repeated on the page.
- A template ID, filename, notebook selection, and store entry already identify the document.
- Page metadata that changes per page, such as date, client, patient, meeting, employee, week, project, session, or topic, belongs on the page.

### Framework Rule

Templates should render page titles only when they explicitly opt in.

By default, page titles are disabled.

This preserves handwriting space and keeps the visual language focused on the user’s actual content.
