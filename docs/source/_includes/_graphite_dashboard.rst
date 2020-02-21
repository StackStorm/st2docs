[
  {
    "target": [
      "integral(stats.counters.st2.<prefix>.action.executions.count)"
    ],
    "title": "Total Number of Action Executions",
    "height": "308",
    "width": "586"
  },
  {
    "target": [
      "stats.counters.st2.<prefix>.action.executions.rate"
    ],
    "title": "Action Executions per Second",
    "height": "308",
    "width": "586"
  },
  {
    "target": [
      "integral(stats.counters.st2.<prefix>.action.executions.running.count)",
      "sumSeries(stats.counters.st2.<prefix>.action.executions.requested.count)",
      "sumSeries(stats.counters.st2.<prefix>.action.executions.pending.count)",
      "sumSeries(stats.counters.st2.<prefix>.action.executions.delayed.count)",
      "sumSeries(stats.counters.st2.<prefix>.action.executions.paused.count)"
    ],
    "title": "Current Number of Action Execution in Particular State",
    "height": "495",
    "width": "798"
  },
  {
    "logBase": "",
    "target": [
      "stats.timers.st2.<prefix>.action.executions.median"
    ],
    "title": "Median Action Execution Duration (ms)",
    "areaMode": "stacked",
    "minorY": "",
    "height": "469",
    "width": "754"
  },
  {
    "logBase": "",
    "target": [
      "stats.counters.st2.<prefix>.api.request.rate"
    ],
    "title": "API Requests Per Second",
    "areaMode": "stacked",
    "minorY": "",
    "height": "308",
    "width": "586"
  },
  {
    "target": [
      "stats.counters.st2.<prefix>.rule.processed.rate",
      "stats.counters.st2.<prefix>.rule.matched.rate"
    ],
    "title": "Processed trigger instances and matched rules per second",
    "height": "308",
    "width": "586"
  },
  {
    "target": [
      "stats.counters.st2.<prefix>.api.response.status.200.rate",
      "stats.counters.st2.<prefix>.api.response.status.404.rate",
      "stats.counters.st2.<prefix>.api.response.status.201.rate"
    ],
    "title": "API responses per status code per second",
    "height": "308",
    "width": "586"
  },
  {
    "target": [
      "stats.counters.st2.<prefix>.orquesta.action.executions.rate"
    ],
    "title": "Orquesta Workflow and Action Executions per Second",
    "height": "331",
    "width": "697"
  }
]