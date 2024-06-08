# adapted from: https://github.com/eclipse-ditto/ditto-examples/blob/master/mqtt-bidirectional/README.md

curl -X POST 'http://34.143.239.132:3000/devops/piggyback/connectivity' -u 'devops:foobar' -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
    	"aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:createConnection",
        "connection": {
            "id": "mqtt-example-connection-123",
            "connectionType": "mqtt",
            "connectionStatus": "open",
            "failoverEnabled": true,
            "uri": "tcp://test.mosquitto.org:1883",
            "sources": [{
                "addresses": ["ditto-tutorial/#"],
                "authorizationContext": ["nginx:ditto"],
                "qos": 0,
                "filters": []
            }],
            "targets": [{
                "address": "ditto-tutorial/{{ thing:id }}",
                "topics": [
                "_/_/things/twin/events",
                "_/_/things/live/messages"
                ],
                "authorizationContext": ["nginx:ditto"],
                "qos": 0
            }]
        }
    }
}'
