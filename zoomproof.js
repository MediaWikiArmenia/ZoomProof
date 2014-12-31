// JsDiff
// Software License Agreement (BSD License)
// Copyright (c) 2009-2011, Kevin Decker <kpdecker@gmail.com>
(function(e,t){var n=function(){function e(e,t,n){if(Array.prototype.map){return Array.prototype.map.call(e,t,n)}var r=new Array(e.length);for(var i=0,s=e.length;i<s;i++){r[i]=t.call(n,e[i],i,e)}return r}function n(e){return{newPos:e.newPos,components:e.components.slice(0)}}function r(e){var t=[];for(var n=0;n<e.length;n++){if(e[n]){t.push(e[n])}}return t}function i(e){var t=e;t=t.replace(/&/g,"&");t=t.replace(/</g,"&lt;");t=t.replace(/>/g,"&gt;");t=t.replace(/"/g,"&quot;");return t}function s(t,n,r,i){var s=0,o=t.length,u=0,a=0;for(;s<o;s++){var f=t[s];if(!f.removed){if(!f.added&&i){var l=n.slice(u,u+f.count);l=e(l,function(e,t){var n=r[a+t];return n.length>e.length?n:e});f.value=l.join("")}else{f.value=n.slice(u,u+f.count).join("")}u+=f.count;if(!f.added){a+=f.count}}else{f.value=r.slice(a,a+f.count).join("");a+=f.count}}return t}function v(e,t,n){t=t||[];n=n||[];var r;for(var r=0;r<t.length;r+=1){if(t[r]===e){return n[r]}}var i;if("[object Array]"===d.call(e)){t.push(e);i=new Array(e.length);n.push(i);for(r=0;r<e.length;r+=1){i[r]=v(e[r],t,n)}t.pop();n.pop()}else if(typeof e==="object"&&e!==null){t.push(e);i={};n.push(i);var s=[];for(var o in e){s.push(o)}s.sort();for(r=0;r<s.length;r+=1){var o=s[r];i[o]=v(e[o],t,n)}t.pop();n.pop()}else{i=e}return i}var o=function(e){this.ignoreWhitespace=e};o.prototype={diff:function(e,r,i){function u(e){if(i){setTimeout(function(){i(t,e)},0);return true}else{return e}}function p(){for(var i=-1*d;i<=d;i+=2){var l;var h=c[i-1],p=c[i+1];g=(p?p.newPos:0)-i;if(h){c[i-1]=t}var v=h&&h.newPos+1<a;var m=p&&0<=g&&g<f;if(!v&&!m){c[i]=t;continue}if(!v||m&&h.newPos<p.newPos){l=n(p);o.pushComponent(l.components,t,true)}else{l=h;l.newPos++;o.pushComponent(l.components,true,t)}var g=o.extractCommon(l,r,e,i);if(l.newPos+1>=a&&g+1>=f){return u(s(l.components,r,e,o.useLongestToken))}else{c[i]=l}}d++}var o=this;if(r===e){return u([{value:r}])}if(!r){return u([{value:e,removed:true}])}if(!e){return u([{value:r,added:true}])}r=this.tokenize(r);e=this.tokenize(e);var a=r.length,f=e.length;var l=a+f;var c=[{newPos:-1,components:[]}];var h=this.extractCommon(c[0],r,e,0);if(c[0].newPos+1>=a&&h+1>=f){return u([{value:r.join("")}])}var d=1;if(i){(function m(){setTimeout(function(){if(d>l){return i()}if(!p()){m()}},0)})()}else{while(d<=l){var v=p();if(v){return v}}}},pushComponent:function(e,t,n){var r=e[e.length-1];if(r&&r.added===t&&r.removed===n){e[e.length-1]={count:r.count+1,added:t,removed:n}}else{e.push({count:1,added:t,removed:n})}},extractCommon:function(e,t,n,r){var i=t.length,s=n.length,o=e.newPos,u=o-r,a=0;while(o+1<i&&u+1<s&&this.equals(t[o+1],n[u+1])){o++;u++;a++}if(a){e.components.push({count:a})}e.newPos=o;return u},equals:function(e,t){var n=/\S/;return e===t||this.ignoreWhitespace&&!n.test(e)&&!n.test(t)},tokenize:function(e){return e.split("")}};var u=new o;var a=new o(true);var f=new o;a.tokenize=f.tokenize=function(e){return r(e.split(/(\s+|\b)/))};var l=new o(true);l.tokenize=function(e){return r(e.split(/([{}:;,]|\s+)/))};var c=new o;c.tokenize=function(e){var t=[],n=e.split(/^/m);for(var r=0;r<n.length;r++){var i=n[r],s=n[r-1];if(i==="\n"&&s&&s[s.length-1]==="\r"){t[t.length-1]+="\n"}else if(i){t.push(i)}}return t};var h=new o;h.tokenize=function(e){return r(e.split(/(\S.+?[.!?])(?=\s+|$)/))};var p=new o;p.useLongestToken=true;p.tokenize=c.tokenize;p.equals=function(e,t){return c.equals(e.replace(/,([\r\n])/g,"$1"),t.replace(/,([\r\n])/g,"$1"))};var d=Object.prototype.toString;return{Diff:o,diffChars:function(e,t,n){return u.diff(e,t,n)},diffWords:function(e,t,n){return a.diff(e,t,n)},diffWordsWithSpace:function(e,t,n){return f.diff(e,t,n)},diffLines:function(e,t,n){return c.diff(e,t,n)},diffSentences:function(e,t,n){return h.diff(e,t,n)},diffCss:function(e,t,n){return l.diff(e,t,n)},diffJson:function(e,n,r){return p.diff(typeof e==="string"?e:JSON.stringify(v(e),t,"  "),typeof n==="string"?n:JSON.stringify(v(n),t,"  "),r)},createPatch:function(t,n,r,i,s){function a(t){return e(t,function(e){return" "+e})}function f(e,t,n){var r=u[u.length-2],i=t===u.length-2,s=t===u.length-3&&(n.added!==r.added||n.removed!==r.removed);if(!/\n$/.test(n.value)&&(i||s)){e.push("\\ No newline at end of file")}}var o=[];o.push("Index: "+t);o.push("===================================================================");o.push("--- "+t+(typeof i==="undefined"?"":"	"+i));o.push("+++ "+t+(typeof s==="undefined"?"":"	"+s));var u=c.diff(n,r);if(!u[u.length-1].value){u.pop()}u.push({value:"",lines:[]});var l=0,h=0,p=[],d=1,v=1;for(var m=0;m<u.length;m++){var g=u[m],y=g.lines||g.value.replace(/\n$/,"").split("\n");g.lines=y;if(g.added||g.removed){if(!l){var b=u[m-1];l=d;h=v;if(b){p=a(b.lines.slice(-4));l-=p.length;h-=p.length}}p.push.apply(p,e(y,function(e){return(g.added?"+":"-")+e}));f(p,m,g);if(g.added){v+=y.length}else{d+=y.length}}else{if(l){if(y.length<=8&&m<u.length-2){p.push.apply(p,a(y))}else{var w=Math.min(y.length,4);o.push("@@ -"+l+","+(d-l+w)+" +"+h+","+(v-h+w)+" @@");o.push.apply(o,p);o.push.apply(o,a(y.slice(0,w)));if(y.length<=4){f(o,m,g)}l=0;h=0;p=[]}}d+=y.length;v+=y.length}}return o.join("\n")+"\n"},applyPatch:function(e,t){var n=t.split("\n");var r=[];var i=false,s=false;for(var o=n[0][0]==="I"?4:0;o<n.length;o++){if(n[o][0]==="@"){var u=n[o].split(/@@ -(\d+),(\d+) \+(\d+),(\d+) @@/);r.unshift({start:u[3],oldlength:u[2],oldlines:[],newlength:u[4],newlines:[]})}else if(n[o][0]==="+"){r[0].newlines.push(n[o].substr(1))}else if(n[o][0]==="-"){r[0].oldlines.push(n[o].substr(1))}else if(n[o][0]===" "){r[0].newlines.push(n[o].substr(1));r[0].oldlines.push(n[o].substr(1))}else if(n[o][0]==="\\"){if(n[o-1][0]==="+"){i=true}else if(n[o-1][0]==="-"){s=true}}}var a=e.split("\n");for(var o=r.length-1;o>=0;o--){var f=r[o];for(var l=0;l<f.oldlength;l++){if(a[f.start-1+l]!==f.oldlines[l]){return false}}Array.prototype.splice.apply(a,[f.start-1,+f.oldlength].concat(f.newlines))}if(i){while(!a[a.length-1]){a.pop()}}else if(s){a.push("")}return a.join("\n")},convertChangesToXML:function(e){var t=[];for(var n=0;n<e.length;n++){var r=e[n];if(r.added){t.push("<ins>")}else if(r.removed){t.push("<del>")}t.push(i(r.value));if(r.added){t.push("</ins>")}else if(r.removed){t.push("</del>")}}return t.join("")},convertChangesToDMP:function(e){var t=[],n;for(var r=0;r<e.length;r++){n=e[r];t.push([n.added?1:n.removed?-1:0,n.value])}return t},canonicalize:v}}();if(typeof module!=="undefined"){module.exports=n}else if(typeof define==="function"){define([],function(){return n})}else if(typeof e.JsDiff==="undefined"){e.JsDiff=n}})(this);


(function($) {
	if (!jQuery().draggable) {
		$.fn.draggable = function() {
			this
				.css('cursor', 'move')
				.on('mousedown touchstart', function(e) {
					var $dragged = $(this);
 
					var x = $dragged.offset().left - e.pageX,
						y = $dragged.offset().top - e.pageY,
						z = $dragged.css('z-index');
 
					if (!$.fn.draggable.stack) {
						$.fn.draggable.stack = 999;
					}
					stack = $.fn.draggable.stack;
					
					$(window)
						.on('mousemove.draggable touchmove.draggable', function(e) {
							$dragged
								.css({'z-index': stack, 'transform': 'scale(1.1)', 'transition': 'transform .3s', 'bottom': 'auto', 'right': 'auto'})
								.offset({
									left: x + e.pageX,
									top: y + e.pageY
								})
								.find('a').one('click.draggable', function(e) {
									e.preventDefault();
								});
 
							e.preventDefault();
						})
						.one('mouseup touchend touchcancel', function() {
							$(this).off('mousemove.draggable touchmove.draggable click.draggable');
							$dragged.css({'z-index': stack, 'transform': 'scale(1)'})
							$.fn.draggable.stack++;
						});
 
					e.preventDefault();
				});
			return this;
		};
	}
})(jQuery);

// ZoomProof
var ZoomProof = function(element) {
	this.editor = element;
	this.data = {};
	this.enabled = false;
	return this;
};

var a, b, words;

ZoomProof.prototype.prepareData = function(callback) {
	this.data.words.forEach(function(word) {
		word.contents = $("<div/>").html(word.contents).text();
	});
	
	a = this.data.words.map(function(word){
		return word.contents;
	}).join('');
};

ZoomProof.prototype.update = function(callback) {
	b = this.editor.value;
	JsDiff.diffWordsWithSpace(a, b, function(err, diff) {
		if(err) {
			callback(err);
			return;
		}
		
		var ap = 0;
		var bp = 0;
		words = diff.map(function(diff) {
			var position = {
				startA: -1,
				endA: -1,
				startB: -1,
				endB: -1,
				value: diff.value,
				length: diff.value.length,
				added: diff.added,
				removed: diff.removed
			};
			
			if(!diff.added) {
				position.startA = ap;
				ap += position.length;
				position.endA = ap;
			}
			
			if(!diff.removed) {
				position.startB = bp;
				bp += position.length;
				position.endB = bp;
			}
			
			return position;
		});	
		
		callback(null);
	});
};

ZoomProof.prototype.find = function(position) {
	var p = 0;
	for(var i = 0; i < this.data.words.length; ++i) {
		var word = this.data.words[i];
		if(p <= position && position <= p + word.contents.length) {
			return word;
		}
		p += word.contents.length;
	}
	return null;
};

ZoomProof.prototype.enable = function(json) {
	this.data = json;
	this.enabled = true;
	this.prepareData();
	
	var $editor = $(this.editor);
	var self = this;
	
	var $body = $(document.body);
	
	var $image = $(".prp-page-image img");
	var imageUrl = $image.attr("src");
	
	var ratio;
	
	var $highlight = $('<div/>')
		.css({
			position: 'absolute',
			zIndex: 100,
			backgroundColor: 'rgba(255,255,0,.5)',
			top: '50%',
			left: '50%'
		});
		
	var $zoomedImage = $('<img/>')
		.attr('src', imageUrl)
		.css({
			position: 'absolute',
			top: '50%',
			left: '50%',
			transition: '.4s all'
		})
		.on('load', function() {
			ratio = $(this).width() / self.data.size.width;
		});
		
	var $ZoomProofUI = $('<div/>')
		.css({ // TODO
			width: 400,
			height: 200,
			border: '4px solid rgba(0,0,0,0.5)',
			position: 'absolute',
			top: 0,
			right: 0,
			borderRadius: 6,
			overflow: 'hidden',
			background: 'white',
			cursor: 'move'
		})
		.draggable();
	
	$zoomedImage.appendTo($ZoomProofUI);
	$highlight.appendTo($ZoomProofUI)
		
	$ZoomProofUI.appendTo($body);
	
	
	var doWithDelay = (function(){
		var timeoutId = -1;
		return function(fn, dl) {
			if(timeoutId >= 0) {
				clearTimeout(timeoutId);
				timeoutId = -1;
			}
			timeoutId = setTimeout(function() {
				timeoutId = -1;
				fn();
			}, dl);
		};
	})();
	
	
	var highlight = function() {
		var selectionStart = $editor.prop("selectionStart");
		var selectionEnd  = $editor.prop("selectionEnd");
		var selectionDirection = $editor.prop("selectionDirection");
		
		var caret = selectionDirection === 'forward' 
				  ? selectionEnd
				  : selectionStart;
		
		var i;
		for(i = 0; i < words.length; ++i) {
			if(words[i].startB <= caret && caret <= words[i].endB) {
				break;
			}
		}
		
		if(i == words.length) {
			// Corresponding point was not found!
			return;
		}
		
		function isKeyPoint(point) {
			return point.startA >= 0
				&& point.startB >= 0
				&& point.value.trim().length > 0;
		}
		
		var j = i;
		while (!isKeyPoint(words[j])) {
			if(j-- === 0) {
				break;
			}
		}
		if(j === -1) {
			// Previous keypoint was not found!
			return;
		}
		
		var k = i;
		while (!isKeyPoint(words[k])) {
			if(++k === words.length) {
				break;
			}
		}
		if(k === words.length) {
			// Next keypoint was not found!
			return;
		}
		
		
		var lengthA = words[k].endA - words[j].startA;
		
		var lengthB = words[k].endB - words[j].startB;
		
		var offset = (caret - words[j].startB) / lengthB;
		var word = self.find(words[j].startA + Math.round(offset * lengthA));
		
		$zoomedImage.css({
			marginTop: -word.position.top * ratio -word.size.height / 2 * ratio,
			marginLeft: -word.position.left * ratio -word.size.width / 2 * ratio
		});
		
		$highlight.css({
			marginTop: - word.size.height / 2 * ratio,
			marginLeft: - word.size.width / 2 * ratio,
			width: word.size.width * ratio,
			height: word.size.height * ratio
		});
		
		return;
	};
	
	$editor.on('change paste', function(e) {
		console.log(e);
		doWithDelay(function() {
			self.update(function(){
				highlight();
			});
		}, 200);
	}).on('keyup click focus', function(e) {
		if(!words) {
			return;
		}
		highlight();
	}).trigger('change');
};

function init () {
	var editor = document.getElementById('wpTextbox1');
	if(!editor) {
		return;
	}
	var instance = new ZoomProof(editor);
	
	var title = mw.config.get("wgTitle");
	var jsonTitle = title + '.json';
	
	
	var data = {
		title: jsonTitle,
		action: "raw",
		ctype: "application/json"
	};

	$.getJSON('/', data).done(function(json) {
		console.log('ZoomProof data files found. Enabling ZoomProof.');
		instance.enable(json);
	}).fail(function(err){
		console.log('No ZoomProof data files found. Disabling ZoomProof.', err);
	});
}
	
$(init);
