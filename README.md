# Instructions

venv\Scripts\activate

# You are tasked with creating a basic test project in Django to facilitate automated invoice generation for a channel manager. The goal is to streamline the billing process for bookings, specifically for camping sites. Here are the detailed requirements:

    Basic Setup:
        Create a Django project with the following models:
            Campingplatz (representing a customer)
            Buchung (representing a booking)
        Use SQLite for simplicity.
        Populate the database with 100 sample bookings for a few camping sites using random travel dates and booking amounts from June 2024.

    Backend Functionality:
        Develop a backend interface where bookings can be viewed and manipulated.
        Add a page to generate invoices:
            Allow selection of bookings to generate invoices.
            Change the booking status to "abgerechnet" (billed) after simulating the invoice generation via API.
        Ensure that changes in billing status are logged, including the date and operator who made the change.

    Models and Fields:
        Buchung model should include:
            id, booking_number, status (initially set to "offen" - open)
            abrechnungsstatus with values like "Offen", "Storniert", "Ohne Berechnung", "Abgerechnet", "Gutschreiben", "Gutgeschrieben".
            commission_rate which can be overwritten.
        Campingplatz model should include fields necessary for integration with external billing systems (e.g., customer number).

    Invoice Generation Page:
        Options to:
            Create invoices for all open bookings up to a specified date.
            Generate credit notes for disputed bookings.
            Display and resend invoices that were not sent.
            View and resend any created invoices.
        Allow changing the commission rate and billing status before finalizing the invoice generation.

    Logging and History:
        Log every status change internally.
        Store generated invoices with details like:
            Camping site receiving the invoice.
            List of billed bookings.
            Status of the invoice (e.g., "Created", "Sent").
            Creation date and history of changes and sending status.

    Simulating API Interaction:
        Instead of actually calling an external API, simulate the process and update the status to "abgerechnet".

# No Mention of Deadlines

There is no specific deadline mentioned for submitting the task. However, you are expected to report your progress after 10 hours of work.
Billing Information

    You are currently being offered 25 Euros per hour for this freelance task.
    Your current salary of 3,500 Euros (gross) translates to an approximate hourly rate of 20 Euros.

Next Steps

    Set up the Django project and define the necessary models.
    Populate the database with sample data.
    Create the backend interface for viewing and manipulating bookings.
    Develop the invoice generation and status update functionalities.
    Ensure logging and history tracking for all changes.
    Simulate the external API interaction for invoice generation.
    Report progress after 10 hours of work.