$(document).ready(function(){
	responseConsequence = {};
	$.get('/getword/',{cnt:0},function(data){
		wordObj = data;
		$('#bb-show').append("<div>"+data['ch'][0]+"</div>");
		$('#blackboard').attr('myAttr','0');
		globalCnt=0;
	});
	$("button").click(function(){
		if (wordObj['ch'].length<20&&globalCnt+1==wordObj['ch'].length) {
			var inputValue = $.trim($("input[name='en-input']").val());
			addIn(inputValue);
			calculate();
			alert('已经是最后一个单词了，开启循环！');
			window.location.reload(); 
			return false;
		}
		// console.log(globalCnt+'&&'+wordObj['ch'].length);
		if (globalCnt+1==wordObj['ch'].length) {
			var cnt = $('#blackboard').attr('myAttr');
			cnt = parseInt(cnt);
			cnt++;
			var cnt_s = cnt.toString();
			$('#blackboard').attr('myAttr',cnt_s);
			calculate();
			$.get('/getword/',{cnt:cnt},function(data){
				wordObj=data;
			});
			globalCnt=0;
			responseConsequence = {};
		}
		var inputValue = $.trim($("input[name='en-input']").val());
		addIn(inputValue);
		globalCnt++;
		$("#bb-show").html("");
		$('#bb-show').append(wordObj['ch'][globalCnt]);
		$("input[name='en-input']").val('');
	})
})

function addIn(ipt){
	var index = globalCnt;
	var score = '';
	var matchResult = wordObj['en'][index]==ipt?true:false;
	if (matchResult) {
		$("#reminder").html("<span style='color:red'>right!</span>");
	}else{
		$("#reminder").html("<span style='color:red'>wrong!</span>");
	}
	if (!responseConsequence.hasOwnProperty(wordObj['wi'][index])) {
		score = matchResult?'0/1':'1/1';
		responseConsequence[wordObj['wi'][index]] = score;
	}else{
		var tempstr = responseConsequence[wordObj['wi'][index]];
		var tempstrarr = tempstr.split("/");
		var temp_up = parseInt(tempstrarr[0]);
		var temp_down = parseInt(tempstrarr[1]);
		if (matchResult) {
			var score = (temp_up).toString()+'/'+(temp_down+1).toString();
		}else{
			var score = (temp_up+1).toString()+'/'+(temp_down+1).toString();
		}
		responseConsequence[wordObj['wi'][index]] = score;
	}
}

function calculate(){
	var resp_json = JSON.stringify(responseConsequence);
	$.get('/calculate/',{consequence:resp_json},function(data){});
}