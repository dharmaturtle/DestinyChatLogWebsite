conn = new Mongo();
db = conn.getDB('testDB2');
db.logapp_log.mapReduce(
	function() {
		var regex = /[\w']+/g;
		var matched = null;
		while (matched = regex.exec(this.text.toLowerCase())) {
			emit(matched[0], 1);
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


/* adds "word" and changes "value" to "rank", because Django is unhappy with variables beginning with _ */
function wordcount_update(){
	db.logapp_log_wordcount.find().forEach(function(doc){
		db.logapp_log_wordcount.update({_id:doc._id}, {$set:{"word":doc._id}});
		db.logapp_log_wordcount.update({value:doc.value}, {$set:{"rank":NumberInt( doc.value )}});
	});
}
wordcount_update();