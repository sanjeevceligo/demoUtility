"""
Enhanced Production Queries for Snowflake Dashboard
Real queries for production data analysis
"""

PRODUCTION_QUERIES = {
    "🔍 User & Account Analysis": {
        "Get User by ID": {
            "query": "select * from DATA_ROOM.MONGODB.USERS WHERE _ID = '6474c249d3e7670148a92b25'",
            "description": "Retrieve specific user details by user ID"
        },
        "Get User by Email": {
            "query": "select * from DATA_ROOM.MONGODB.USERS WHERE email = 'asunley@marianipremiergroup.com'",
            "description": "Find user by email address"
        },
        "Get User Microservices Config": {
            "query": "select microservices from users where _id = '642728ad041e1475d6c8f321'",
            "description": "Get microservices configuration for a user"
        },
        "User Verification Status": {
            "query": "select verified, count(*) as user_count from users group by verified",
            "description": "Distribution of user verification status"
        }
    },
    
    "📤 Export/Import Operations": {
        "Get Export by ID": {
            "query": "select * from _exports WHERE export_id = '5feb0e50056747047168bd22'",
            "description": "Get specific export details"
        },
        "Get Import by ID": {
            "query": "select * from _imports where IMPORT_ID = '671127044e30587ce240c78c'",
            "description": "Get specific import details"
        },
        "Export Full Object": {
            "query": "select OBJECT_CONSTRUCT( * ) from exports where _id='624cb7627904946a6115ebf1'",
            "description": "Get complete export object structure"
        },
        "Import Full Object": {
            "query": "select OBJECT_CONSTRUCT( * ) from imports where _id='66e870b8cdfd8b4b8fe6a3cc'",
            "description": "Get complete import object structure"
        },
        "Import Types Analysis": {
            "query": "select adaptortype, COUNT(*) as occurrence from imports group by adaptortype order by occurrence desc",
            "description": "Most common import adaptor types"
        },
        "Export Types Analysis": {
            "query": "select adaptortype, COUNT(*) as occurrence from exports group by adaptortype order by occurrence desc",
            "description": "Most common export adaptor types"
        }
    },
    
    "⚙️ Flow Management": {
        "Get Flow by ID": {
            "query": "select * from DATA_ROOM.MONGODB.FLOWS where _ID = '682e063bbbfea077bbe94ca9'",
            "description": "Get specific flow configuration"
        },
        "User Flows with Processors": {
            "query": "select *, ARRAY_SIZE(PAGEPROCESSORS) from flows where _userid = '5f7b40aa8b0d066e21b294dc'",
            "description": "Get flows for user with processor count"
        },
        "Flows by Name and User": {
            "query": "SELECT name, _id, _sourceId FROM mongodb.FLOWS WHERE _userId IN ('604916f89716277b7a653731')",
            "description": "Get flows by specific user ID"
        },
        "Flow with Full Object": {
            "query": "select OBJECT_CONSTRUCT( * ) from flows where _id='624cb7657904946a6115ebfa'",
            "description": "Complete flow object with all details"
        },
        "Complex Flow Analysis": {
            "query": """select distinct *,ARRAY_SIZE(PAGEPROCESSORS),ARRAY_SIZE(PAGEGENERATORS),PAGEPROCESSORSRAW,PAGEGENERATORSRAW 
from flows where ARRAY_SIZE(PAGEPROCESSORS)>=1 and ARRAY_SIZE(PAGEGENERATORS)>=7 
AND NAME='DF5 Import Inventory Transfers from RICS to NetSuite'""",
            "description": "Analyze complex flows with multiple processors and generators"
        },
        "Flows with Many Generators": {
            "query": """select OBJECT_CONSTRUCT( * ),ARRAY_SIZE(PAGEGENERATORS),NAME from flows 
where _USERID = '5301043caa20740200000001' AND ARRAY_SIZE(PAGEGENERATORS)>8
AND NAME like 'DF04 -- SFDC to Snowflake (daily schedule)'""",
            "description": "Flows with high number of page generators"
        },
        "Flow Response Mapping Analysis": {
            "query": """select OBJECT_CONSTRUCT( * ),PAGEPROCESSORSRAW from flows 
where _userid = '5f7b40aa8b0d066e21b294dc' 
AND (PARSE_JSON(PAGEPROCESSORSRAW):responseMapping IS NULL)""",
            "description": "Flows missing response mapping configuration"
        }
    },
    
    "🔗 Connection Analysis": {
        "User Connections": {
            "query": "select * from _connections WHERE user='63c530e37509483cdcc1af96'",
            "description": "Get all connections for a specific user"
        },
        "OAuth Connections by App": {
            "query": """SELECT APP, Count(*) as ConnectionCount FROM
(SELECT * FROM DATA_ROOM.MONGODB.CONNECTIONS WHERE HTTP:auth:oauth is NOT NULL) 
Group by APP ORDER BY ConnectionCount desc""",
            "description": "OAuth connections distribution by application"
        },
        "Connection Full Object": {
            "query": "select OBJECT_CONSTRUCT( * ) from connections where _id='66e478dba1ec42ac4b9d2b5c'",
            "description": "Complete connection configuration"
        },
        "Apps Distribution": {
            "query": "select app, COUNT(*) as occurrence from connections group by app order by occurrence desc",
            "description": "Most popular connection apps"
        },
        "HTTP Endpoints Usage": {
            "query": "select endpoint, COUNT(*) as occurrence from connections where app='http' group by endpoint order by occurrence desc",
            "description": "Most used HTTP endpoints"
        },
        "Endpoint Import Analysis": {
            "query": """SELECT t2.endpoint, COUNT(*) AS total_imports
FROM DATA_ROOM.MONGODB.imports AS t1
INNER JOIN DATA_ROOM.MONGODB.connections AS t2 ON t1._connectionid = t2._id
GROUP BY t2.endpoint""",
            "description": "Import activity by endpoint"
        },
        "Connection Apps & Endpoints": {
            "query": "select endpoint, app, COUNT(*) as occurrence from connections group by app order by occurrence desc",
            "description": "Connection distribution by app and endpoint"
        },
        "Distinct Apps List": {
            "query": "select distinct app from connections order by app asc",
            "description": "All unique application types"
        }
    },
    
    "📜 License & Audit Management": {
        "User License": {
            "query": "select * from licenses WHERE _userid= '5301043caa20740200000001'",
            "description": "Get license information for user"
        },
        "Rollout Audit Records": {
            "query": "SELECT * FROM ms_rollout_audit where resource_type='users' and resource_id='642728ad041e1475d6c8f321'",
            "description": "Microservice rollout audit for user"
        },
        "Active License Tiers": {
            "query": "select tier, count(*) as license_count from licenses where expires > current_date() group by tier",
            "description": "Distribution of active license tiers"
        }
    },
    
    "🎯 User Segmentation & Tiers": {
        "Detailed User Segmentation": {
            "query": """SELECT 
    DISTINCT CASE 
        WHEN u.emaildomain = 'celigo.com' THEN 'internal'
        WHEN nc.customer_segment = '' THEN 'free' 
        ELSE nc.customer_segment 
    END AS tiers,
    CASE
        WHEN u.MICROSERVICES:enableHttp IS NULL OR u.MICROSERVICES:enableHttp = 'false' THEN 'false'
        ELSE u.MICROSERVICES:enableHttp
    END AS status,
    IFF(u.subdomain IS NULL, 'NA', 'EU') AS domain,
    c._userid AS userId,
    u.email AS email
FROM connections c
LEFT JOIN NETSUITE.CUSTOMER_IDS ncids ON ncids.io_id = c._USERID AND c.type IN ('http', 'rest')
LEFT JOIN NETSUITE.CUSTOMERS nc ON nc.internal_id = ncids.NS_CUSTOMER_ID
INNER JOIN users u ON u._id = c._userid""",
            "description": "Comprehensive user tier and domain analysis"
        },
        "Active Users by Tier & Domain": {
            "query": """select  CASE 
            WHEN u.emaildomain='celigo.com' THEN 'internal'
            WHEN nc.customer_segment = '' THEN 'free' 
            ELSE nc.customer_segment END tiers,
        IFF(u.subdomain is null, 'NA', 'EU') domain,
        count(distinct c._userid) from connections c
INNER JOIN NETSUITE.CUSTOMER_IDS ncids on ncids.io_id=c._USERID AND type in ('http', 'rest')
INNER JOIN NETSUITE.CUSTOMERS nc on nc.internal_id=ncids.NS_CUSTOMER_ID
INNER JOIN users u on u._id=c._userid
WHERE (u._id in (SELECT distinct _userId FROM EXPORTS exp INNER JOIN INFLUXDB.usage_stats us ON us.exp_or_imp_id=exp._id AND END_DATE > CURRENT_DATE - 90)
or u._id in (SELECT distinct _userId FROM IMPORTS imp INNER JOIN INFLUXDB.usage_stats us ON us.exp_or_imp_id=imp._id AND END_DATE > CURRENT_DATE - 90))
group by 1,2 order by 2,1""",
            "description": "Active users with recent usage by tier and domain"
        }
    },
    
    "⚠️ Anomaly Detection": {
        "All Anomaly Events": {
            "query": "select * from influxdb.anomaly_events",
            "description": "All detected anomaly events"
        },
        "User Specific Anomalies": {
            "query": "select * from influxdb.anomaly_events where uid IN ('6390aa56efa6681af404d2f5') ORDER BY time desc",
            "description": "Anomalies for specific user"
        },
        "Recent API Anomalies": {
            "query": "select * from influxdb.api_anomaly_events order by time desc limit 1000",
            "description": "Recent API anomaly events"
        },
        "App-based Anomaly Analysis": {
            "query": """select c.app, ae.*
from influxdb.anomaly_events ae
left outer join mongodb.imports i on ae.exp_or_imp_id=i._id
left outer join mongodb.exports e on ae.exp_or_imp_id=e._id
inner join mongodb.connections c on (c._id=i._connectionid or c._id=e._connectionid)""",
            "description": "Anomalies grouped by application type"
        }
    },
    
    "🚀 Canary Rollout Management": {
        "Canary Groups": {
            "query": "select * from release_canary_groups",
            "description": "All canary release groups"
        },
        "Canary Audit Trail": {
            "query": "select * from canary_rollout_audit",
            "description": "Canary rollout audit records"
        },
        "Canary Phase Distribution": {
            "query": """WITH user_group as (SELECT
    u._id AS user_id, u.name, u.email, u.verified,
    CASE
        WHEN u.emailDomain = 'celigo.com' THEN 'internal'
        WHEN l.tier = 'free' and l.trialenddate > CURRENT_DATE() THEN 'free-trial'
        WHEN l.tier = 'free' THEN 'free'
        ELSE ef.canary_group_name
    END as phase, l.tier
FROM users u INNER JOIN licenses l ON l._userId = u._id
LEFT JOIN (SELECT e.canary_group_name, f.value::STRING AS user_id, e.release_name, e.version
    FROM release_canary_groups e, LATERAL FLATTEN(input => e.USER_IDS) f 
) ef ON ef.user_id = u._id and ef.RELEASE_NAME='2025.5.1' and ef.version='1.0'
WHERE l.type in ('integrator', 'endpoint', 'platform', 'diy') and l.tier != 'none'
    and (l.tier = 'free' OR l.expires > current_date())
) select phase, count(*) as user_count from user_group group by phase ORDER BY phase""",
            "description": "User distribution across canary phases"
        },
        "Canary with Audit Analysis": {
            "query": """WITH user_group as (SELECT u._id AS user_id, u.name, u.email, u.verified,
    CASE WHEN u.emailDomain = 'celigo.com' THEN 'internal'
        WHEN l.tier = 'free' and l.trialenddate > CURRENT_DATE() THEN 'free-trial'
        WHEN l.tier = 'free' THEN 'free' ELSE ef.canary_group_name END as phase,
    l.tier, coalesce(u.subdomain, 'na') subdomain
FROM users u INNER JOIN licenses l ON l._userId = u._id
LEFT JOIN (SELECT e.canary_group_name, f.value::STRING AS user_id, e.release_name, e.version
    FROM release_canary_groups e, LATERAL FLATTEN(input => e.USER_IDS) f
) ef ON ef.user_id = u._id and ef.RELEASE_NAME='2025.5.1' and ef.version='1.0'
WHERE l.type in ('integrator', 'endpoint', 'platform', 'diy') and l.tier != 'none'
    and (l.tier = 'free' OR l.expires > current_date())
), canary_audit as (SELECT * FROM canary_rollout_audit WHERE time >= '2025-06-04'
QUALIFY ROW_NUMBER() OVER (PARTITION BY uid ORDER BY time DESC) = 1)
select email, uid, phase, time, release_version from canary_audit ca inner join user_group ug on ca.uid=ug.phase""",
            "description": "Canary phases with audit trail correlation"
        }
    },
    
    "⚙️ Integration & System Settings": {
        "Integration Canary Settings": {
            "query": "select settings:\"canary-new-deployment\" from integrations where _id = '66c8ae223a88959f6144edd4'",
            "description": "Canary deployment settings for integration"
        },
        "Scripts from S3": {
            "query": "select * from DATA_ROOM.integrator_s3.scripts LIMIT 10",
            "description": "Integration scripts data from S3"
        },
        "Flow by Specific ID": {
            "query": "select * from flows WHERE _id= '5301043caa20740200000001'",
            "description": "Get specific flow by ID"
        }
    }
}

def get_query_by_category(category):
    """Get all queries for a specific category"""
    return PRODUCTION_QUERIES.get(category, {})

def get_all_categories():
    """Get all available query categories"""
    return list(PRODUCTION_QUERIES.keys())

def search_queries(keyword):
    """Search for queries containing a keyword"""
    results = {}
    for category, queries in PRODUCTION_QUERIES.items():
        matching_queries = {}
        for name, details in queries.items():
            if (keyword.lower() in name.lower() or 
                keyword.lower() in details['description'].lower() or 
                keyword.lower() in details['query'].lower()):
                matching_queries[name] = details
        if matching_queries:
            results[category] = matching_queries
    return results

def get_featured_queries():
    """Get a selection of featured queries for dashboard"""
    featured = {
        "Quick User Lookup": PRODUCTION_QUERIES["🔍 User & Account Analysis"]["Get User by ID"],
        "OAuth Connections": PRODUCTION_QUERIES["🔗 Connection Analysis"]["OAuth Connections by App"],
        "Recent Anomalies": PRODUCTION_QUERIES["⚠️ Anomaly Detection"]["Recent API Anomalies"],
        "Canary Distribution": PRODUCTION_QUERIES["🚀 Canary Rollout Management"]["Canary Phase Distribution"],
        "Active User Tiers": PRODUCTION_QUERIES["🎯 User Segmentation & Tiers"]["Active Users by Tier & Domain"]
    }
    return featured 