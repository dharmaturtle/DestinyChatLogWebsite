/* counts how many time a person's name is said */

conn = new Mongo();
db = conn.getDB('testDB2');
var names=new Array();
var Names=new Array();

/* This generates two n/Names arrays, since it is faster to do .toLowerCase
 * here and compare in the map than to run a .toLowerCase on every map run. */
var i = 0;
db.logapp_log_verbosity.find({}, { '_id' : 1 } ).forEach(function(doc){
	names[i] = doc._id.toLowerCase();
	Names[i] = doc._id;
	i++;
});

printjson("Part 1 complete (generating names arrays)");

/* map reduce */
db.logapp_log.mapReduce(
	function() {
		var regex = /[\w']+/g;                                  /* selects words */
		var matched = null;
		while (matched = regex.exec(this.text.toLowerCase())) { /* cycles through text */
			var i=0, name;
			while(name = names[i++]){                           /* cycles through lower cased array */
				if (matched[0] == name){
					emit(Names[i-1], 1);                        /* emits properly cased name by decrementing index to compensate for i++ */
				}
			}
		}
	}, 
	function (key, vals) {                                      /* simple tallying of names */
		for (var i=0, sum=0; i < vals.length; i++){
			sum += vals[i];
		}
		return sum;
	},
	{
		out   : {replace : "logapp_log_popularity" },
		scope : { names : names , Names : Names},               /* adds names and Names to scope so the map function can call them */
	}
);

printjson("Part 2 complete (map reduce finished)");

/* cleaning up after map reduce */
db.logapp_log_popularity.find().forEach(function(doc){
	db.logapp_log_popularity.update( /* copies _id to user because Django can't grab id */
		{_id:doc._id},
		{$set:
			{"user":doc._id}
		}
	);
	db.logapp_log_popularity.update( /* converts value to int for prettier numbers */
		{value:doc.value},
		{$set:
			{"value":NumberInt( doc.value )}
		}
	);
});