curl -X PUT 'http://34.143.239.132:3000/api/2/policies/default:basic_policy' -u 'ditto:ditto' -H 'Content-Type: application/json' -d '{
    "policyId": "default:basic_policy",
    "entries": {
        "DEFAULT": {
            "subjects": {
                "nginx:ditto": {
                    "type": "Ditto user authenticated via nginx"
                },
                "pre-authenticated:kafkaml-connection": {
                    "type": "Connection to KafkaML"
                },
                "pre-authenticated:hono-connection": {
                    "type": "Connection to Eclipse Hono"
                }
            },
            "resources": {
                "policy:/": {
                    "grant": [
                        "READ",
                        "WRITE"
                    ],
                    "revoke": []
                },
                "thing:/": {
                    "grant": [
                        "READ",
                        "WRITE"
                    ],
                    "revoke": []
                },
                "message:/": {
                    "grant": [
                        "READ",
                        "WRITE"
                    ],
                    "revoke": []
                }
            }
        }
    }
}'
