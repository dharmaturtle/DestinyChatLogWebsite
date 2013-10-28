/* sums number of chat messages per hour */

conn = new Mongo();
db = conn.getDB('testDB2');

db.logapp_log.mapReduce(
	function() {
		emit(this.time.getHours(), 1);
	}, 
	function (key, vals) {
		for (var i=0, sum=0; i < vals.length; i++){
			sum += vals[i];
		}
		return sum;
	},
	{
		out : {replace : "logapp_log_populartimes" }
	}
 );

 /* cleaning up after map reduce */
db.logapp_log_populartimes.find().forEach(function(doc){ 
	if (doc._id == 0){
		result = "Midnight";
	}
	else if (doc._id < 12){
		result = doc._id + "am";
	}
	else if (doc._id == 12){
		result = "Noon";
	}
	else {
		result = (doc._id - 12) + "pm";
	}
	db.logapp_log_populartimes.update( /* makes hours more human readable */
		{_id:doc._id},
		{$set:
			{"prettyprint":result}
		}
	);
	db.logapp_log_populartimes.update( /* int hours still necessary so we can sort by it */
		{_id:doc._id},
		{$set:
			{"hour":doc._id}
		}
	);
	db.logapp_log_populartimes.update( /* converts value to int for prettier numbers */
		{value:doc.value},
		{$set:
			{"value":NumberInt( doc.value )}
		}
	);
});