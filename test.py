import pymsteams
# You must create the connectorcard object with the Microsoft Webhook URL
myTeamsMessage = pymsteams.connectorcard("https://microsoft.webhook.office.com/webhookb2/e917a424-6a22-4931-b080-7f195a4e3ded@72f988bf-86f1-41af-91ab-2d7cd011db47/IncomingWebhook/deb085efd12941c0a8f8af31906fc2b9/ea2720f9-a5fb-478a-8aba-861af0de14db")
# Add text to the message.
myTeamsMessage.text("Sneha testing")
# send the message.
myTeamsMessage.send()