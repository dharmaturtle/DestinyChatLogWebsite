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

/* adds "user" and changes "value" to "rank", because Django is unhappy with variables beginning with _ */
function verbosity_update(){
	db.logapp_log_verbosity.find().forEach(function(doc){
		db.logapp_log_verbosity.update({_id:doc._id}, {$set:{"user":doc._id}});
	});
}
verbosity_update();
db.logapp_log_verbosity.update({}, {$rename: {'value':'rank'}}, false, true);