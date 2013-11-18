/* It is more efficient to just copy with a parameter in .find()
 * But that doesn't use map reduce, and the entire point of this is to learn map reduce.*/
 
 /******************************************************************************************
  *
  * IMPORTANT: MAKE SURE YOU RUN WORDCOUNT.JS BEFORE THIS
  *
  ******************************************************************************************/

conn = new Mongo();
db = conn.getDB('testDB2');

map = function() {
	var emotes = ["abathur","angelthump","aslan","basedgod","biblethump","callcatz","callchad","dafeels","dappakappa","desbro","djaslan","dravewin","duckerz","durrstiny","feednathan","fidgetlol","frankerz","gameofthrows","heimerdonger","hhhehhehe","infestiny","kappa","klappa","lul","motherfuckingame","notears","ohkrappa","overrustle","sodoge","sosad","surprise","toospicy","uwotm8","whoahdude","worth"];
	if (emotes.indexOf(this._id) > -1)
		emit(this._id, this );
}

reduce = function(key, values) {
	return values[0];
}

db.logapp_log_wordcount.mapReduce(map, reduce,
	{out : {replace : "logapp_log_emote" }}
);

/* The mapreduce's results are very nested like the following:
 * { "_id" : "worth" , "value" : { "_id" : "worth" , "value" : 142 , "word" : "worth"}}
 * This part gets rid of the nesting. */
db.logapp_log_emote.find().forEach(function(doc){
	db.logapp_log_emote.update({_id:doc._id}, /* copies _id to face because Django can't grab id */
		{$set:
			{"face":doc._id}
		}
	);
	db.logapp_log_emote.update(               /* converts value to int for prettier numbers */
		{value:doc.value},
		{$set:
			{"value":NumberInt( doc.value.value )}
		}
	);
});