/* counts how many times a word is said */

conn = new Mongo();
db = conn.getDB('testDB2');

db.logapp_log.mapReduce(
	function() {
		var regex = /[\w']+/g;   /* matches a word */
		var matched = null;
		while (matched = regex.exec(this.text.toLowerCase())) {
			emit(matched[0], 1); /* emits every word */
		}
	}, 
	function (key, vals) {
		for (var i=0, sum=0; i < vals.length; i++){
			sum += vals[i];
		}
		return sum;
	},
	{
		out : {replace : "logapp_log_wordcount" }
	}
);

/* cleaning up after map reduce */
db.logapp_log_wordcount.find().forEach(function(doc){
	db.logapp_log_wordcount.update( /* copies _id to user because Django can't grab id */
		{_id:doc._id},
		{$set:
			{"word":doc._id}
		}
	);
	db.logapp_log_wordcount.update( /* converts value to int for prettier numbers */
		{value:doc.value},
		{$set:
			{"value":NumberInt( doc.value )}
		}
	);
});