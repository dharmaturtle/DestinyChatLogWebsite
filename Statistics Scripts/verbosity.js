/* counts how many times a user has spoken */

conn = new Mongo();
db = conn.getDB('testDB2');
db.logapp_log.mapReduce(
	function() {
		emit(this.user, 1);
	}, 
	function (key, vals) {
		for (var i=0, sum=0; i < vals.length; i++){
			sum += vals[i];
		}
		return sum;
	},
	{
		out : {replace : "logapp_log_verbosity" }
	}
 );

/* cleaning up after map reduce */
db.logapp_log_verbosity.find().forEach(function(doc){
	db.logapp_log_verbosity.update( /* copies _id to user because Django can't grab id */
		{_id:doc._id}, 
		{$set:
			{"user":doc._id}
		}
	);
	db.logapp_log_verbosity.update( /* converts value to int for prettier numbers */
		{value:doc.value},
		{$set:
			{value:NumberInt( doc.value )}
		}
	);
});