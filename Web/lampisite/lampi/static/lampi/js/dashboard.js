
var client = new Keen({
  projectId: window_global['project_id'],
  readKey: window_global['read_key'] 
});

Keen.ready(function(){

  // Web User Engagement
  var engagement_funnel = new Keen.Dataviz()
    .el("#chart-01")
    .type('area-step')
    .height(315)
    .title("Web User Engagement (by Pageviews)")
    .notes("Last two weeks")
    .prepare();

  client
    .query("funnel", {
        steps: [
          {
            "actor_property": "user.uuid",
            "event_collection": "pageviews",
            "filters": [
                {
                    "operator": "eq",
                    "property_name": "url.info.path",
                    "property_value": "/lampi/"
                }
            ],
            "inverted": false,
            "optional": false,
            "timeframe": "this_14_days",
            "timezone": "UTC"
          },
          {
            "actor_property": "user.uuid",
            "event_collection": "pageviews",
            "filters": [
                {
                    "operator": "eq",
                    "property_name": "url.info.path",
                    "property_value": "/lampi/add/"
                }
            ],
            "inverted": false,
            "optional": false,
            "timeframe": "this_14_days",
            "timezone": "UTC"
           },
          {
            "actor_property": "user.uuid",
            "event_collection": "pageviews",
            "filters": [
                {
                    "operator": "contains",
                    "property_name": "url.info.path",
                    "property_value": "/lampi/device/"
                }
            ],
            "inverted": false,
            "optional": false,
            "timeframe": "this_14_days",
            "timezone": "UTC"
           },
        ],
        })
    .then(function(res) {
        engagement_funnel
            .data(res)
            .labels([
                 "/lampi",
                 "/lampi/add",
                 "/lampi/device/",
                ])
            .render();
        console.log("funnel data: ", res);
        });

  // Devices By Zip
  var devices_by_zip = new Keen.Dataviz()
    .el("#chart-02")
    .type("bar")
    .height(315)
    .title('Devices by Zip Code')
    .notes('Previous 10 years')
    .prepare();

  client
    .query('count_unique', {
        event_collection: "ui",
        filters: [
            {
                "operator": "eq",
                "property_name": "lampi.ui",
                "property_value": "lampi"
            },
        ],
        group_by: [
            "geo.postal_code",
        ],
        target_property: "lampi.device_id",
        timeframe: "this_10_years"
        })
    .then(function(res) {
        devices_by_zip
            .data(res)
            .render();
        });

  // Usage by Browser
  var pageviews_timeline = new Keen.Dataviz()
    .el("#chart-03")
    .type('area')
    .height(190)
    .title("Usage by Browser")
    .notes("Last two weeks")
    .prepare();

  client
    .query('count', {
        event_collection: "pageviews",
        group_by: "tech.browser.family",
        interval: "daily",
        timeframe: "this_14_days"
    })
    .then(function(res) {
        pageviews_timeline
            .data(res)
            .render();
    });

  // User Interface Type
  var ui_type_timeline = new Keen.Dataviz()
    .el("#chart-04")
    .type('area')
    .height(190)
    .title("Usage by Interface")
    .notes("Last two weeks")
    .prepare();

  client
    .query('count', {
        event_collection: "ui",
        group_by: "lampi.ui",
        interval: "daily",
        timeframe: "this_14_days"
    })
    .then(function(res) {
        ui_type_timeline
            .data(res)
            .render();
    });

  var device_activations = new Keen.Dataviz()
    .el("#chart-05")
    .type('metric')
    .height(190)
    .title('Activations')
    .notes("")
    .prepare();

  client
    .query("count_unique", {
        event_collection: "activations",
        target_property: "device_id",
        timeframe: "this_10_years",
    })
    .then(function(res) {
        device_activations
            .data(res)
            .render();
    }); 

  // Device Interactions Per Day
  var device_interactions = new Keen.Dataviz()
    .el("#chart-06")
    .type('bar')
    .height(190)
    .title('Device Interactions Per Day')
    .notes('Last Wek')
    .prepare();

  client
    .query('count', {
        event_collection: "ui",
        filters: [
            {
                "operator": "eq",
                "property_name": "lampi.ui",
                "property_value": "lampi",
            }
        ],
        group_by: [
            "timestamp.info.day_of_week_string"
        ],
        timeframe: "this_7_days",
        })
    .then(function(res) {
        device_interactions
            .data(res)
            .render();
        });

  // Average Brightness By Day

  var average_brightness = new Keen.Dataviz()
    .el("#chart-07")
    .type('linechart')
    .height(190)
    .title("Average Brightness by Day")
    .notes("Previous two weeks")
    .prepare();

  client
    .query('average', {
        event_collection: 'devicestate',
        filters: [
            {
                "operator": "eq",
                "property_name": "state.on",
                "property_value": true
            }
        ],
        group_by: [
            "timestamp.info.day_of_week_string"
        ],
        target_property: "state.brightness",
        timeframe: "this_7_days",
        })
    .then(function(res) {
        average_brightness
            .data(res)
            .render();
    });

  // Device Disconnections
  var device_disconnections = new Keen.Dataviz()
    .el('#chart-08')
    .type('bar')
    .height(190)
    .title('Total Device Disconnections Per Day')
    .notes('Last week')
    .prepare();

  client
    .query('count', {
       event_collection: "devicemonitoring",
        filters: [
            {
                "operator": "eq",
                "property_name": "service",
                "property_value": "mqttbridge"
            },
            {
                "operator": "eq",
                "property_name": "state",
                "property_value": "disconnected"
            },
        ],
        group_by: [
            "timestamp.info.day_of_week_string"
        ],
        timeframe: "this_7_days",
        })
    .then(function(res) {
        device_disconnections
            .data(res)
            .render();
    });

});
