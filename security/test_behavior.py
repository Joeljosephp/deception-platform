from .behavior import analyze_behavior


events = [

    {
        "asset":"API_KEY"
    },

    {
        "asset":"DATABASE"
    },

    {
        "asset":"SOURCE_CODE"
    }

]


result = analyze_behavior(events)

print(result)