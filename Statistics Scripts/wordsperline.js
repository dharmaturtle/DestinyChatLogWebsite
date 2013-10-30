/* linecounts how many times a word is said */
conn = new Mongo();
db = conn.getDB('testDB2');

/* map reduce */
var map = function() {
	var key = this.user;
	var value = {
					linecount: 1,
					wordcount: this.text.split(' ').length
				};
	emit(key, value);
};

var reduce = function(key, value) {
	r_value = { linecount: 0, wordcount: 0 };
	for (var x = 0; x < value.length; x++){
		r_value.linecount += value[x].linecount;
		r_value.wordcount += value[x].wordcount;
	}
	return r_value;
};

var finalfn = function (key, value) {
	value.linecount = value.linecount;
	value.wordcount = value.wordcount;
	return value;
};

db.logapp_log.mapReduce( map, reduce, {
	out		:	{ replace : "logapp_log_wordline_count" },
	finalize:	finalfn
})

/* cleaning up after map reduce */

/* copies _id to user because Django can't grab id */
db.logapp_log_wordline_count.find().forEach(function(doc){
	db.logapp_log_wordline_count.update(
		{_id : doc._id},
		{$set:
			{
				"user":doc._id,
				"linecount":NumberInt(doc.value.linecount),
				"wordcount":NumberInt(doc.value.wordcount)
			},
		}
	);
});

db.logapp_log_wordline_count.find().forEach(function(doc){
	db.logapp_log_wordline_count.update(
		{_id : doc._id},
		{$unset: { value:1 }}
	);
});

/* calculates total word and line count */
var totalline = 0;
var totalword = 0;
db.logapp_log_wordline_count.find().forEach(function(doc){
	totalline += doc.linecount;
	totalword += doc.wordcount;
});

/* records total word and line count */
db.logapp_log_wordline_count_meta.update(
	{ id : "prime"}, /* this should be the only key */
	{
		_id					: "prime",
		'totalline'			: totalline,
		'totalword'			: totalword,
	},
	{ upsert : true }
);