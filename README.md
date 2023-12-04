# The Architecture of the Application

The client/server application follows an **MVC (Model-View-Controller) architecture**. This architecture is implemented using the Flask Python framework, which is known for not being prescriptive on the design of the application. Implementing this pattern in our application comes with the following benefits:

1. **Separation of Concerns**: Each part of the application has its own responsibility, making the code easier to understand and maintain.
2. **Modularity and Reusability**: Code is organized into modules that can be reused across different parts of the application.
3. **Easier Collaboration**: Different team members can work on different parts of the application without stepping on each other's toes.

## Models

Models return data for various entities and are used to get the data for different features.

1. **Person Model**: Returns data for the Person entity. Used for the search person feature.
2. **Link Model**: Returns data for the Link entity. Used for the search link feature.
3. **Event Model**: Returns data for the Event entity. Used for the all event features.

## Views

Views are used for rendering templates with the data from the models, passed using a controller.

1. **Person View**: Used with the Person Model.
2. **Link View**: Used with the Link Model.
3. **Event View**: Used with the Event Model.

## Controllers

Controllers handle requests for various endpoints and pass the data from the models to the views.

1. **Person Controller**: Handles requests for the search-person endpoint.
2. **Link Controller**: Handles requests for the search-link endpoint.
3. **Event Controller**: Handles requests for the all-event endpoints.
