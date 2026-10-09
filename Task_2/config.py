"""Task 2 config: SLA rules, priority weights, agents and other settings."""

TEAMS = ["billing" , "technical" , "delivery" , "account" , "general"]

# SLA time limit per priority , in Business hours..
SLA_HOURS = {"P1" : 4 , "P2" : 8 , "P3" : 24 , "P4" : 48}

# Warning at 75% completion
SLA_WARNING_PERCENTAGE = 75

WEEKEND_DAYS = {6}
HOLIDAYS = {"2026-10-12"} # Just for checking afterwards..

#  Fields for making tickets-->
MANDATORY_FIELDS =["order_id" , "issue" , "contact"]

#duplicate the problem if come again in 24 hours
DUPLICATE_WINDOW_HOURS = 24

# Priority score
PRIORITY_WEIGHTS = {"severity" : 40 , "sentiment" : 20 , "waiting" : 20 , "impact" : 20}  # Severity means how much the problem is big..

PRIORITY_CUTOFFS = {"P1":75 , "P2" : 50 , "P3" : 25}  # Below this - P4

#  Agents: skills , available or not , at now tickets, How much tickets can he/she takes

AGENTS = [
    {"name" : "Amit" , "skills" : ["delivery" , "general"] , "available" : True , "workload":0 , "max_load" : 5},
    {"name" : "Priya" , "skills" : ["billing" , "account"] , "available" : True , "workload":0 , "max_load" : 5},
    {"name" : "Rohan" , "skills" : ["technical" , "general"] , "available" : True , "workload":0 , "max_load" : 5},
]

# EACH LEVEL GETS FRACTION...
SEVERITY_LEVELS = {"low" : 0.0 , "medium" :0.4 , "high":0.75 , "critical" : 1.0}
SENTIMENT_LEVELS =  {"positive": 0.0, "neutral": 0.1, "negative": 0.5,"sarcastic": 0.6, "frustrated": 0.8, "urgent": 1.0}

IMPACT_LEVELS = {"single_customer" : 0.25 , "multiple_customers" : 0.7 , "business" : 1.0}

# WAITING THIS MUCH TIME TO GET FULL POINTS..
WAITING_FULL_HOURS = 24

# PROBLEM OF THIS SEVERITY NEVER GOES BELOW FROM THIS PROIORITY
PRIORITY_FLOOP = {"critical" : "P1"}

# IF two text match this much (0-1) then the problem will consider same...
SIMILARITY_LIMMIT = 0.6