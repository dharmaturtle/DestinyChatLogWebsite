/* counts how many times someone says someone else's name */

conn = new Mongo();
db = conn.getDB('testDB2');
var names=new Array();
var Names=new Array();

/* This generates two names/Names arrays, since it is faster to do .toLowerCase
 * here and compare in the map than to run a .toLowerCase on every map run. */
var i = 0;
db.logapp_log_verbosity.find({}, { '_id' : 1 } ).forEach(function(doc){
	names[i] = doc._id.toLowerCase();
	Names[i] = doc._id;
	i++;
});

printjson("Part 1 complete! (Generating names arrays)");

/* map reduce */
db.logapp_log.mapReduce(
	function() {
		var regex = /[\w']+/g;                                  /* selects words */
		var matched = null;
		while (matched = regex.exec(this.text.toLowerCase())) { /* cycles through logapp_log's text */
			var i=0, name;
			while(name = names[i++]){                           /* cycles through lower cased array */
				if (matched[0] == name){
					emit(	{ talker:this.user,                 /* the key is a pair of keyvalues describing the talker and listener */
							  listener:Names[i-1]               /* emits properly cased name by decrementing index to compensate for i++ */
							} , 1                               /* talker talked to the listener exactly once */
						);  
				}
			}
		}
	}, 
	function (key, vals) {                                      /* simple tallying of who talked to who */
		for (var i=0, sum=0; i < vals.length; i++){
			sum += vals[i];
		}
		return sum;
	},
	{
		out   : {replace : "logapp_log_network" },
		scope : { names : names , Names : Names},               /* adds names and Names to scope so the map function can call them */
	}
);

printjson("Part 2 complete! (Map reduce finished)");

/* Creates network_summary, cleaning up after mapreduce
 * A complete mess, .update()'ing arrays is complicated */
db.logapp_log_network.find().forEach(function(doc){
	if (doc.value > 10){                                        /* If they haven't spoken 10x to that person, probably not friends. */
		db.logapp_log_network_summary.update(
			{ talker : doc._id.talker},
			{ $push:                                            /* in the array */
				{ listener:                                     /* inserts listener and # of times talked to */
					{   $each: [ { user:doc._id.listener , value:NumberInt(doc.value) } ],
						$sort: { "value": -1 },                 /* order from largest to smallest */
						$slice: -10000,                         /* last 10k hits, since MongoDB doesn't support the first N hits, and $sort doesn't work w/o $slice. Really. */
					}
				},
			  $inc: { sumvalue : NumberInt(doc.value) }         /* how many total times someone was spoken to by this person*/
			},
			{ upsert : true }
		);
	}
});