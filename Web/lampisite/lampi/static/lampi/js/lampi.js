const hostAddress = window_global['mqtt']['hostname'];
const hostPort = window_global['mqtt']['websockets_port'];
const clientId = Math.random() + "_web_client";
const username = window_global['device_id'];
const password = window_global['session_key'];
const deviceId = window_global['device_id'];

function setup_analytics(obj) {
    var page_description = '';

    meta_description = $("meta[name='description']");
    if(meta_description.length > 0 ) {
        page_description = meta_description[0].content;
    }

    var keenClient = new Keen({
            projectId: window_global['project_id'],
            writeKey: window_global['write_key']
        });

    var sessionCookie = Keen.utils.cookie('keen');
    if (!sessionCookie.get('uuid')) {
        sessionCookie.set('uuid', Keen.helpers.getUniqueId());
    }

    var sessionTimer = Keen.utils.timer();
    sessionTimer.start();

    Keen.listenTo({
        'click #power': function(e) {
            // 500ms to record event
            keenClient.recordEvent('ui', {
            'element': {
                id: e.target.id,
                value: obj.lampState.on,
            },
        });
        },
        'change .slider': function(e) {
            // 500ms to record event
            keenClient.recordEvent('ui', {
            'element': {
               id:  e.target.id,
               value: Number(e.target.value),
            },
        });
        },
        'input .slider': function(e) {
            // 500ms to record event
            keenClient.recordEvent('ui', {
            'element': {
               id:  e.target.id,
               value: Number(e.target.value),
            },
        });
        },
    });

    keenClient.extendEvents(function(){
        return {
            user_agent: '${keen.user_agent}',
            tracked_by: 'lampi.js',
            referrer: {
                // info: add_on
                full: document.referrer,
            },
            // geo: add_on
            geo: {
            },
            tech: {
                profile: Keen.helpers.getBrowserProfile(),
                // device, os, browser: add-on
            },
            url: {
                // info: add_on
                full: document.location.href
            },
            time: {
                // utc, local add_on
            },
            ip_address: '${keen.ip}',
            page: {
                title: document.title,
                description: page_description, 
            },
            local_time_full: new Date().toISOString(),
            user: {
                uuid: sessionCookie.get('uuid'),
            },
            lampi: {
                device_id: window_global['device_id'],
                ui: 'web',
            },
            keen: {
                timestamp: new Date().toISOString(),
                addons: [
                  {
                    "name": "keen:ip_to_geo",
                    "input": {
                      "ip": "ip_address"
                    },
                    "output" : "geo"
                  },
                  {
                    "name": "keen:ua_parser",
                    "input": {
                      "ua_string": "user_agent"
                    },
                    "output": "tech"
                  },              
                  {
                    "name": "keen:url_parser",
                    "input": {
                      "url": "url.full"
                    },
                    "output": "url.info"
                  },
                  {
                    "name": "keen:url_parser",
                    "input": {
                      "url": "referrer.full"
                    },
                    "output": "referrer.info"
                  },
                  {
                    "name": "keen:date_time_parser",
                    "input": {
                      "date_time": "keen.timestamp"
                    },
                    "output": "time.utc"
                  },
                  {
                    "name": "keen:date_time_parser",
                    "input": {
                      "date_time": "local_time_full"
                    },
                    "output": "time.local"
                  }
                ]
            }
        };
    });
}

function LampiPage($){

    console.log(clientId);

    obj = {
        connect : function() {
          obj.client.connect({onSuccess: obj.onConnect,
            onFailure: obj.onFailure,
            useSSL:true,
            userName: username, password: password });
        },

        onFailure : function(response) {
          console.log(response);
        },

        onConnect : function(response) {
          obj.client.subscribe("devices/" + deviceId + "/lamp/changed", {qos:1});
          obj.client.subscribe("$SYS/broker/connection/" + deviceId + "_broker/state", {qos:1});
        },

        onConnectionLost : function(responseObject) {
          if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:" + responseObject.errorMessage);
            obj.connect();
          }
        },

        onMessageArrived : function(message) {
            if (message.destinationName.endsWith('state')) {
                obj.onMessageConnectionState(message);
            } else if (message.destinationName.endsWith('changed')) {
                obj.onMessageLampChanged(message);
            } 
        },

        onMessageConnectionState: function(message) {
            if (message.payloadString == "1" ) {
                console.log("Device Connected");
                $.unblockUI();
            } else {
                console.log("Device Disconnected");
                $.blockUI( {message: '<h1>This LAMPI device does not ' +
                            'seem to be connected to the Internet.</h1>' +
                            '<p>Please make sure it is powered on ' +
                            'and connected to the network.</p>' });
            }
        },

        onMessageLampChanged: function(message) {
            new_lampState = JSON.parse(message.payloadString);
            console.log(new_lampState)
            if (obj.updated && new_lampState.client == clientId) {
                return;
            }
            obj.lampState.color.h = new_lampState.color.h;
            obj.lampState.color.s = new_lampState.color.s;
            obj.lampState.brightness = new_lampState.brightness;
            obj.lampState.on = new_lampState.on;
            obj.updateUI();
            obj.updated = true;
        },

        onPowerToggle : function(inputEvent) {
          obj.lampState.on = !obj.lampState.on;
          obj.updatePowerButton();
          obj.scheduleConfigChange();
        },

        onSliderInput : function(inputEvent) {
          value = Number(inputEvent.target.value);

          if(inputEvent.target.id == "hue-slider") {
            obj.lampState.color.h = value;
          } else if(inputEvent.target.id == "saturation-slider") {
            obj.lampState.color.s = value;
          } else if(inputEvent.target.id == "brightness-slider") {
            obj.lampState.brightness = value;
          }

          obj.scheduleConfigChange();
          obj.updateUIColors();
        },

        scheduleConfigChange : function() {
          function onTimeout() {
            obj.updateTimer = null;
            obj.sendConfigChange();
          }

          if(obj.updateTimer == null) {
            obj.updateTimer = setTimeout(onTimeout, 100);
          }
        },

        sendConfigChange : function() {
          configJson = JSON.stringify(obj.lampState);

          message = new Paho.MQTT.Message(configJson);
          message.destinationName = "devices/" + deviceId + "/lamp/set_config";
          message.qos = 1;
          obj.client.send(message);
        },

        updateUI : function() {
          if(obj.isManipulatingSlider) {
            return;
          }

          setSliderValues(obj.lampState.color.h,
            obj.lampState.color.s,
            obj.lampState.brightness);
          obj.updatePowerButton();
          obj.updateUIColors();
        },

        updateUIColors : function() {
          updateSliderStyles(obj.lampState.color.h,
            obj.lampState.color.s,
            obj.lampState.brightness);
          obj.updateColorBox(obj.lampState.color.h, obj.lampState.color.s);
        },

        updatePowerButton : function() {
          opacity = obj.lampState.on ? 1.0 : 0.3;
          $( "#power" ).fadeTo(0, opacity);
          $( "#power" ).css("color", "#ff0000");
        },

        updateColorBox : function(hue, saturation) {
          color = tinycolor({ h:hue * 360, s:saturation, v:1.0 });
          hexColor = color.toHexString();
          $( "#colorbox" ).css("background-color", hexColor);
        },

        lampState : {
            color : {
                h: "50",
                s: "50"
            },
            brightness : "50",
            on: true,
            client: clientId
        },
        client : new Paho.MQTT.Client(hostAddress, Number(hostPort),
            clientId),
        updateTimer : null,
        isManipulatingSlider :false,
        updated: false,

        init : function() {

            if( deviceId == "") {
                alert("PLEASE FILL IN THE 'deviceId' VARIABLE IN 'lampi.js'," +
                      " SAVE, AND REFRESH THE PAGE.  THE PAGE WILL NOT WORK " +
                      "CORRECTLY UNTIL YOU DO!");
                return;
            }

            setSliderValues(obj.lampState.color.h,
                obj.lampState.color.s,
                obj.lampState.brightness);

            obj.client.onConnectionLost = obj.onConnectionLost;
            obj.client.onMessageArrived = obj.onMessageArrived;

            obj.connect();

            $( "#power" ).click(obj.onPowerToggle);
            $( ".slider" ).on( "change input", obj.onSliderInput);
            $( ".slider" ).on( "mousedown touchstart", function() {
                obj.isManipulatingSlider = true; });
            $( window ).on( "mouseup mousecancel touchend touchcancel", function() {
                obj.isManipulatingSlider = false; });
        },
    };

    obj.init();
    setup_analytics(obj);
    return obj;
}

jQuery(LampiPage);



