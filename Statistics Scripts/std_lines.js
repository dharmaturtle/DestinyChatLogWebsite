/* linecounts how many times a word is said */
conn = new Mongo();
db = conn.getDB('testDB2');

/* https://gist.github.com/RedBeard0531/1886960 */ 
var map = function(){
	emit(1,
		{	sum: this.text.split(' ').length, // the field you want stats for
			count:1,
			diff: 0, // M2,n:  sum((val-mean)^2)
		}
	);
};
 
var reduce = function(key, values) {
	var a = values[0]; // will reduce into here
	for (var i=1; i < values.length; i++){
		var b = values[i]; // will merge 'b' into 'a'
		var delta = a.sum/a.count - b.sum/b.count; // a.mean - b.mean
		var weight = (a.count * b.count)/(a.count + b.count);
		a.diff += b.diff + delta*delta*weight;
		a.sum += b.sum;
		a.count += b.count;
	}
	return a;
};
 
var finalfn = function (key, value) {
	value.avg = value.sum / value.count;
	value.variance = value.diff / value.count;
	value.stddev = Math.sqrt(value.variance);
	return value;
};

db.logapp_log_small.mapReduce( map, reduce, {
	out		:	{ replace : "logapp_log_wordline_std" },
	finalize:	finalfn
});

/* records total word and line count */
db.logapp_log_wordline_std.find().forEach(function(doc){
	db.logapp_log_wordline_std_meta.update(
		{_id : "prime"}, /* this should be the only key */
		{
			_id				: "prime",
			'avg'			: doc.value.avg,
			'stddev'		: doc.value.stddev,
		},
		{ upsert : true }
	);
});
/*
db.logapp_log_wordline_count.update(
	{_id : this._id},
	{$unset: { value:1 }}
);*/